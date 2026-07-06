import telebot
from telebot import types
import logging

logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot("8737037440:AAEeTfPlP5LkIwldPAcrmkFNmqUlEKVj-Hw")

@bot.message_handler(commands=['start'])
def start(m):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("🏛️ אקדמיה", callback_data="academy")
    btn2 = types.InlineKeyboardButton("💰 השקעות", callback_data="invest")
    btn3 = types.InlineKeyboardButton("🔰 Staking", callback_data="stake")
    btn4 = types.InlineKeyboardButton("📊 PnL", callback_data="report")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.reply_to(m, "ברוך הבא ל-SLH OS!\nבחר:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "invest":
        bot.send_message(call.message.chat.id, "💰 הצטרף להשקעה:\n/stake_join <amount> USDT")
    elif call.data == "stake":
        bot.send_message(call.message.chat.id, "🔰 Staking 4% חודשי\n/stake_join <amount>")
    elif call.data == "report":
        bot.send_message(call.message.chat.id, "📊 PnL: -1310$\nInvestors: 2")
    elif call.data == "academy":
        bot.send_message(call.message.chat.id, "🏛️ Courses coming soon!")

print("✅ Full menu with buttons started")
bot.infinity_polling()
