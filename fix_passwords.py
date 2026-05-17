from Data.database import SessionLocal
from Services.AuthService import AuthService
from Models.Account import Account

def update_passwords():
    db = SessionLocal()
    auth_service = AuthService(db)
    
    users = db.query(Account).all()
    for user in users:
        # Neu password chua duoc ma hoa bang bcrypt (khong bat dau bang $2)
        if not user.password_hash.startswith('$2'):
            # Set default password la '123456'
            new_hash = auth_service.hash_password('123456')
            user.password_hash = new_hash
            print(f"Updated password for {user.username} to '123456'")
            
    db.commit()
    print("All passwords updated successfully.")
    db.close()

if __name__ == '__main__':
    update_passwords()
