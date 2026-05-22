from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, threading
from api.system import router as system_router
from api.docker import router as docker_router
from api.trades import router as trades_router
from api.ai import router as ai_router
from api.auth import router as auth_router
from api.admin import router as admin_router

app = FastAPI(title="SLH Trading Bot Control API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(system_router)
app.include_router(docker_router)
app.include_router(trades_router)
app.include_router(ai_router)
app.include_router(auth_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"status": "running", "bot": "SLH"}

def start_dashboard(port=8080):
    def run():
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    t = threading.Thread(target=run, daemon=True)
    t.start()
    print(f"Full API (auth, admin, system, trades) on http://localhost:{port}")
