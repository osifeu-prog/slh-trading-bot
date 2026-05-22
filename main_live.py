from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio

from api.middleware import RBACMiddleware
from api.websocket import websocket_endpoint

# Import routers
try:
    from api.auth import router as auth_router
except ImportError:
    auth_router = None

try:
    from api.admin import router as admin_router
except ImportError:
    admin_router = None

app = FastAPI(title="SLH Trading Bot - Production")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# RBAC Middleware
app.add_middleware(RBACMiddleware)

# Routers
if auth_router:
    app.include_router(auth_router, prefix="/api/auth")

if admin_router:
    app.include_router(admin_router, prefix="/api/admin")

# WebSocket
@app.websocket("/ws")
async def websocket_endpoint_handler(websocket):
    await websocket_endpoint(websocket)

@app.get("/api/system/status")
async def system_status():
    return {
        "status": "online",
        "version": "1.0",
        "message": "SLH Trading Bot is running"
    }

@app.get("/")
async def root():
    return {"message": "SLH Trading Bot API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
