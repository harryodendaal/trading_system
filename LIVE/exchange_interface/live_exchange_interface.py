from LIVE.exchange_interface.constants import EXCHANGE



def has_active_order(symbol: str):
    '''Check to see if the symbol has an active order'''
    # keep the strategy orders id in database to see
    # which starte executed this order?
    orders = EXCHANGE.fetch_orders(symbol)
    for o in orders:
        if o['status'] == 'open':
            if o['filled'] == 0.0:
                return True
    return False


def has_open_position(symbol):
    '''Check to see if the symbol has an open position'''

    positions = EXCHANGE.fetch_positions([symbol])

    for item in positions:
        if item['contracts'] != 0.0:
            return True
    return False


def fetch_position_side(symbol):
    '''Check to see if position is a long or short'''
    positions = EXCHANGE.fetch_positions([symbol])

    for item in positions:
        if item['contracts'] != 0.0:
            return item['side']
    return ""


def fetch_position_size(symbol):
    '''Check to see the size of the position'''
    positions = EXCHANGE.fetch_positions([symbol])

    for item in positions:
        if item['contracts'] != 0.0:
            return item['info']['size']
    return 0

def fetch_ohlcv_data(symbol, timeframe):
    '''get the candle data for a certain symbol and timeframe.'''
    return EXCHANGE.fetch_ohlcv(
            symbol=symbol, timeframe=timeframe, limit=100)

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

def close_position(symbol, side, size):
    return EXCHANGE.create_order(
            symbol, 'market', side, amount=size, params={'reduce_only': True})

def invalidNonce_fix_somehow():
    print(EXCHANGE.load_time_difference())
    return
