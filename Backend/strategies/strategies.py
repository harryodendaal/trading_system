# pylint: disable=E1101
import pandas as pd

from Backend.exchange_interface.live_exchange_interface import fetch_ohlcv_data
from Backend.strategies.add_indicators import add_strategy_components
from Backend.strategies.constants import STRATEGIES

from .strategy import death_cross_20_40, macd_ema


class Strategies:
    """ """

    def __init__(self, strategy: int, timeframe: str) -> None:
        self.strategy = strategy
        self.timeframe = timeframe
        self.is_long = False
        self.is_short = False

    def adding_new_attr(self, attr):
        setattr(self, attr, attr)

    def prepare(self):
        """
        add the components needed to execute the designated strategy.
        """

        # type: ignore
        bars = fetch_ohlcv_data(self.symbol, self.timeframe)
        data_frame = pd.DataFrame(
            bars[:-1], columns=["Date", "Open", "High", "Low", "Close", "Volume"]
        )
        data_frame["Date"] = pd.to_datetime(data_frame["Date"], unit="ms")

        add_strategy_components(self, data_frame)

        close = data_frame["Close"].iloc[-1]
        setattr(self, "close", close)

    def live_before(self):
        """
        this is the first method that gets called when a new candle is received.
        It is used for updating self.vars (custom variables)
        or any other action you might have in
        mind that needs to be done before your strategy gets executed.
        """
        strategy = STRATEGIES[self.strategy]

        if strategy == "1":
            return death_cross_20_40.before(self)
        elif strategy == "3":
            return macd_ema.before(self)

    def live_update_position(self):
        """
        Called only if you have an open position, used to update the exit point
        (dynamically adjusting take-profit or stop-loss) or
        to add the size of the position if needed.
        """
        strategy = STRATEGIES[self.strategy]

        if strategy == "1":
            return death_cross_20_40.update_position(self)
        elif strategy == "3":
            return macd_ema.update_position(self)

    def live_should_short(self):
        """
        If not position is open and no order is active
        returns whether or not should enter short.
        """
        strategy = STRATEGIES[self.strategy]

        if strategy == "1":
            return death_cross_20_40.should_short(self)
        elif strategy == "3":
            return macd_ema.should_short(self)

    def live_should_long(self):
        """
        If not position is open and no order is active
        returns whether or not should enter long.
        """
        strategy = STRATEGIES[self.strategy]

        if strategy == "1":
            return death_cross_20_40.should_long(self)
        elif strategy == "3":
            return macd_ema.should_long(self)

    def live_should_cancel_entry(self):
        """
        If there is an open order that has not been executed yet then this funciton
        returns whether that order should be cancelled
        """
        strategy = STRATEGIES[self.strategy]

        if strategy == "1":
            return death_cross_20_40.should_cancel_entry(self)

        elif strategy == "3":
            return macd_ema.should_cancel_entry(self)

            # def live_after(self):
            # 	after(self)
            # 	return
