"""
ETL Script — Seed embeddings cho Products, Categories, FAQs.
Chạy: python Scripts/seed_embeddings.py
Idempotent: xóa chunks cũ rồi tạo mới.
"""
import sys
import os
import time

# Thêm project root vào path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from Data.database import SessionLocal
from Models.Product import Product
from Models.Category import Category
from Models.Chat import FAQ
from Services.AI.EmbeddingService import get_embedding_service
from Services.AI.VectorStore import VectorStore
from sqlalchemy.orm import joinedload
import json


def build_product_chunk(product: Product) -> str:
    """Chuyển Product → text chunk cho embedding"""
    parts = [f"Sản phẩm: {product.name}"]

    if product.category:
        parts.append(f"Danh mục: {product.category.name}")

    if product.price:
        parts.append(f"Giá: {float(product.price):,.0f}₫")
    if product.original_price and product.original_price > product.price:
        parts.append(f"Giá gốc: {float(product.original_price):,.0f}₫")
    if product.discount_percent and product.discount_percent > 0:
        parts.append(f"Giảm {product.discount_percent}%")

    if product.description:
        desc = product.description[:200]
        parts.append(f"Mô tả: {desc}")

    if product.specifications:
        try:
            specs = json.loads(product.specifications)
            if isinstance(specs, dict):
                spec_str = ", ".join(f"{k}: {v}" for k, v in list(specs.items())[:6])
                parts.append(f"Thông số: {spec_str}")
        except (json.JSONDecodeError, TypeError):
            pass

    tags = []
    if product.is_hot:
        tags.append("HOT")
    if product.is_new:
        tags.append("Mới")
    if tags:
        parts.append(f"Tags: {', '.join(tags)}")

    if product.stock_quantity is not None:
        parts.append("Còn hàng" if product.stock_quantity > 0 else "Hết hàng")

    return " | ".join(parts)


def build_category_chunk(cat: Category) -> str:
    """Chuyển Category → text chunk"""
    text = f"Danh mục sản phẩm: {cat.name}"
    if cat.description:
        text += f" - {cat.description}"
    return text


def build_faq_chunk(faq: FAQ) -> str:
    """Chuyển FAQ → text chunk"""
    return f"Câu hỏi: {faq.question}\nTrả lời: {faq.answer}"


def seed():
    """Chạy ETL: tạo chunks + embeddings"""
    embed_svc = get_embedding_service()
    if not embed_svc.is_available():
        print("❌ EmbeddingService không khả dụng. Kiểm tra GEMINI_API_KEY trong .env")
        return

    db = SessionLocal()
    store = VectorStore(db)

    try:
        # ═══════════ PRODUCTS ═══════════
        print("\n📦 Đang xử lý Products...")
        products = (
            db.query(Product)
            .options(joinedload(Product.category))
            .filter(Product.is_available == True)
            .all()
        )
        print(f"   Tìm thấy {len(products)} sản phẩm")

        store.delete_by_source("Products")
        success = 0
        for i, p in enumerate(products):
            chunk_text = build_product_chunk(p)
            vec = embed_svc.embed_text(chunk_text)
            if vec:
                store.upsert_chunk(
                    content=chunk_text,
                    content_type="product_info",
                    source_id=p.product_id,
                    source_table="Products",
                    embedding=vec,
                    metadata={"name": p.name, "price": float(p.price) if p.price else 0},
                )
                success += 1
            # Rate limit: tránh 429 từ Gemini free tier
            if (i + 1) % 10 == 0:
                time.sleep(1)
                print(f"   ... {i + 1}/{len(products)}")
        db.commit()
        print(f"   ✅ {success}/{len(products)} products embedded")

        # ═══════════ CATEGORIES ═══════════
        print("\n📂 Đang xử lý Categories...")
        categories = db.query(Category).filter(Category.is_active == True).all()
        print(f"   Tìm thấy {len(categories)} danh mục")

        store.delete_by_source("Categories")
        success = 0
        for cat in categories:
            chunk_text = build_category_chunk(cat)
            vec = embed_svc.embed_text(chunk_text)
            if vec:
                store.upsert_chunk(
                    content=chunk_text,
                    content_type="category_info",
                    source_id=cat.category_id,
                    source_table="Categories",
                    embedding=vec,
                    metadata={"name": cat.name},
                )
                success += 1
        db.commit()
        print(f"   ✅ {success}/{len(categories)} categories embedded")

        # ═══════════ FAQs ═══════════
        print("\n❓ Đang xử lý FAQs...")
        faqs = db.query(FAQ).filter(FAQ.is_active == True).all()
        print(f"   Tìm thấy {len(faqs)} FAQs")

        if faqs:
            store.delete_by_source("FAQs")
            success = 0
            for faq in faqs:
                chunk_text = build_faq_chunk(faq)
                vec = embed_svc.embed_text(chunk_text)
                if vec:
                    store.upsert_chunk(
                        content=chunk_text,
                        content_type="faq",
                        source_id=faq.faq_id,
                        source_table="FAQs",
                        embedding=vec,
                        metadata={"question": faq.question[:100]},
                    )
                    success += 1
            db.commit()
            print(f"   ✅ {success}/{len(faqs)} FAQs embedded")
        else:
            print("   ⏭️ Không có FAQs, bỏ qua")

        # ═══════════ KẾT QUẢ ═══════════
        total = store.get_chunk_count()
        print(f"\n{'='*50}")
        print(f"🎉 ETL hoàn tất! Tổng: {total} chunks có embedding trong DB")
        print(f"{'='*50}")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Lỗi ETL: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("🚀 SEED EMBEDDINGS — Tech Store RAG")
    print("=" * 50)
    seed()
