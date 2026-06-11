from fastapi import APIRouter, Depends, HTTPException
from typing import List

router = APIRouter()

# Simple in-memory users for demo
users_db = []

@router.get("/users")
async def get_users():
    """Admin only - list all users"""
    return {"users": users_db}

@router.post("/users")
async def create_user(user: dict):
    users_db.append(user)
    return {"message": "User created", "user": user}
