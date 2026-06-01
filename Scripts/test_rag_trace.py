"""
Test end-to-end RAG flow cho cau hoi cu the.
Simulate chinh xac qua trinh: intent -> context -> Groq response
"""
import sys, re, traceback
sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()

TEST_MSG = "tôi muốn mua điện thoại tầm 20 triệu chơi gaem tốt"
print(f"=== TEST MESSAGE: '{TEST_MSG}' ===\n")

# ─── 1. Intent Detection ───
print("─── BUOC 1: Intent Detection ───")
msg = TEST_MSG.lower()
HAS_PRICE_RE = r'\d+\s*(?:triệu|trieu|tr\b|củ|cu\b|lít|lit\b|nghìn|ngàn|k\b)'
price_kws_strict = ["giá","bao nhiêu","price","cost","rẻ","đắt","tầm giá","khoảng giá",
                    "budget","tầm tiền","trong khoảng","dưới","muốn mua","cần mua"]
product_kws = ["iphone","samsung","laptop","macbook","điện thoại","phone","mua","tư vấn","tìm"]

price_re_match = re.search(HAS_PRICE_RE, msg)   
price_kw_match = any(kw in msg for kw in price_kws_strict)
product_kw_match = any(kw in msg for kw in product_kws)

print(f"  HAS_PRICE_RE match: {price_re_match.group() if price_re_match else 'None'}")
print(f"  price_kws_strict match: {next((kw for kw in price_kws_strict if kw in msg), None)}")
print(f"  product_kws match: {next((kw for kw in product_kws if kw in msg), None)}")

if price_re_match or price_kw_match:
    intent = "price_query"
elif product_kw_match:
    intent = "product_query"
else:
    intent = "general"
print(f"  => Intent: {intent}\n")

# ─── 2. Price Parsing ───
print("─── BUOC 2: Price Parsing ───")
UNIT = r'(?:triệu|trieu|tr(?![a-z])|củ|cu|lít|lit)'
RANGE_RE = r'(\d+(?:[.,]\d+)?)\s*[-–~đến tới to]+\s*(\d+(?:[.,]\d+)?)\s*' + UNIT
MILLION_RE = r'(\d+(?:[.,]\d+)?)\s*(?:triệu|trieu|tr(?![a-z])|củ|cu|lít|lit)'

range_match = re.search(RANGE_RE, msg)
mil_matches = re.findall(MILLION_RE, msg)
print(f"  RANGE_RE match: {range_match}")
print(f"  MILLION_RE matches: {mil_matches}")

prices = [float(n.replace(",",".")) * 1_000_000 for n in mil_matches]
print(f"  Prices detected: {prices}")

if prices:
    if len(prices) >= 2:
        mn, mx = min(prices), max(prices)
    else:
        mn, mx = None, prices[0] * 1.2
    print(f"  Query range: min={mn}, max={mx:,.0f}")
else:
    mn, mx = None, None
    print("  !! KHONG CO GIA NAO DUOC DETECT !!")

# ─── 3. Category Detection ───
print("\n─── BUOC 3: Category Detection ───")
CATEGORY_MAP = [
    ("di động",       ["điện thoại","phone","iphone","samsung","xiaomi","oppo","vivo","realme","di động"]),
    ("laptop",        ["laptop","máy tính xách tay","macbook","dell","asus","hp","lenovo","acer"]),
    ("máy tính bảng", ["máy tính bảng","tablet","ipad"]),
    ("phụ kiện",      ["tai nghe","airpods","sạc","ốp lưng","cáp","chuột","bàn phím","phụ kiện"]),
]
detected_cat = None
for db_kw, triggers in CATEGORY_MAP:
    matched = next((kw for kw in triggers if kw in msg), None)
    if matched:
        detected_cat = db_kw
        print(f"  Trigger '{matched}' => category: '{db_kw}'")
        break
if not detected_cat:
    print("  Khong detect duoc category")

# ─── 4. DB Query ───
print("\n─── BUOC 4: DB Query ───")
try:
    from Data.database import SessionLocal
    from Services.AI.KnowledgeService import KnowledgeService
    db = SessionLocal()
    ks = KnowledgeService(db)

    if detected_cat and (mn is not None or mx is not None):
        print(f"  get_price_range_by_category('{detected_cat}', min={mn}, max={mx:,.0f})")
        products = ks.get_price_range_by_category(detected_cat, mn, mx, 5)
        print(f"  => {len(products)} san pham")
        for p in products:
            print(f"     - {p['name']} | {p['price']:,.0f}d | {p['category']}")

    if not products and mx:
        print(f"\n  Fallback: get_price_range(min={mn}, max={mx:,.0f})")
        products = ks.get_price_range(mn, mx, 8)
        print(f"  => {len(products)} san pham")
        for p in products:
            print(f"     - {p['name']} | {p['price']:,.0f}d | {p['category']}")

    if not products:
        print("  Fallback: keyword search 'dien thoai'")
        products = ks.search_products("điện thoại", 5)
        print(f"  => {len(products)} san pham")
        for p in products:
            print(f"     - {p['name']} | {p['price']:,.0f}d")

    context_text = ks.build_product_context(products) if products else ""
    print(f"\n  Context length: {len(context_text)} chars")
    if context_text:
        print("  Context preview:")
        print("  " + context_text[:300].replace("\n", "\n  "))

    db.close()
except Exception as e:
    print(f"  !! DB ERROR: {e}")
    traceback.print_exc()

# ─── 5. Groq API Test ───
print("\n─── BUOC 5: Groq API Test ───")
try:
    import os
    from groq import Groq
    groq_key = os.getenv("GROQ_API_KEY","")
    groq_model = os.getenv("GROQ_MODEL","llama-3.3-70b-versatile")
    client = Groq(api_key=groq_key)

    if context_text:
        user_msg = (
            f"[THÔNG TIN TỪ CỬA HÀNG]\n{context_text}\n\n"
            f"[CÂU HỎI CỦA KHÁCH HÀNG]\n{TEST_MSG}\n\n"
            f"Hãy trả lời CHỈ dựa trên thông tin ở trên."
        )
    else:
        user_msg = (
            f"[THÔNG TIN TỪ CỬA HÀNG]\nKhông tìm thấy dữ liệu liên quan.\n\n"
            f"[CÂU HỎI]\n{TEST_MSG}\n\nKHÔNG có thông tin sản phẩm."
        )
    
    resp = client.chat.completions.create(
        model=groq_model,
        messages=[
            {"role": "system", "content": "Bạn là trợ lý AI của Tech Store. Trả lời ngắn gọn bằng tiếng Việt. Chỉ dùng thông tin được cung cấp."},
            {"role": "user", "content": user_msg}
        ],
        max_tokens=200,
        temperature=0.3,
    )
    answer = resp.choices[0].message.content.strip()
    print(f"  Context co du lieu: {'YES' if context_text else 'NO'}")
    print(f"  Groq response:\n  {answer}")
except Exception as e:
    print(f"  !! GROQ ERROR: {e}")
    traceback.print_exc()

print("\n=== DONE ===")
