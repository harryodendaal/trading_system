from ta.trend import MACD, EMAIndicator

from Backend.exchange_interface.live_exchange_interface import liquidate
from Backend.strategies.strategy._strategy_template import Strategy


class DeathCross(Strategy):
    def __init__(self, short_ema, long_ema, is_long, is_short) -> None:
        self.short_ema = short_ema
        self.long_ema = long_ema
        self.is_long = is_long
        self.is_short = is_short

    def print_name(self):
        print("DEATH CROSS 20 40")

    def should_long(self):
        # 20 > 40 ; blue > red
        return self.short_ema > self.long_ema

    def should_short(self):
        return self.long_ema > self.short_ema

    def update_position(self, symbol) -> None:
        if self.is_long and self.short_ema < self.long_ema:
            liquidate(symbol)

        if self.is_short and self.short_ema > self.long_ema:
            liquidate(symbol)

    @classmethod
    def add_strategy_components(cls, df):
        short_ema_value = (
            EMAIndicator(close=df["Close"], window=20).ema_indicator().iloc[-1]
        )
        long_ema_value = (
            EMAIndicator(close=df["Close"], window=40).ema_indicator().iloc[-1]
        )

        return cls(short_ema_value, long_ema_value, False, False)
