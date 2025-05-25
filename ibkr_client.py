from ib_insync import *
import time

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)  # Use correct port for TWS / IB Gateway

def get_market_price(symbol):
    contract = Stock(symbol, 'SMART', 'USD')
    ib.qualifyContracts(contract)
    ticker = ib.reqMktData(contract, '', False, False)
    ib.sleep(1)
    price = ticker.marketPrice()
    ib.cancelMktData(contract)
    return contract, price

def place_limit_order(contract, action, quantity, price):
    order = LimitOrder(action, quantity, price, tif='GTC', outsideRth=True)
    trade = ib.placeOrder(contract, order)
    ib.sleep(1)
    return trade

def get_position(symbol):
    positions = ib.positions()
    for pos in positions:
        if pos.contract.symbol == symbol:
            return pos
    return None

def get_unrealized_pct(symbol):
    pnl = ib.pnl()
    for p in pnl:
        if p.contract.symbol == symbol:
            return (p.unrealizedPNL / p.value) * 100
    return 0
