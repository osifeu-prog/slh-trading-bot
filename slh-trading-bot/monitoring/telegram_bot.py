import requests, threading
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

CHANNEL_INVITE = "https://t.me/+37XWeJ87enw4YjJk"

class TelegramBot:
    def __init__(self, token, chat_id=None):
        self.token = token
        self.chat_id = chat_id
        self.app = None

    def send_message(self, text):
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            payload = {"chat_id": self.chat_id, "text": text}
            requests.post(url, json=payload)
        except Exception as e:
            print(f"Telegram send error: {e}")

    async def myid(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        await update.message.reply_text(
            f"Your user ID: `{user_id}`\n\n"
            f"Join our channel: {CHANNEL_INVITE}",
            parse_mode="Markdown"
        )

    def build_app(self):
        self.app = Application.builder().token(self.token).build()
        self.app.add_handler(CommandHandler(["start", "myid"], self.myid))
        print("Telegram app built (commands: /start, /myid)")
