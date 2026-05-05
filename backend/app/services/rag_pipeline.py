"""
RAG Pipeline Service - Retrieval Augmented Generation
Tương ứng C#: Services/RAGService.cs
"""
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.services.embedding_service import EmbeddingService


class RAGPipeline:
    """Pipeline RAG để truy xuất sản phẩm liên quan"""

    def __init__(self, db: Session):
        self.db = db
        self.embedding_service = EmbeddingService(db)
        self.embedding_service.get_all_product_embeddings()

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        return self.embedding_service.search_products(query, top_k)

    def generate_context(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        if not retrieved_docs:
            return "Không tìm thấy sản phẩm phù hợp."

        context_parts = ["Dựa trên thông tin sản phẩm trong cửa hàng:\n"]
        for i, doc in enumerate(retrieved_docs, 1):
            context_parts.append(
                f"{i}. {doc['name']} - Giá: {doc['price']:,} VNĐ"
            )
            if doc.get("category"):
                context_parts.append(f"   Danh mục: {doc['category']}")

        return "\n".join(context_parts)

    def query(self, user_query: str, top_k: int = 5) -> Dict[str, Any]:
        retrieved = self.retrieve(user_query, top_k)
        context = self.generate_context(retrieved)

        return {
            "user_query": user_query,
            "retrieved_products": retrieved,
            "context": context,
        }
