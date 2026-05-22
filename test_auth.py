from Data.database import SessionLocal
from Services.AuthService import AuthService

def test_auth():
    db = SessionLocal()
    auth_service = AuthService(db)
    
    # Get all users
    from Models.Account import Account
    users = db.query(Account).all()
    print("Users in DB:", [(u.username, u.email, u.is_active, u.role.role_name if u.role else None) for u in users])
    
    if not users:
        print("No users found in database.")
        return
        
    for user in users:
        pwd_hash = user.password_hash
        print(f"User: {user.username}, Hash: {pwd_hash}")

    db.close()

if __name__ == '__main__':
    test_auth()
