from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse
from core.auth import decode_access_token

EXCLUDED_PATHS = [
    "/ws",
    "/api/system/status",
    "/docs",
    "/openapi.json",
    "/redoc",
]

class RBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # עקוף WebSocket ונתיבים ציבוריים
        if request.url.path in EXCLUDED_PATHS or request.url.path.startswith("/ws"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid token"})

        token = auth_header.split(" ")[1]
        try:
            payload = decode_access_token(token)
            request.state.user = payload
        except Exception:
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

        return await call_next(request)
