"""
Vector Store — lưu & tìm kiếm vector trong KnowledgeChunks table.
Cosine similarity thuần Python, in-memory cache cho tốc độ.
"""
import json
import math
import threading
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from Models.Chat import KnowledgeChunk


def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Cosine similarity thuần Python — không cần numpy"""
    if len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class VectorStore:
    """
    In-memory vector search trên KnowledgeChunks.
    Load vectors 1 lần từ DB → cache trong RAM → cosine search nhanh.
    """

    def __init__(self, db: Session):
        self.db = db
        self._cache: Optional[List[Dict]] = None
        self._lock = threading.Lock()

    def _load_cache(self):
        """Load tất cả chunks có embedding từ DB vào memory"""
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
        self._cache = cache
        print(f"[VectorStore] Loaded {len(cache)} chunks vào cache")

    def _ensure_cache(self):
        """Lazy load cache khi cần"""
        if self._cache is None:
            with self._lock:
                if self._cache is None:
                    self._load_cache()

    def invalidate_cache(self):
        """Xóa cache — gọi sau khi ETL cập nhật chunks"""
        with self._lock:
            self._cache = None

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        threshold: float = 0.35,
        content_type: str = None,
    ) -> List[Dict]:
        """
        Tìm top-k chunks tương đồng nhất với query_embedding.

        Args:
            query_embedding: vector embedding của câu hỏi user
            top_k: số kết quả tối đa
            threshold: ngưỡng similarity tối thiểu (0.35 cho 256-dim)
            content_type: filter theo loại (product_info, faq, category_info)

        Returns:
            List[{content, content_type, similarity, metadata}] sắp xếp giảm dần
        """
        self._ensure_cache()
        if not self._cache or not query_embedding:
            return []

        scored: List[Tuple[float, Dict]] = []
        for item in self._cache:
            # Filter theo content_type nếu cần
            if content_type and item["content_type"] != content_type:
                continue
            sim = cosine_similarity(query_embedding, item["vector"])
            if sim >= threshold:
                scored.append((sim, item))

        # Sắp xếp giảm dần theo similarity
        scored.sort(key=lambda x: x[0], reverse=True)

        results = []
        for sim, item in scored[:top_k]:
            results.append({
                "content": item["content"],
                "content_type": item["content_type"],
                "source_id": item["source_id"],
                "similarity": round(sim, 4),
                "metadata": item["metadata"],
            })
        return results

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
        # Tìm chunk cũ theo source
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
