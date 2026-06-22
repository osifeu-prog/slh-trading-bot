import os, time, logging, requests, subprocess

logging.basicConfig(level=logging.INFO, format="%(asctime)s [WATCHDOG] %(message)s")
logger = logging.getLogger("watchdog")

CHECK_INTERVAL = 60  # seconds

def check_http(url, label):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            logger.info(f"{label} OK ({url})")
            return True
        else:
            logger.warning(f"{label} returned {r.status_code}")
            return False
    except Exception as e:
        logger.error(f"{label} FAILED: {e}")
        return False

def check_trader():
    # check shared data freshness
    try:
        with open("/shared_data/last_price.json", "r") as f:
            data = f.read()
            if "BTCUSDT" in data:
                logger.info("Trader OK (shared_data present)")
                return True
    except Exception as e:
        logger.error(f"Trader data missing: {e}")
    return False

def check_docker_container(name):
    try:
        out = subprocess.check_output(["docker", "ps", "--filter", f"name={name}", "--format", "{{.Status}}"], text=True)
        if "Up" in out:
            logger.info(f"Docker {name} OK")
            return True
        else:
            logger.warning(f"Docker {name} not running: {out}")
    except Exception as e:
        logger.error(f"Docker check {name} failed: {e}")
    return False

def restart_service(service):
    logger.warning(f"Restarting {service}...")
    subprocess.run(["docker", "compose", "restart", service], cwd="/app")

if __name__ == "__main__":
    logger.info("Watchdog started")
    while True:
        # Local checks
        check_http("http://localhost:8080/health", "Local API")
        check_trader()
        check_http("http://localhost:3000", "Frontend")
        check_docker_container("slh_supervisor")
        # Optional Render check (uncomment if needed)
        # check_http("https://slh-trading-bot.onrender.com/health", "Render")
        time.sleep(CHECK_INTERVAL)
