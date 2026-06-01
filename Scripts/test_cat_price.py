"""Test end-to-end price query voi RAGEngine keyword"""
import sys; sys.path.insert(0, '.')
from dotenv import load_dotenv; load_dotenv()
from Data.database import SessionLocal
from Services.AI.KnowledgeService import KnowledgeService

db = SessionLocal()
ks = KnowledgeService(db)

# Day la keyword chinh xac ma RAGEngine se truyen vao sau fix
print("=== RAGEngine se dung keyword: 'di \u0111\u1ed9ng' ===")
r = ks.get_price_range_by_category("di \u0111\u1ed9ng", 10_000_000, 20_000_000)
print(f"=> {len(r)} san pham dien thoai 10-20tr")
for x in r:
    print(f"  + {x['name']} | {x['price']:,.0f}d")

print()
print("=== Fallback (tat ca san pham 10-20tr) ===")
r2 = ks.get_price_range(10_000_000, 20_000_000, 8)
print(f"=> {len(r2)} san pham")
for x in r2:
    print(f"  - {x['name']} | {x['price']:,.0f}d | {x['category']}")

db.close()
print("\n=> Ket luan: Neu 'di dong' co 4 ket qua, pipeline hoat dong dung!")
