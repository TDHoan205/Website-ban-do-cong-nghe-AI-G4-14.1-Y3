"""
Embedding Service - Tạo và tìm kiếm embeddings cho sản phẩm
Tương ứng C#: Services/EmbeddingService.cs
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.product import Product


class EmbeddingService:
    """Service xử lý embedding và tìm kiếm sản phẩm"""

    def __init__(self, db: Session):
        self.db = db
        self._embeddings = []

    def get_product_text(self, product: Product) -> str:
        parts = [
            f"Tên sản phẩm: {product.name}",
        ]
        if product.description:
            parts.append(f"Mô tả: {product.description}")
        if product.specifications:
            parts.append(f"Thông số kỹ thuật: {product.specifications}")
        if product.category:
            parts.append(f"Danh mục: {product.category.name}")
        if product.price:
            parts.append(f"Giá: {product.price:,} VNĐ")
        if product.supplier:
            parts.append(f"Nhà cung cấp: {product.supplier.name}")

        for variant in product.variants:
            variant_info = []
            if variant.color:
                variant_info.append(f"Màu: {variant.color}")
            if variant.storage:
                variant_info.append(f"Bộ nhớ: {variant.storage}")
            if variant.ram:
                variant_info.append(f"RAM: {variant.ram}")
            if variant_info:
                parts.append(f"Phiên bản ({', '.join(variant_info)}): Giá {variant.price:,} VNĐ")

        return ". ".join(parts)

    def get_all_product_embeddings(self) -> List[Dict[str, Any]]:
        products = self.db.query(Product).filter(Product.is_available == True).all()
        self._embeddings = []

        for product in products:
            self._embeddings.append({
                "product_id": product.product_id,
                "name": product.name,
                "text": self.get_product_text(product),
                "price": product.price,
                "image_url": product.image_url,
                "category": product.category.name if product.category else None,
            })

        return self._embeddings

    def search_products(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not self._embeddings:
            self.get_all_product_embeddings()

        query_lower = query.lower()
        results = []

        for emb in self._embeddings:
            score = 0
            query_words = query_lower.split()

            for word in query_words:
                if word in emb["name"].lower():
                    score += 10
                if word in emb["text"].lower():
                    score += 3
                if emb.get("category") and word in emb["category"].lower():
                    score += 5

            if score > 0:
                results.append({**emb, "relevance_score": score})

        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:top_k]
