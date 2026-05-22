import os, time, requests, subprocess, threading, json
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import Conflict

load_dotenv()
TOKEN = os.getenv("SUPERVISOR_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HEARTBEAT_FILE = r"C:\Users\USER\Desktop\SLH\algo-bot\logs\heartbeat.txt"
AGENTS_FILE = r"C:\Users\USER\Desktop\SLH\algo-bot\agents.json"
JOURNAL_FILE = r"C:\Users\USER\Desktop\SLH\SLH_JOURNAL.md"
LOCK_FILE = r"C:\Users\USER\Desktop\SLH\algo-bot\logs\supervisor.lock"
TASKS_FILE = r"C:\Users\USER\Desktop\SLH\algo-bot\TASKS.md"
CHANNEL_INVITE = "https://t.me/+37XWeJ87enw4YjJk"

def acquire_lock():
    if os.path.exists(LOCK_FILE):
        print("Another supervisor instance is already running. Exiting.")
        return False
    with open(LOCK_FILE, "w") as f:
        f.write(str(os.getpid()))
    return True

def release_lock():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

def check_docker():
    try: subprocess.run(["docker", "ps"], capture_output=True, check=True); return True
    except: return False

def check_binance_ws():
    try:
        with open(HEARTBEAT_FILE) as f:
            content = f.read().strip()
        if content.startswith("{"):
            hb = json.loads(content)
            from datetime import datetime
            last_time = datetime.fromisoformat(hb["timestamp"])
            age = (datetime.utcnow() - last_time).total_seconds()
        else:
            last_unix = float(content)
            age = time.time() - last_unix
        return age < 120
    except:
        return False

def send_telegram(text):
    if not CHAT_ID: return
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                  json={"chat_id": CHAT_ID, "text": text})

class SupervisorBot:
    def __init__(self, token, chat_id):
        self.token, self.chat_id = token, chat_id

    async def start_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        await update.message.reply_text(
            f"Welcome! Your ID: `{uid}`\nJoin: {CHANNEL_INVITE}", parse_mode="Markdown")

    async def myid_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        uid = update.effective_user.id
        await update.message.reply_text(f"Your ID: `{uid}`", parse_mode="Markdown")

    async def health_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        d, ws = check_docker(), check_binance_ws()
        await update.message.reply_text(f"Docker: {'OK' if d else 'DOWN'}\nBinance WS: {'OK' if ws else 'DISCONNECTED'}")

    async def menu_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        msg = "Commands:\n/start - Welcome & ID\n/myid - Your ID\n/health - System health\n/restart - Restart bot\n/logs - Last 10 log lines\n/wake - Agent status\n/task - Assign task\n/tasks - View full task list\n/menu - This menu"
        await update.message.reply_text(msg)

    async def tasks_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            with open(TASKS_FILE, "r") as f:
                tasks = f.read()
            await update.message.reply_text(tasks[:4000])
        except:
            await update.message.reply_text("Could not read TASKS.md")

    async def restart_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        subprocess.run(["docker-compose", "restart"], cwd=r"C:\Users\USER\Desktop\SLH\algo-bot")
        await update.message.reply_text("Restarting...")

    async def logs_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            out = subprocess.check_output(["docker", "logs", "--tail", "10", "slh_bot"]).decode()
            await update.message.reply_text(out[:4000])
        except: await update.message.reply_text("Failed to get logs.")

    async def wake_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            with open(AGENTS_FILE) as f: data = json.load(f)
            msg = "Agent Status:\n"
            for a in data["agents"]:
                msg += f"{a['id']} ({a['role']}): {a['status']}\n"
            await update.message.reply_text(msg)
        except: await update.message.reply_text("Could not read agents.json")

    async def task_cmd(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            args = context.args
            if len(args) < 2:
                await update.message.reply_text("Usage: /task <agent_id> <task description>")
                return
            agent_id = args[0]
            task_desc = " ".join(args[1:])
            from datetime import datetime
            timestamp = datetime.utcnow().isoformat()
            entry = f"\n## {timestamp}\n**Agent:** {agent_id}\n**Task:** {task_desc}\n**Status:** assigned\n"
            with open(JOURNAL_FILE, "a") as f:
                f.write(entry)
            await update.message.reply_text(f"Task assigned to {agent_id}: {task_desc}")
        except Exception as e:
            await update.message.reply_text(f"Error: {e}")

    def start(self):
        if not self.token: return
        if not acquire_lock(): return
        requests.post(f"https://api.telegram.org/bot{self.token}/deleteWebhook")
        app = Application.builder().token(self.token).build()
        app.add_handler(CommandHandler(["start", "myid"], self.start_cmd))
        app.add_handler(CommandHandler("health", self.health_cmd))
        app.add_handler(CommandHandler("menu", self.menu_cmd))
        app.add_handler(CommandHandler("tasks", self.tasks_cmd))
        app.add_handler(CommandHandler("restart", self.restart_cmd))
        app.add_handler(CommandHandler("logs", self.logs_cmd))
        app.add_handler(CommandHandler("wake", self.wake_cmd))
        app.add_handler(CommandHandler("task", self.task_cmd))
        print("Supervisor active (commands: start, myid, health, menu, tasks, restart, logs, wake, task)")
        try:
            app.run_polling(drop_pending_updates=True)
        except Conflict:
            print("Conflict detected ? another instance may be running.")
        finally:
            release_lock()

if __name__ == "__main__":
    SupervisorBot(TOKEN, CHAT_ID).start()
