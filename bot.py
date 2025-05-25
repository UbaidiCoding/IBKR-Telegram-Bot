import json
from ibkr_client import get_market_price, place_limit_order, get_position, get_unrealized_pct
from math import floor

CONFIG_FILE = "config.json"

def load_config(symbol):
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    return config.get(symbol)

def handle_buy(symbol):
    cfg = load_config(symbol)
    if not cfg:
        return {"status": "no config for symbol"}, 400

    contract, price = get_market_price(symbol)
    qty = floor(cfg["usd_amount"] / price)

    if qty <= 0:
        return {"status": "not enough USD for quantity"}, 400

    trade = place_limit_order(contract, "BUY", qty, price)
    return {"status": "buy order placed", "quantity": qty, "price": price}

def handle_sell(symbol):
    cfg = load_config(symbol)
    if not cfg:
        return {"status": "no config for symbol"}, 400

    unrealized_pct = get_unrealized_pct(symbol)
    if unrealized_pct >= cfg["profit_pct"]:
        contract, price = get_market_price(symbol)
        pos = get_position(symbol)
        if pos:
            trade = place_limit_order(contract, "SELL", pos.position, price)
            return {"status": "sell order placed", "quantity": pos.position, "price": price}
        else:
            return {"status": "no open position"}, 400
    else:
        return {"status": f"profit target not met: {unrealized_pct:.2f}%"}, 200
