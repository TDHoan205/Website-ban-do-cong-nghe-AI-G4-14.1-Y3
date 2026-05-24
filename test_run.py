# Test database connection and basic imports
import sys
sys.path.insert(0, r'd:\a_LTPY\BTLPYTHON\Website-ban-do-cong-nghe-AI-G4-14.1-Y3')

print("Testing imports...")
try:
    from Data.database import engine, SessionLocal, get_connection_info
    print("OK: database.py imported")
except Exception as e:
    print(f"FAIL: database.py - {e}")

try:
    from Controllers import HomeController, ProductsController, AuthController
    print("OK: Controllers imported")
except Exception as e:
    print(f"FAIL: Controllers - {e}")

try:
    from Services import AuthService, ProductService, CartService
    print("OK: Services imported")
except Exception as e:
    print(f"FAIL: Services - {e}")

try:
    from Models import Account, Product, Order
    print("OK: Models imported")
except Exception as e:
    print(f"FAIL: Models - {e}")

print("\nTesting DB connection...")
try:
    from sqlalchemy import text
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("OK: DB connection works!")
except Exception as e:
    print(f"FAIL: DB connection - {e}")

print("\nChecking accounts in DB...")
try:
    db = SessionLocal()
    from Models import Account
    accounts = db.query(Account).all()
    print(f"OK: Found {len(accounts)} accounts")
    for a in accounts:
        print(f"  - {a.username} (role_id={a.role_id})")
    db.close()
except Exception as e:
    print(f"FAIL: Query accounts - {e}")

print("\nAll tests done!")
