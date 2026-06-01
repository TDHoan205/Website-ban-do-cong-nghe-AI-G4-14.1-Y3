"""
Migration script: Đồng nhất đường dẫn ảnh sản phẩm về /static/images/products/

Vấn đề: Hệ thống đang lưu 2 dạng đường dẫn:
  - /static/uploads/products/{guid}.ext   (từ Admin upload mới)
  - /images/products/{name}.{ext}         (từ seed cũ, hoặc /static/images/products/)

Sau khi chạy script này:
  - File vật lý từ wwwroot/uploads/products/ → di chuyển sang wwwroot/images/products/
  - DB image_url từ /static/uploads/products/ → sửa thành /static/images/products/
  - File cũ trong wwwroot/images/products/ giữ nguyên
  - _normalize_image_url() cập nhật để hỗ trợ /static/uploads/products/ (backward compat)

Chạy: python migrate_image_paths.py
"""
import os
import shutil
import sys

# Add parent dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Data.database import SessionLocal, engine
from sqlalchemy import text


def migrate():
    print("=" * 60)
    print("MIGRATE IMAGE PATHS - Tech Store AI")
    print("=" * 60)

    db = SessionLocal()

    # ── 1. Move physical files ──────────────────────────────────────────
    src_dir = os.path.join("wwwroot", "uploads", "products")
    dst_dir = os.path.join("wwwroot", "images", "products")
    os.makedirs(dst_dir, exist_ok=True)

    moved_files = 0
    skipped_files = 0
    if os.path.isdir(src_dir):
        for filename in os.listdir(src_dir):
            src_path = os.path.join(src_dir, filename)
            dst_path = os.path.join(dst_dir, filename)
            if os.path.isfile(src_path):
                if os.path.exists(dst_path):
                    # File đã tồn tại ở đích → bỏ qua
                    skipped_files += 1
                    print(f"  [SKIP] {filename} (đã tồn tại ở {dst_dir})")
                else:
                    shutil.move(src_path, dst_path)
                    moved_files += 1
                    print(f"  [MOVE] {filename}")
        # Xóa thư mục rỗng
        try:
            os.rmdir(src_dir)
            print(f"  [RM DIR] {src_dir} (đã rỗng)")
        except OSError:
            pass

    print(f"\n  Đã di chuyển: {moved_files} file")
    print(f"  Đã bỏ qua:    {skipped_files} file")

    # ── 2. Update DB: Products.image_url ───────────────────────────────
    updates_products = [
        # /static/uploads/... → /static/images/...
        ("Products", "image_url", "/static/uploads/products/", "/static/images/products/"),
        # /images/... → /static/images/...
        ("Products", "image_url", "/images/products/", "/static/images/products/"),
    ]
    for table, col, old_prefix, new_prefix in updates_products:
        sql = text(f"""
            UPDATE {table}
            SET {col} = REPLACE({col}, :old, :new)
            WHERE {col} LIKE :pattern
        """)
        result = db.execute(sql, {
            "old": old_prefix,
            "new": new_prefix,
            "pattern": old_prefix + "%"
        })
        rowcount = result.rowcount
        print(f"  [{table}.{col}] {old_prefix!r} → {new_prefix!r}: {rowcount} rows updated")

    # ── 3. Update DB: ProductImages.image_url ──────────────────────────
    updates_product_images = [
        ("ProductImages", "image_url", "/static/uploads/products/", "/static/images/products/"),
        ("ProductImages", "image_url", "/images/products/", "/static/images/products/"),
    ]
    for table, col, old_prefix, new_prefix in updates_product_images:
        sql = text(f"""
            UPDATE {table}
            SET {col} = REPLACE({col}, :old, :new)
            WHERE {col} LIKE :pattern
        """)
        result = db.execute(sql, {
            "old": old_prefix,
            "new": new_prefix,
            "pattern": old_prefix + "%"
        })
        rowcount = result.rowcount
        print(f"  [{table}.{col}] {old_prefix!r} → {new_prefix!r}: {rowcount} rows updated")

    db.commit()
    print("\n  ✓ Database updated!")

    # ── 4. Preview sample rows ────────────────────────────────────────
    print("\n── Sample Products.image_url after migration ──")
    rows = db.execute(text("SELECT TOP 10 product_id, name, image_url FROM Products WHERE image_url IS NOT NULL")).fetchall()
    for r in rows:
        print(f"  [{r[0]}] {r[1][:40]:<40} → {r[2]}")

    print("\n── Sample ProductImages.image_url after migration ──")
    rows2 = db.execute(text("SELECT TOP 10 image_id, product_id, image_url FROM ProductImages WHERE image_url IS NOT NULL")).fetchall()
    for r in rows2:
        print(f"  [{r[0]}] prod={r[1]} → {r[2]}")

    db.close()
    print("\n✓ Migration hoàn tất!")


if __name__ == "__main__":
    migrate()
