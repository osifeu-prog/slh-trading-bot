import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import httpx

# טוקן מהסביבה
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN")

PUBLIC_API_URL = os.getenv("PUBLIC_API_URL", "http://localhost:8080")
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("SLH Supervisor is alive!")

async def remote_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{PUBLIC_API_URL}/control/status")
            data = resp.json()
            await update.message.reply_text(f"📊 Status: {data}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def remote_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(f"{PUBLIC_API_URL}/control/restart")
            await update.message.reply_text(f"🔄 Restart sent: {resp.text}")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("remote_status", remote_status))
    app.add_handler(CommandHandler("remote_restart", remote_restart))
    logging.info("✅ Supervisor started. Commands: /start , /remote_status , /remote_restart")
    app.run_polling()
