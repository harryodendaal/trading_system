from ccxt import bybit


def has_open_position(exchange: bybit, symbol: str):
    positions = exchange.fetch_positions()

    for item in positions:
        if item['contracts'] != 0.0:
            if item['info']['symbol'] == symbol:

                return True, item['side']

    return False, ""


def go_trade(action: str, size: int, symbol: str, exchange: bybit):
    '''
        takes the action, size and symbol
        opens a position
    '''

    current_price = float(exchange.fetch_ticker(symbol=symbol)['close'])
    take_profit = round(current_price + current_price*(0.1/100), 2)
    stop_loss = round(current_price - current_price*(0.1/100), 2)
    # print(f'stoploss = {stop_loss} and profit = {take_profit}')

    # go long and go short
    side = 'buy' if action == 'L' else 'sell'
    # params = {'take_profit': take_profit, 'stop_loss': stop_loss} if action == 'L' else {
    #     'take_profit': stop_loss, 'stop_loss': take_profit}

    amount = size/current_price
    o = exchange.create_order(symbol, 'market', side,
                              amount=amount)
    # print(o)
