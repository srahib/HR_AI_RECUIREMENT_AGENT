from database import SessionLocal
from models import Admin

db = SessionLocal()

users = db.query(Admin).all()

for u in users:
    print("Username:", u.username)
    print("Password:", u.password)