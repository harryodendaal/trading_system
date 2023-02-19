from ta.trend import MACD, EMAIndicator

from Backend.strategies.blocks.entering import (
    close_above_ema_and_macd_line_above_signal,
)
from Backend.strategies.blocks.managing.positions import macd_update_position
from Backend.strategies.strategy.strategy import Strategy


class Macd(Strategy):
    def __init__(self, ema, macd, close) -> None:
        self.ema = ema
        self.macd = macd
        self.close = close

    def should_long(self):
        # return true if close is above EMA and MACD line is above signal line
        return close_above_ema_and_macd_line_above_signal(
            self.close, self.ema, self.macd
        )

    def update_position(self):
        macd_update_position(self)

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
