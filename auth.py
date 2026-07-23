from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db,engine
from models import Admin
from schemas import AdminLogin
from sqlalchemy import func
from security import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================
# REGISTER ADMIN
# ==========================
@router.post("/register")
def register(
    admin: AdminLogin,
    db: Session = Depends(get_db)
):
    print("REGISTER DB:", engine.url)

    existing = db.query(Admin).filter(
        Admin.username == admin.username
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_admin = Admin(
        username=admin.username,
        password=hash_password(admin.password)
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    
    print(admin.username)
    print(admin.password)
    return {
        "message": "Admin registered successfully"
    }
    


# ==========================
# LOGIN
# ==========================
@router.post("/login")
def login(
    data: AdminLogin,
    db: Session = Depends(get_db)
):
    print("LOGIN DB:", engine.url)
    print("Username received:", repr(data.username))

    user = db.query(Admin).filter(
        func.lower(Admin.username) == data.username.strip().lower()
    ).first()

    print("User found:", user)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        data.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }