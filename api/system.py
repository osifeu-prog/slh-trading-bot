from fastapi import APIRouter
import os, json, time

router = APIRouter(prefix="/api/system", tags=["system"])

HEARTBEAT_FILE = "logs/heartbeat.txt"

@router.get("/status")
def system_status():
    docker_ok = False
    binance_ok = False
    try:
        if os.path.exists(HEARTBEAT_FILE):
            with open(HEARTBEAT_FILE) as f:
                content = f.read().strip()
            if content.startswith("{"):
                hb = json.loads(content)
                last_time = time.mktime(time.strptime(hb["timestamp"][:19], "%Y-%m-%dT%H:%M:%S"))
                age = time.time() - last_time
            else:
                last_unix = float(content)
                age = time.time() - last_unix
            if age < 120:
                docker_ok = True
                binance_ok = True
    except:
        pass

    return {
        "bot": "SLH Trading Bot",
        "docker": "running" if docker_ok else "unknown",
        "binance_ws": "connected" if binance_ok else "unknown",
        "dashboard": "http://localhost:8080"
    }
