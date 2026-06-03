"""
Vector Store — lưu & tìm kiếm vector trong KnowledgeChunks table.
FIX #1/#4: Class-level shared cache — dùng chung cho tất cả requests, không reload mỗi request.
FIX #2:    Numpy vectorized search — nhanh hơn 10-50x so với pure Python.
"""
import json
import math
import threading
from typing import List, Dict, Optional, Any, Tuple
from sqlalchemy.orm import Session
from Models.Chat import KnowledgeChunk

# ─── Numpy optional ───────────────────────────────────────────────────
try:
    import numpy as np
    _HAS_NUMPY = True
except ImportError:
    _HAS_NUMPY = False
    print("[VectorStore] numpy không tìm thấy — dùng pure Python fallback")


def _cosine_python(a: List[float], b: List[float]) -> float:
    """Cosine similarity thuần Python — fallback khi không có numpy"""
    if len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


# Giữ alias backward-compat
cosine_similarity = _cosine_python


class VectorStore:
    """
    In-memory vector search trên KnowledgeChunks.
    Class-level cache chia sẻ giữa mọi instance/request → chỉ load DB 1 lần.
    Numpy matrix search cho tốc độ tối đa khi có thể.
    """

    # ═══ Class-level shared state ═══
    _class_cache: Optional[List[Dict]] = None
    _class_matrix: Optional[Any] = None   # numpy matrix (n_chunks × dim) đã normalize
    _class_lock = threading.Lock()

    def __init__(self, db: Session):
        self.db = db

    # ─────────────── CACHE MANAGEMENT ───────────────

    def _load_cache(self):
        """Load tất cả chunks có embedding từ DB vào class-level memory"""
        chunks = (
            self.db.query(KnowledgeChunk)
            .filter(KnowledgeChunk.embedding_vector.isnot(None))
            .filter(KnowledgeChunk.embedding_vector != "")
            .all()
        )
        cache = []
        for c in chunks:
            try:
                vec = json.loads(c.embedding_vector)
                if isinstance(vec, list) and len(vec) > 0:
                    cache.append({
                        "chunk_id": c.chunk_id,
                        "content": c.content,
                        "content_type": c.content_type,
                        "source_id": c.source_id,
                        "source_table": c.source_table,
                        "vector": vec,
                        "metadata": json.loads(c.metadata_json) if c.metadata_json else {},
                    })
            except (json.JSONDecodeError, TypeError):
                continue

        VectorStore._class_cache = cache

        # Pre-compute numpy normalized matrix — cosine = dot product với normalized vectors
        if _HAS_NUMPY and cache:
            try:
                matrix = np.array([item["vector"] for item in cache], dtype=np.float32)
                norms = np.linalg.norm(matrix, axis=1, keepdims=True)
                norms[norms == 0] = 1.0
                VectorStore._class_matrix = matrix / norms
            except Exception as e:
                print(f"[VectorStore] Không tạo được numpy matrix: {e}")
                VectorStore._class_matrix = None
        else:
            VectorStore._class_matrix = None

        print(f"[VectorStore] Loaded {len(cache)} chunks | numpy={'yes' if _HAS_NUMPY else 'no'}")

    def _ensure_cache(self):
        """Lazy load class-level cache khi cần (thread-safe)"""
        if VectorStore._class_cache is None:
            with VectorStore._class_lock:
                if VectorStore._class_cache is None:
                    self._load_cache()

    def invalidate_cache(self):
        """Xóa cache — gọi sau khi ETL cập nhật chunks"""
        with VectorStore._class_lock:
            VectorStore._class_cache = None
            VectorStore._class_matrix = None
        print("[VectorStore] Cache invalidated")

    # ─────────────── SEARCH ───────────────

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        threshold: float = 0.35,
        content_type: str = None,
    ) -> List[Dict]:
        """
        Tìm top-k chunks tương đồng nhất với query_embedding.
        - Numpy vectorized (fast path) khi không filter content_type
        - Pure Python fallback khi có filter hoặc numpy không cài
        """
        self._ensure_cache()
        cache = VectorStore._class_cache
        if not cache or not query_embedding:
            return []

        # ── Fast path: numpy, không filter content_type ──
        if _HAS_NUMPY and VectorStore._class_matrix is not None and content_type is None:
            try:
                q = np.array(query_embedding, dtype=np.float32)
                q_norm = np.linalg.norm(q)
                if q_norm == 0:
                    return []
                q = q / q_norm
                sims = VectorStore._class_matrix @ q  # (n_chunks,)

                indices = np.where(sims >= threshold)[0]
                if len(indices) == 0:
                    return []
                top_indices = indices[np.argsort(-sims[indices])[:top_k]]

                return [
                    {
                        "content": cache[int(idx)]["content"],
                        "content_type": cache[int(idx)]["content_type"],
                        "source_id": cache[int(idx)]["source_id"],
                        "similarity": round(float(sims[idx]), 4),
                        "metadata": cache[int(idx)]["metadata"],
                    }
                    for idx in top_indices
                ]
            except Exception as e:
                print(f"[VectorStore] Numpy search error: {e} — fallback Python")

        # ── Slow path: pure Python (hoặc có filter content_type) ──
        items = cache if not content_type else [i for i in cache if i["content_type"] == content_type]
        scored: List[Tuple[float, Dict]] = []
        for item in items:
            sim = _cosine_python(query_embedding, item["vector"])
            if sim >= threshold:
                scored.append((sim, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "content": item["content"],
                "content_type": item["content_type"],
                "source_id": item["source_id"],
                "similarity": round(sim, 4),
                "metadata": item["metadata"],
            }
            for sim, item in scored[:top_k]
        ]

    # ─────────────── ETL HELPERS ───────────────

    def upsert_chunk(
        self,
        content: str,
        content_type: str,
        source_id: int,
        source_table: str,
        embedding: List[float],
        metadata: dict = None,
    ) -> KnowledgeChunk:
        """Tạo hoặc cập nhật chunk — dùng trong ETL"""
        existing = (
            self.db.query(KnowledgeChunk)
            .filter(
                KnowledgeChunk.source_table == source_table,
                KnowledgeChunk.source_id == source_id,
                KnowledgeChunk.content_type == content_type,
            )
            .first()
        )

        vec_json = json.dumps(embedding) if embedding else None
        meta_json = json.dumps(metadata, ensure_ascii=False) if metadata else None

        if existing:
            existing.content = content
            existing.embedding_vector = vec_json
            existing.metadata_json = meta_json
        else:
            existing = KnowledgeChunk(
                content=content,
                content_type=content_type,
                source_id=source_id,
                source_table=source_table,
                embedding_vector=vec_json,
                metadata_json=meta_json,
            )
            self.db.add(existing)

        return existing

    def delete_by_source(self, source_table: str):
        """Xóa tất cả chunks theo source_table — dùng trước khi re-seed"""
        self.db.query(KnowledgeChunk).filter(
            KnowledgeChunk.source_table == source_table
        ).delete()
        self.db.commit()

    def get_chunk_count(self) -> int:
        """Đếm tổng chunks có embedding"""
        return (
            self.db.query(KnowledgeChunk)
            .filter(KnowledgeChunk.embedding_vector.isnot(None))
            .count()
        )
