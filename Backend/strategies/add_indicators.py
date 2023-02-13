from pandas import DataFrame
from ta.trend import MACD, EMAIndicator

from .constants import STRATEGIES


def add_strategy_components(self, df: DataFrame):
    strategy = STRATEGIES[self.strategy]
    print(strategy)
    if strategy == "1":
        short_ema_value = (
            EMAIndicator(close=df["Close"], window=20).ema_indicator().iloc[-1],
        )
        long_ema_value = (
            EMAIndicator(close=df["Close"], window=40).ema_indicator().iloc[-1]
        )

        setattr(self, "short_ema", short_ema_value)
        setattr(
            self,
            "long_ema",
            long_ema_value,
        )
    elif strategy == "3":
        # macd[0] = macd line AND
        # macd[1] = signal line.
        ema_value = EMAIndicator(close=df["Close"], window=100).ema_indicator().iloc[-1]
        macdonald_value = MACD(df["Close"])

        setattr(self, "ema", ema_value)
        setattr(
            self,
            "macd",
            [macdonald_value.macd().iloc[-1], macdonald_value.macd_signal().iloc[-1]],
        )
    return
