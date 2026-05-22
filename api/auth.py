import os, jwt, bcrypt, json
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["auth"])

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "slh-dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 30

USERS_FILE = "config/users.json"

security = HTTPBearer()

# --- Models ---
class UserRegister(BaseModel):
    email: str
    password: str
    full_name: str = ""

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Helpers ---
def load_users():
    if not os.path.exists(USERS_FILE):
        os.makedirs("config", exist_ok=True)
        default = {"users": [{"id": "admin", "role": "admin", "email": "admin@slh.local", "password_hash": bcrypt.hashpw("admin".encode(), bcrypt.gensalt()).decode()}]}
        with open(USERS_FILE, "w") as f:
            json.dump(default, f, indent=2)
    with open(USERS_FILE) as f:
        return json.load(f)

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def create_token(user_id, role):
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# --- Routes ---
@router.post("/register")
def register(user: UserRegister):
    data = load_users()
    if any(u["email"] == user.email for u in data["users"]):
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
    new_user = {"id": user.email.split("@")[0], "role": "viewer", "email": user.email, "password_hash": hashed, "full_name": user.full_name}
    data["users"].append(new_user)
    save_users(data)
    return {"message": "User registered", "user_id": new_user["id"]}

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    data = load_users()
    u = next((u for u in data["users"] if u["email"] == user.email), None)
    if not u or not bcrypt.checkpw(user.password.encode(), u["password_hash"].encode()):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(u["id"], u["role"])
    return TokenResponse(access_token=token)

@router.get("/me")
def me(user = Depends(get_current_user)):
    return {"user_id": user["sub"], "role": user["role"]}
