from pandas import DataFrame
from .constants import STRATEGIES
from ta.trend import EMAIndicator, IchimokuIndicator, MACD
from ta.volatility import BollingerBands



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
    elif strategy == '3':
        # macd[0] = macd line AND
        # macd[1] = signal line.
        self.ema = EMAIndicator(
            close=df['Close'], window=100).ema_indicator().iloc[-1]
        self.macdonald = MACD(df['Close'])
        self.macd = [self.macdonald.macd().iloc[-1],
                     self.macdonald.macd_signal().iloc[-1]]
    return

# Need to break these up and work on the infrastructure.


def print_out_current_strategy(strategy):
    if STRATEGIES[strategy] == '0':
        print('')
    if STRATEGIES[strategy] == '1':
        print('death_cross_20_40')
    if STRATEGIES[strategy] == '2':
        print('simple_bollinger')
    if STRATEGIES[strategy] == '3':
        print('macd_ema')
