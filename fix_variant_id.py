"""Fix: Add variant_id column and FK to ProductImages if missing"""
from Data.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Check if column exists
    result = conn.execute(text(
        "SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('ProductImages') AND name = 'variant_id'"
    ))
    if result.fetchone():
        print("variant_id column already exists in ProductImages")
        # Check if FK constraint exists
        fk = conn.execute(text(
            "SELECT 1 FROM sys.foreign_keys WHERE name = 'FK_ProductImages_Variants'"
        ))
        if fk.fetchone():
            print("FK_ProductImages_Variants constraint already exists")
        else:
            conn.execute(text(
                "ALTER TABLE ProductImages ADD CONSTRAINT FK_ProductImages_Variants "
                "FOREIGN KEY (variant_id) REFERENCES ProductVariants(variant_id) ON DELETE NO ACTION"
            ))
            conn.commit()
            print("SUCCESS: Added FK constraint on variant_id")
    else:
        conn.execute(text(
            "ALTER TABLE ProductImages ADD variant_id INT NULL"
        ))
        conn.execute(text(
            "ALTER TABLE ProductImages ADD CONSTRAINT FK_ProductImages_Variants "
            "FOREIGN KEY (variant_id) REFERENCES ProductVariants(variant_id) ON DELETE NO ACTION"
        ))
        conn.commit()
        print("SUCCESS: Added variant_id column and FK constraint to ProductImages table")
