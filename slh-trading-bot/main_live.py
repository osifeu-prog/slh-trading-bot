from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.middleware import RBACMiddleware
from api.websocket import websocket_endpoint

app = FastAPI(title="SLH Trading Bot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RBACMiddleware)

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket_endpoint(websocket)

@app.get("/api/system/status")
async def status():
    return {"status": "online", "version": "1.0"}

# נתיב מוגן זמני לבדיקת RBAC
@app.get("/api/admin/test-rbac")
async def test_rbac():
    return {"message": "If you see this, RBAC is NOT working!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
