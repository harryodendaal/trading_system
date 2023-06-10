from Backend.exchange_interface.constants import EXCHANGE


def has_active_order(symbol: str):
    """Check to see if the symbol has an active order"""
    # keep the strategy orders id in database to see
    # which starte executed this order?
    orders = EXCHANGE.fetch_orders(symbol)
    for o in orders:
        if o["status"] == "open":
            if o["filled"] == 0.0:
                return True
    return False


def has_open_position(symbol):
    """Check to see if the symbol has an open position"""

    positions = EXCHANGE.fetch_positions([symbol])

    for item in positions:
        if item["contracts"] != 0.0:
            return True, positions[0]["side"]
    return False, positions[0]["side"]


def fetch_position_side(symbol):
    """Check to see if position is a long or short"""
    positions = EXCHANGE.fetch_positions([symbol])

    for item in positions:
        if item["contracts"] != 0.0:
            return item["side"]
    return ""


def fetch_position_size(symbol):
    """Check to see the size of the position"""
    positions = EXCHANGE.fetch_positions([symbol])

    for item in positions:
        if item["contracts"] != 0.0:
            return item["info"]["size"]
    return 0


def fetch_ohlcv_data(symbol, timeframe):
    """get the candle data for a certain symbol and timeframe."""
    return EXCHANGE.fetch_ohlcv(symbol=symbol, timeframe=timeframe, limit=100)


def fetch_symbol_currentprice(symbol):
    return float(EXCHANGE.fetch_ticker(symbol=symbol)["close"])
