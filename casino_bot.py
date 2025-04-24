
import os
import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

user_balances = {}

def get_balance(user_id):
    return user_balances.get(user_id, 1000)

def set_balance(user_id, balance):
    user_balances[user_id] = balance

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_balances:
        set_balance(user_id, 1000)
    await update.message.reply_text(f"🎰 Casino Bot'a hoş geldin! Bakiyen: {get_balance(user_id)}₺")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(f"💰 Bakiyen: {get_balance(user_id)}₺")

async def bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    if len(args) != 2 or args[0] not in ["red", "black"]:
        await update.message.reply_text("Kullanım: /bet red 100")
        return

    color, amount = args[0], int(args[1])
    balance = get_balance(user_id)

    if amount > balance:
        await update.message.reply_text("Yetersiz bakiye.")
        return

    result = random.choice(["red", "black"])
    if color == result:
        balance += amount
        await update.message.reply_text(f"🎉 Kazandın! Top: {result}. Yeni bakiye: {balance}₺")
    else:
        balance -= amount
        await update.message.reply_text(f"😢 Kaybettin. Top: {result}. Yeni bakiye: {balance}₺")

    set_balance(user_id, balance)

async def slot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("Kullanım: /slot 100")
        return

    amount = int(args[0])
    balance = get_balance(user_id)

    if amount > balance:
        await update.message.reply_text("Yetersiz bakiye.")
        return

    emojis = ["🍒", "🍋", "🔔", "🍉", "⭐"]
    result = [random.choice(emojis) for _ in range(3)]

    if len(set(result)) == 1:
        balance += amount * 5
        await update.message.reply_text(f"{' '.join(result)}
🎉 JACKPOT! Yeni bakiye: {balance}₺")
    else:
        balance -= amount
        await update.message.reply_text(f"{' '.join(result)}
😢 Kaybettin. Yeni bakiye: {balance}₺")

    set_balance(user_id, balance)

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    app = ApplicationBuilder().token(os.environ["7776625674:AAEK0EOmnMtb50Um1IUf1cjBiDI7M4WBLlA"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("bet", bet))
    app.add_handler(CommandHandler("slot", slot))

    app.run_polling()
