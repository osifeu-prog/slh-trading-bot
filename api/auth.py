from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import jwt
import os
from datetime import datetime, timedelta

router = APIRouter()

class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str = ""
    role: str = "viewer"   # <-- important

class UserLogin(BaseModel):
    email: str
    password: str

# Simple in-memory users for now (replace with real DB later)
users_db = {}

@router.post("/register")
async def register(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(400, "Email already exists")
    
    users_db[user.email] = {
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,          # <-- Save the role!
        "password": user.password   # In production use hash!
    }
    
    return {"message": "User registered", "user_id": user.email}

@router.post("/login")
async def login(credentials: UserLogin):
    user = users_db.get(credentials.email)
    if not user or user["password"] != credentials.password:
        raise HTTPException(401, "Invalid credentials")
    
    # Create token with REAL role
    secret = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    token = jwt.encode({
        "sub": user["email"],
        "role": user["role"],           # <-- This was missing
        "exp": datetime.utcnow() + timedelta(hours=24)
    }, secret, algorithm="HS256")
    
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}
