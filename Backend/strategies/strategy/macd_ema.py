from ta.trend import MACD, EMAIndicator

from Backend.exchange_interface.live_exchange_interface import liquidate
from Backend.strategies.strategy._strategy_template import Strategy


class Macd(Strategy):
    def __init__(self, ema, macd, close) -> None:
        self.ema = ema
        self.macd = macd
        self.close = close

    def print_name(self):
        print("MACE EMA")

    def should_long(self):
        # return true if close is above EMA and MACD line is above signal line

        return self.close > self.ema and self.macd[0] > self.macd[1]

    def update_position(self, symbol):
        # Close the position when MACD crosses below the signal line and closing prices is less than 100EMA

        if self.macd[0] < self.macd[1] and self.close < self.ema:
            liquidate(symbol)

    @classmethod
    def add_strategy_components(cls, df):
        ema_value = EMAIndicator(close=df["Close"], window=100).ema_indicator().iloc[-1]
        macdonald_value = MACD(df["Close"])
        close = df["Close"].iloc[-1]

        return cls(
            ema_value,
            [macdonald_value.macd().iloc[-1], macdonald_value.macd_signal().iloc[-1]],
            close,
        )
