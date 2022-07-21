from ccxt import bybit
from constants import EXCHANGE


def has_active_order(symbol: str):
    # keep the strategy orders id in database to see
    # which starte executed this order?
    orders = EXCHANGE.fetch_orders(symbol)
    for o in orders:
        if o['status'] == 'open':
            if o['filled'] == 0.0:
                return True
    return False


def has_open_position(symbol):
    positions = EXCHANGE.fetch_positions([symbol])

    for item in positions:
        if item['contracts'] != 0.0:
            return True
    return False


def fetch_position_side(symbol):
    positions = EXCHANGE.fetch_positions([symbol])

    for item in positions:
        if item['contracts'] != 0.0:
            return item['side']
    return ""


def fetch_position_size(symbol):
    positions = EXCHANGE.fetch_positions([symbol])

    for item in positions:
        if item['contracts'] != 0.0:
            return item['info']['size']
    return 0


def go_trade(action: str, size: int, symbol: str):
    '''
        takes the action, size and symbol
        opens a position
    '''

    current_price = float(EXCHANGE.fetch_ticker(symbol=symbol)['close'])
    take_profit = round(current_price + current_price*(0.1/100), 2)
    stop_loss = round(current_price - current_price*(0.1/100), 2)
    # print(f'stoploss = {stop_loss} and profit = {take_profit}')

    # go long and go short
    side = 'buy' if action == 'L' else 'sell'
    # params = {'take_profit': take_profit, 'stop_loss': stop_loss} if action == 'L' else {
    #     'take_profit': stop_loss, 'stop_loss': take_profit}

    amount = size/current_price
    o = EXCHANGE.create_order(symbol, 'market', side,
                              amount=amount)
    # print(o)
