from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
import os

# פונקציה זמנית לקבלת הרשאות – יש להחליף בקריאה אמיתית ל-RBAC Engine
async def get_current_user_permissions(token: str):
    try:
        secret = os.getenv("JWT_SECRET_KEY", "your-secret-key")
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload.get("permissions", [])
    except:
        return []

class RBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        
        # נתיבים ציבוריים
        public_paths = ["/api/auth/login", "/api/auth/register", "/api/system/status"]
        if any(path.startswith(p) for p in public_paths):
            return await call_next(request)
        
        # בדיקת JWT
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid token"})
        
        token = auth_header.split(" ")[1]
        permissions = await get_current_user_permissions(token)
        
        # הרשאות לפי נתיב
        if path.startswith("/api/admin"):
            if "admin:read" not in permissions:
                return JSONResponse(status_code=403, content={"detail": "Admin access required"})
        elif path.startswith("/api/trades"):
            if "trade:read" not in permissions:
                return JSONResponse(status_code=403, content={"detail": "Trader access required"})
        elif path.startswith("/api/system"):
            if "system:read" not in permissions and "admin:read" not in permissions:
                return JSONResponse(status_code=403, content={"detail": "System access required"})
        elif path.startswith("/api/ai"):
            if "ai:read" not in permissions and "viewer:read" not in permissions:
                return JSONResponse(status_code=403, content={"detail": "AI access required"})
        
        response = await call_next(request)
        return response
