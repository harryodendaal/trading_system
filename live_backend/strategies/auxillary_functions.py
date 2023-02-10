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


# Need to break these up and work on the infrastructure.


def print_out_current_strategy(strategy):
    if STRATEGIES[strategy] == "0":
        print("")
    if STRATEGIES[strategy] == "1":
        print("death_cross_20_40")
    if STRATEGIES[strategy] == "2":
        print("simple_bollinger")
    if STRATEGIES[strategy] == "3":
        print("macd_ema")
