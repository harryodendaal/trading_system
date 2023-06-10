from ccxt import bybit


def go_trade(action: str, size: int, symbol: str, exchange: bybit):
    '''
        takes the action, size and symbol
        opens a position
    '''

    current_price = float(exchange.fetch_ticker(symbol='ETHUSDT')['close'])
    take_profit = round(current_price + current_price*(0.1/100), 2)
    stop_loss = round(current_price - current_price*(0.1/100), 2)
    # print(f'stoploss = {stop_loss} and profit = {take_profit}')

    # go long and go short
    side = 'buy' if action == 'L' else 'sell'
    params = {'take_profit': take_profit, 'stop_loss': stop_loss} if action == 'L' else {
        'take_profit': stop_loss, 'stop_loss': take_profit}

    o = exchange.create_order(symbol, 'market', side,
                              amount=size, params=params)


def has_active_orders(exchange: bybit):
    return(exchange.fetch_open_orders("ETHUSDT") == [])


def should_cancel():
    return False


def has_open_position(exchange: bybit, symbol: str):
    market = exchange.market(symbol)
    response = exchange.private_linear_get_position_list(
        {'symbol': market['id']})

    linear_positions = response['result']
    for item in linear_positions:
        if item['position_value'] != '0':
            return True

    return False
