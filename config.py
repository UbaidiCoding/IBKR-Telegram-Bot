import json

CONFIG_FILE = "config.json"

def set_config():
    symbol = input("Enter ticker symbol (e.g. AAPL): ").upper()
    usd_amount = float(input("Enter order size in USD: "))
    profit_pct = float(input("Enter minimum profit percentage to sell (e.g. 5 for 5%): "))

    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
    except:
        config = {}

    config[symbol] = {
        "usd_amount": usd_amount,
        "profit_pct": profit_pct
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

    print(f"Configuration for {symbol} saved.")
