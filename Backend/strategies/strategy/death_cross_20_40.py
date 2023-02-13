from ta.trend import MACD, EMAIndicator

from Backend.strategies.blocks.entering import ema_cross
from Backend.strategies.blocks.managing.positions import dc_update_position
from Backend.strategies.strategy.strategy import Strategy

# overwrite strategy, then after finishing this part make it so that strategies are easy to test.


class DeathCross(Strategy):
    def __init__(self, short_ema, long_ema, is_long, is_short) -> None:
        self.short_ema = short_ema
        self.long_ema = long_ema
        self.is_long = is_long
        self.is_short = is_short

    def before(self):
        return

    def should_long(self):
        # 20 > 40 ; blue > red
        return ema_cross(self.short_ema, self.long_ema)

    def should_short(self):
        return ema_cross(self.long_ema, self.short_ema)

    def should_cancel_entry(self):
        return True

    def update_position(self) -> None:
        dc_update_position(self)

    @classmethod
    def add_strategy_components(cls, df):
        short_ema_value = (
            EMAIndicator(close=df["Close"], window=20).ema_indicator().iloc[-1],
        )
        long_ema_value = (
            EMAIndicator(close=df["Close"], window=40).ema_indicator().iloc[-1]
        )

        return cls(short_ema_value, long_ema_value, False, False)
