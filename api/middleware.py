from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
import os

async def get_current_user_permissions(token: str):
    try:
        secret = os.getenv("JWT_SECRET_KEY", "your-secret-key")
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        role = payload.get("role", "viewer")
        email = payload.get("sub", "")
        
        # FORCE ADMIN FOR TESTING
        if email == "realadmin@slh.com":
            role = "admin"
        
        role_permissions = {
            "admin": ["admin:read", "admin:write", "trade:read", "trade:write", "system:read", "ai:read"],
            "trader": ["trade:read", "trade:write", "system:read"],
            "viewer": ["trade:read", "system:read"]
        }
        return role_permissions.get(role, [])
    except:
        return []

class RBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path.startswith(p) for p in ["/api/auth/login", "/api/auth/register", "/api/system/status"]):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid token"})

        token = auth_header.split(" ")[1]
        permissions = await get_current_user_permissions(token)

        if path.startswith("/api/admin"):
            if "admin:read" not in permissions:
                return JSONResponse(status_code=403, content={"detail": "Admin access required"})
        
        return await call_next(request)
