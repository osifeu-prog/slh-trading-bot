from fastapi import APIRouter
import subprocess

router = APIRouter(prefix="/api/docker", tags=["docker"])

@router.get("/status")
def docker_status():
    try:
        subprocess.run(["docker", "ps"], capture_output=True, check=True)
        return {"status": "running"}
    except:
        return {"status": "stopped"}

@router.post("/restart")
def restart_container():
    try:
        subprocess.run(["docker-compose", "restart"], cwd=r"C:\Users\USER\Desktop\SLH\algo-bot", capture_output=True)
        return {"status": "restarting"}
    except Exception as e:
        return {"error": str(e)}

@router.get("/logs")
def docker_logs(tail: int = 20):
    try:
        output = subprocess.check_output(["docker", "logs", "--tail", str(tail), "slh_bot"]).decode()
        return {"logs": output.splitlines()}
    except Exception as e:
        return {"error": str(e)}
