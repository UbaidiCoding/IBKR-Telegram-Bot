from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import json

TOKEN = "8144114288:AAF2wcOgMmuSbnok9EPn7PrLhLGAAlmvjaA"  # replace with your actual token
CONFIG_FILE = "config.json"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! Use /config to set trading config.")

async def config(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send ticker config like:\nAAPL, 100, 5\nFormat: SYMBOL, USD_AMOUNT, PROFIT_PERCENT"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        symbol, usd, profit = [x.strip() for x in text.split(",")]
        symbol = symbol.upper()
        config = {}
        try:
            with open(CONFIG_FILE) as f:
                config = json.load(f)
        except:
            pass
        config[symbol] = {
            "usd_amount": float(usd),
            "profit_pct": float(profit)
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        await update.message.reply_text(f"✅ Config saved for {symbol}")
    except Exception as e:
        await update.message.reply_text("❌ Error. Format should be:\nAAPL, 100, 5")

def run_telegram_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("config", config))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
