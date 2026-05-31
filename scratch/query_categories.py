from Data.database import SessionLocal
from Models.Category import Category

db = SessionLocal()
categories = db.query(Category).all()
for c in categories:
    print(f"ID: {c.category_id}, Name: {c.name}")
db.close()
