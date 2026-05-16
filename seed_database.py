"""
Database Seed Script - Tao du lieu ban dau
Chay script nay mot lan de tao Admin mac dinh va Customer role
"""
from sqlalchemy.orm import Session
from Data.database import SessionLocal, init_db
from Models.Account import Account, Role, Employee
from Services.AuthService import AuthService


def seed_database():
    """Tao du lieu ban dau cho database"""
    init_db()
    db: Session = SessionLocal()

    try:
        auth_service = AuthService(db)

        # === 1. Tao Role Admin ===
        admin_role = db.query(Role).filter(Role.role_name == "Admin").first()
        if not admin_role:
            admin_role = Role(role_name="Admin")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
            print(f"  [OK] Created role: Admin (id={admin_role.role_id})")
        else:
            print(f"  [--] Role Admin already exists (id={admin_role.role_id})")

        # === 2. Tao Role Customer ===
        customer_role = db.query(Role).filter(Role.role_name == "Customer").first()
        if not customer_role:
            customer_role = Role(role_name="Customer")
            db.add(customer_role)
            db.commit()
            db.refresh(customer_role)
            print(f"  [OK] Created role: Customer (id={customer_role.role_id})")
        else:
            print(f"  [--] Role Customer already exists (id={customer_role.role_id})")

        # === 3. Tao tai khoan Admin mac dinh ===
        admin_account = db.query(Account).filter(Account.username == "admin").first()
        if not admin_account:
            admin_account = Account(
                username="admin",
                email="admin@techstore.com",
                password_hash=auth_service.hash_password("admin123"),
                full_name="Quan Tri Vien",
                phone="0909123456",
                address="Toa nha TechStore, Q.1, TP.HCM",
                role_id=admin_role.role_id,
                is_active=True
            )
            db.add(admin_account)
            db.commit()
            db.refresh(admin_account)
            print(f"  [OK] Created admin account: admin / admin123")
            print(f"        Account ID: {admin_account.account_id}")
        else:
            print(f"  [--] Admin account already exists: {admin_account.username}")

        # === 4. Tao tai khoan Customer mac dinh (test) ===
        test_customer = db.query(Account).filter(Account.username == "khachhang").first()
        if not test_customer:
            test_customer = Account(
                username="khachhang",
                email="khachhang@techstore.com",
                password_hash=auth_service.hash_password("khach123"),
                full_name="Nguyen Van Khach",
                phone="0909876543",
                address="123 Le Loi, Q.1, TP.HCM",
                role_id=customer_role.role_id,
                is_active=True
            )
            db.add(test_customer)
            db.commit()
            db.refresh(test_customer)
            print(f"  [OK] Created test customer: khachhang / khach123")
            print(f"        Account ID: {test_customer.account_id}")
        else:
            print(f"  [--] Test customer already exists: {test_customer.username}")

        print("\n[DONE] Database seeding completed successfully!")
        print("=" * 50)
        print("Admin login credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("=" * 50)
        print("Customer login credentials (test):")
        print("  Username: khachhang")
        print("  Password: khach123")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
