"""
Gemini Embedding Service — singleton, gọi Gemini API cho text embeddings.
Dùng text-embedding-004 với output_dimensionality=256 cho nhẹ & nhanh.
"""
import os
import threading
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

_embed_instance = None
_embed_lock = threading.Lock()


def get_embedding_service():
    """Lấy singleton EmbeddingService"""
    global _embed_instance
    if _embed_instance is None:
        with _embed_lock:
            if _embed_instance is None:
                _embed_instance = EmbeddingService()
    return _embed_instance


class EmbeddingService:
    """Gemini Embedding Service — 256-dim, CPU-friendly"""

    DIMENSION = 256  # Giảm từ 768 → 256 cho nhanh nhẹ

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.model = os.getenv("EMBEDDING_MODEL", "gemini-embedding-2")
        self.client = None
        self._init_client()

    def _init_client(self):
        """Khởi tạo Gemini client"""
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            print("[EmbeddingService] GEMINI_API_KEY chưa cấu hình — embeddings bị tắt")
            return
        try:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)
            print(f"[EmbeddingService] OK — model={self.model}, dim={self.DIMENSION}")
        except Exception as e:
            print(f"[EmbeddingService] Lỗi khởi tạo: {e}")
            self.client = None

    def is_available(self) -> bool:
        return self.client is not None

    def embed_text(self, text: str) -> Optional[List[float]]:
        """
        Embed 1 đoạn text (cho document/chunk).
        Lưu ý: gemini-embedding-2 KHÔNG hỗ trợ task_type — chỉ dùng output_dimensionality.
        """
        if not self.is_available() or not text.strip():
            return None
        try:
            from google.genai import types
            response = self.client.models.embed_content(
                model=self.model,
                contents=text,
                config=types.EmbedContentConfig(
                    output_dimensionality=self.DIMENSION,
                ),
            )
            return response.embeddings[0].values
        except Exception as e:
            print(f"[EmbeddingService] embed_text error: {e}")
            return None

    def embed_query(self, query: str) -> Optional[List[float]]:
        """
        Embed query từ user.
        Lưu ý: gemini-embedding-2 KHÔNG hỗ trợ task_type — chỉ dùng output_dimensionality.
        """
        if not self.is_available() or not query.strip():
            return None
        try:
            from google.genai import types
            response = self.client.models.embed_content(
                model=self.model,
                contents=query,
                config=types.EmbedContentConfig(
                    output_dimensionality=self.DIMENSION,
                ),
            )
            return response.embeddings[0].values
        except Exception as e:
            print(f"[EmbeddingService] embed_query error: {e}")
            return None

    def embed_batch(self, texts: List[str]) -> List[Optional[List[float]]]:
        """
        FIX #5: Embed nhiều text trong 1 API call (nhanh hơn cho ETL).
        Fallback về sequential nếu batch API lỗi.
        """
        if not self.is_available() or not texts:
            return [None] * len(texts)
        try:
            from google.genai import types
            # Gửi toàn bộ batch trong 1 request
            response = self.client.models.embed_content(
                model=self.model,
                contents=texts,
                config=types.EmbedContentConfig(
                    output_dimensionality=self.DIMENSION,
                ),
            )
            return [emb.values for emb in response.embeddings]
        except Exception as e:
            print(f"[EmbeddingService] embed_batch error: {e} — fallback sequential")
            # Fallback: gọi từng cái
            return [self.embed_text(t) for t in texts]
