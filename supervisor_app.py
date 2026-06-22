import os, time, requests, logging

logging.basicConfig(level=logging.INFO)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send(msg):
    try:
        if TOKEN and CHAT_ID:
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}", timeout=5)
    except Exception as e:
        logging.error(f"Telegram send failed: {e}")

logging.info("Supervisor starting...")
if not TOKEN:
    logging.error("TELEGRAM_BOT_TOKEN not set!")
else:
    send("Supervisor started")
    while True:
        try:
            r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getUpdates", timeout=10)
            time.sleep(5)
        except Exception as e:
            logging.error(f"Error: {e}")
            time.sleep(15)
