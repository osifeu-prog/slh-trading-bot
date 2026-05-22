from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt, os
from core.rbac_engine import AccessControl

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "slh-dev-secret-change-me")
ALGORITHM = "HS256"
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(role: str):
    def role_checker(user = Depends(get_current_user)):
        if user.get("role") != role and user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Insufficient role")
        return user
    return role_checker

def authorize_action(action: str):
    def checker(user = Depends(get_current_user)):
        ac = AccessControl(user.get("role", "viewer"))
        ok, reason = ac.authorize(action)
        if not ok:
            raise HTTPException(status_code=403, detail=reason)
        return user
    return checker
