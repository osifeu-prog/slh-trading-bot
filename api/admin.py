from fastapi import APIRouter, Depends, HTTPException
from api.middleware import get_current_user, require_role
from core.rbac_engine import load_users, save_users, add_user
from pydantic import BaseModel

router = APIRouter(prefix="/api/admin", tags=["admin"])

class UserCreate(BaseModel):
    email: str
    password: str
    role: str = "viewer"

@router.get("/users")
def list_users(user = Depends(require_role("admin"))):
    data = load_users()
    return data["users"]

@router.post("/users")
def create_user(new_user: UserCreate, user = Depends(require_role("admin"))):
    import bcrypt
    data = load_users()
    if any(u["email"] == new_user.email for u in data["users"]):
        raise HTTPException(status_code=400, detail="User exists")
    hashed = bcrypt.hashpw(new_user.password.encode(), bcrypt.gensalt()).decode()
    add_user(new_user.email, new_user.role, hashed)
    return {"status": "created", "email": new_user.email}
