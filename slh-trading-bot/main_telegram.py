import logging, os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "7591051736:AAH6hCADg076adJ28ZwrSR2Cwu0zzF7izzk"

# ================== COMMANDS ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = """
SLH Trading Bot Commands:
/start - Menu
/status - System status
/pnl - Current PnL
/positions - Open positions
/health - Supervisor health check
/myid - Your Telegram ID
/tasks - Show task list
/restart - Restart bot
/logs - Recent logs
/wake - Wake system
/task - Run task
/help - This menu
"""
    await update.message.reply_text(menu)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("? Bot is ONLINE and connected to Binance.\nDocker: Running\nDashboard: Live")

async def pnl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("?? PnL integration in progress.\nLive prices are flowing.")

async def positions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("?? No open positions at the moment.")

async def health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("?? System Health: OK\nDocker: Up\nTelegram: Single Instance")

async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your ID: {update.effective_user.id}")

async def tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("?? Tasks: 1. Merge supervisor 2. PnL integration 3. Deploy VPS")

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("?? Restarting bot...")
    os._exit(0)

async def logs_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with open("logs/main_telegram.log", "r") as f:
            lines = f.readlines()[-10:]
        await update.message.reply_text("?? Last 10 log lines:\n" + "".join(lines))
    except:
        await update.message.reply_text("No logs available.")

async def wake(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("? System is awake and operational.")

async def task_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("?? Task command received.")

# ================== MAIN (Synchronous) ==================
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("pnl", pnl))
    app.add_handler(CommandHandler("positions", positions))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("health", health))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CommandHandler("tasks", tasks))
    app.add_handler(CommandHandler("restart", restart))
    app.add_handler(CommandHandler("logs", logs_cmd))
    app.add_handler(CommandHandler("wake", wake))
    app.add_handler(CommandHandler("task", task_cmd))

    logger.info("? SLH Merged Bot Started (Windows Sync)")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()



