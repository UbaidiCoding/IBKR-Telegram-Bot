from flask import Flask, request
from bot import handle_buy, handle_sell
from telegram_handler import run_telegram_bot
import threading

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    action = data.get("action")
    symbol = data.get("symbol")
    if action == "buy":
        return handle_buy(symbol)
    elif action == "sell":
        return handle_sell(symbol)
    return {"status": "unknown action"}, 400

if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot).start()
    app.run(port=5000)
