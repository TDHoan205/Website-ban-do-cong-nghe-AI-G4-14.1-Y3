"""
Script kiểm tra API keys và dữ liệu sản phẩm trong DB.
Chạy: python Scripts/test_ai_keys.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

SEP = "=" * 55

# ─────────────── 1. GROQ API ───────────────
print(f"\n{SEP}")
print("1. KIỂM TRA GROQ API KEY")
print(SEP)
groq_key = os.getenv("GROQ_API_KEY", "")
groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

if not groq_key or groq_key == "gsk_your_key_here":
    print("❌ GROQ_API_KEY chưa được cấu hình trong .env")
else:
    print(f"   Key: {groq_key[:10]}...{groq_key[-4:]}")
    print(f"   Model: {groq_model}")
    try:
        from groq import Groq
        client = Groq(api_key=groq_key)
        resp = client.chat.completions.create(
            model=groq_model,
            messages=[{"role": "user", "content": "Chào! Trả lời ngắn: bạn là ai?"}],
            max_tokens=50,
        )
        answer = resp.choices[0].message.content.strip()
        print(f"✅ GROQ OK — Response: {answer[:80]}")
    except Exception as e:
        print(f"❌ GROQ LỖI: {e}")

# ─────────────── 2. GEMINI EMBEDDING ───────────────
print(f"\n{SEP}")
print("2. KIỂM TRA GEMINI EMBEDDING API KEY")
print(SEP)
gemini_key = os.getenv("GEMINI_API_KEY", "")
embed_model = os.getenv("EMBEDDING_MODEL", "gemini-embedding-2")

if not gemini_key or gemini_key == "your_gemini_api_key_here":
    print("❌ GEMINI_API_KEY chưa được cấu hình trong .env")
else:
    print(f"   Key: {gemini_key[:10]}...{gemini_key[-4:]}")
    print(f"   Model: {embed_model}")
    try:
        from google import genai
        from google.genai import types
        gclient = genai.Client(api_key=gemini_key)
        resp = gclient.models.embed_content(
            model=embed_model,
            contents="điện thoại samsung giá rẻ",
            config=types.EmbedContentConfig(output_dimensionality=256),
        )
        vec = resp.embeddings[0].values
        print(f"✅ GEMINI EMBEDDING OK — Vector dim: {len(vec)}, first val: {vec[0]:.4f}")
    except Exception as e:
        print(f"❌ GEMINI EMBEDDING LỖI: {e}")

# ─────────────── 3. DATABASE + PRODUCTS ───────────────
print(f"\n{SEP}")
print("3. KIỂM TRA DB — SẢN PHẨM ĐIỆN THOẠI 10-20 TRIỆU")
print(SEP)
try:
    from Data.database import SessionLocal
    from Models.Product import Product
    from Models.Category import Category
    from sqlalchemy import or_, func
    from sqlalchemy.orm import joinedload

    db = SessionLocal()

    # Đếm tổng sản phẩm
    total = db.query(Product).filter(Product.is_available == True).count()
    print(f"   Tổng sản phẩm available: {total}")

    # Tìm theo khoảng giá 10-20 triệu
    price_products = (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.is_available == True)
        .filter(Product.price >= 10_000_000)
        .filter(Product.price <= 20_000_000)
        .order_by(Product.price)
        .limit(5)
        .all()
    )
    if price_products:
        print(f"✅ Tìm thấy {len(price_products)} sản phẩm 10-20 triệu:")
        for p in price_products:
            cat = p.category.name if p.category else "?"
            print(f"   - {p.name} | {p.price:,.0f}₫ | {cat}")
    else:
        print("❌ Không có sản phẩm nào trong khoảng 10-20 triệu!")

    # Tìm theo keyword "điện thoại"
    kw_products = (
        db.query(Product)
        .filter(Product.is_available == True)
        .filter(
            or_(
                func.lower(Product.name).like("%điện thoại%"),
                func.lower(Product.name).like("%iphone%"),
                func.lower(Product.name).like("%samsung%"),
                func.lower(Product.name).like("%xiaomi%"),
                func.lower(Product.name).like("%oppo%"),
                func.lower(Product.name).like("%vivo%"),
            )
        )
        .limit(5)
        .all()
    )
    if kw_products:
        print(f"\n✅ Tìm thấy {len(kw_products)} điện thoại trong DB:")
        for p in kw_products:
            print(f"   - {p.name} | {p.price:,.0f}₫")
    else:
        print("\n❌ Không có sản phẩm điện thoại nào trong DB!")

    # Kiểm tra category "điện thoại"
    phone_cat = db.query(Category).filter(
        func.lower(Category.name).like("%điện thoại%")
    ).first()
    if phone_cat:
        print(f"\n✅ Category điện thoại: '{phone_cat.name}' (id={phone_cat.category_id})")
        cat_count = db.query(Product).filter(
            Product.category_id == phone_cat.category_id,
            Product.is_available == True
        ).count()
        print(f"   Số sản phẩm trong category này: {cat_count}")
    else:
        print("\n⚠️  Không tìm thấy category 'điện thoại' trong DB")

    db.close()
except Exception as e:
    print(f"❌ DB LỖI: {e}")
    import traceback; traceback.print_exc()

# ─────────────── 4. RAG PRICE QUERY ───────────────
print(f"\n{SEP}")
print("4. KIỂM TRA RAG PRICE DETECTION")
print(SEP)
import re
test_msgs = [
    "giúp tôi chọn điện thoại giá từ 10-20 triệu",
    "điện thoại giá từ 10-20 củ",
    "tầm 15 lít",
    "dưới 5 tr",
    "khoảng 500 nghìn",
]
MILLION_RE = r"(\d+(?:[.,]\d+)?)\s*(?:triệu|trieu|tr(?![a-z])|củ|cu|lít|lit)"
THOUSAND_RE = r"(\d+(?:[.,]\d+)?)\s*(?:nghìn|nghìn đồng|ngàn|k(?![a-z]))"
for msg in test_msgs:
    mil = re.findall(MILLION_RE, msg.lower())
    tho = re.findall(THOUSAND_RE, msg.lower())
    prices = [float(n.replace(",",".")) * 1_000_000 for n in mil] + \
             [float(n.replace(",",".")) * 1_000 for n in tho]
    status = "✅" if prices else "❌"
    print(f"   {status} '{msg}' → {prices}")

print(f"\n{SEP}\nHoàn tất kiểm tra!\n")
