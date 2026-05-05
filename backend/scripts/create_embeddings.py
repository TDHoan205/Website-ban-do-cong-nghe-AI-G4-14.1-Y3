"""
Create Vector Embeddings for AI Chatbot
Chạy: python -m scripts.create_embeddings
"""
import sys
sys.path.insert(0, ".")

from app.core.database import SessionLocal
from app.services.embedding_service import EmbeddingService


def create_embeddings():
    print("🚀 Creating product embeddings for AI...")
    db = SessionLocal()

    try:
        embedding_service = EmbeddingService(db)
        products = embedding_service.get_all_product_embeddings()

        print(f"\n✅ Created embeddings for {len(products)} products:")
        for p in products:
            print(f"  - {p['name']} (ID: {p['product_id']})")
            print(f"    Text length: {len(p['text'])} chars")
            print(f"    Category: {p.get('category', 'N/A')}")

        print(f"\n📊 Embedding summary:")
        print(f"  Total products: {len(products)}")
        print(f"  Categories: {set(p.get('category') for p in products)}")

        print("\n✅ Embeddings ready for RAG pipeline!")

    except Exception as e:
        print(f"❌ Error creating embeddings: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_embeddings()
