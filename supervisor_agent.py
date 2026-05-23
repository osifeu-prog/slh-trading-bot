import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv('SUPERVISOR_BOT_TOKEN')

async def health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ SLH Supervisor is Active')

def main():
    if not TOKEN:
        print('❌ Missing SUPERVISOR_BOT_TOKEN in .env')
        return
    print('✅ Supervisor Bot started successfully')
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('health', health))
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
