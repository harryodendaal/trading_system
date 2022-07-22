from pandas import DataFrame
from .constants import EXCHANGE, STRATEGIES
from ta.trend import EMAIndicator, IchimokuIndicator
from ta.volatility import BollingerBands


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


def add_strategy_components(self, df: DataFrame):
    strategy = STRATEGIES[self.strategy]

    if strategy == '1':
        self.short_ema = EMAIndicator(
            close=df['Close'], window=20).ema_indicator().iloc[-1]
        self.long_ema = EMAIndicator(
            close=df['Close'], window=40).ema_indicator().iloc[-1]
    elif strategy == '2':
        self.ichimoku = IchimokuIndicator(
            high=df['High'], low=df['Low'])
        self.ichimoku.span_a = self.ichimoku.ichimoku_a().iloc[-1]
        self.ichimoku.span_a = self.ichimoku.ichimoku_b().iloc[-1]

        # bollinger bands
        self.bollinger = BollingerBands(df['Close'])
        self.bb = [self.bollinger.bollinger_hband().iloc[-1],
                   self.bollinger.bollinger_mavg().iloc[-1]]

    return
