import os, time, json, requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, timezone

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HEARTBEAT_FILE = r"C:\Users\USER\Desktop\SLH\algo-bot\logs\heartbeat.txt"
LOCK_FILE = r"C:\Users\USER\Desktop\SLH\algo-bot\logs\main_telegram.lock"

def acquire_lock():
    if os.path.exists(LOCK_FILE):
        print("Another Main Telegram listener is already running. Exiting.")
        return False
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))
    return True

def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = ("SLH Trading Bot Commands:\n"
           "/start - This menu\n"
           "/status - Bot status\n"
           "/pnl - Approx PnL\n"
           "/positions - Open positions\n"
           "/help - This menu")
    await update.message.reply_text(msg)

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await cmd_start(update, context)

async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    alive = False
    if os.path.exists(HEARTBEAT_FILE):
        with open(HEARTBEAT_FILE) as f:
            content = f.read().strip()
        if content.startswith("{"):
            hb = json.loads(content)
            last_time = datetime.fromisoformat(hb["timestamp"])
            alive = (datetime.now(timezone.utc) - last_time).total_seconds() < 120
        else:
            last_unix = float(content)
            alive = (time.time() - last_unix) < 120
    status = "Active" if alive else "Stale"
    await update.message.reply_text(f"Status: {status}")

if __name__ == "__main__":
    if not acquire_lock():
        exit()
    requests.post(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler(["start", "help"], cmd_start))
    app.add_handler(CommandHandler("status", cmd_status))
    print("Main bot Telegram listener started (commands: /start, /help, /status)")
    try:
        app.run_polling(drop_pending_updates=True)
    finally:
        release_lock()
