from ta.trend import EMAIndicator

from Backend.strategies.strategy.strategy import Strategy


class TestStrategy01(Strategy):
    def __init__(self, short_ema, long_ema) -> None:
        self.short_ema = short_ema
        self.long_ema = long_ema

    def should_long(self) -> bool:
        print(self.short_ema > self.long_ema)
        return self.short_ema > self.long_ema

    def update_position(self) -> None:
        if self.short_ema <= self.long_ema:
            self.liquidate("BITUSDT")

    @classmethod
    def add_strategy_components(cls, df):

        short_ema = (
            EMAIndicator(close=df["Close"], window=20).ema_indicator().iloc[-1],
        )
        long_ema = (
            EMAIndicator(close=df["Close"], window=40).ema_indicator().iloc[-1],
        )

        return cls(short_ema, long_ema)
