# pylint: disable=E1101
import pandas as pd

from Backend.exchange_interface import fetch_ohlcv_data
from Backend.strategies.strategy import DeathCross, Macd, TestStrategy01
from Backend.strategies.strategy.strategy import Strategy


class Strategies:
    """ """

    def __init__(self, strategy: Strategy) -> None:
        self.strategy = strategy

    @staticmethod
    def prepare(symbol, timeframe):
        """
        add the components needed to execute the designated strategy.
        """

        # type: ignore
        bars = fetch_ohlcv_data(symbol, timeframe)
        data_frame = pd.DataFrame(
            bars[:-1], columns=["Date", "Open", "High", "Low", "Close", "Volume"]
        )
        data_frame["Date"] = pd.to_datetime(data_frame["Date"], unit="ms")

        return data_frame

    @staticmethod
    def available_strategies(symbol, timeframe="1m"):
        return [
            TestStrategy01.add_strategy_components(
                Strategies.prepare(symbol, timeframe)
            )
            # Macd.add_strategy_components(Strategies.prepare(symbol, timeframe)),
            # DeathCross.add_strategy_components(Strategies.prepare(symbol, timeframe)),
        ]

    def live_before(self):
        """
        this is the first method that gets called when a new candle is received.
        It is used for updating self.vars (custom variables)
        or any other action you might have in
        mind that needs to be done before your strategy gets executed.
        """
        self.strategy.before()

    def live_update_position(self):
        """
        Called only if you have an open position, used to update the exit point
        (dynamically adjusting take-profit or stop-loss) or
        to add the size of the position if needed.
        """
        self.strategy.update_position()

    def live_should_short(self):
        """
        If not position is open and no order is active
        returns whether or not should enter short.
        """
        return self.strategy.should_short()

    def live_should_long(self):

        """
        If not position is open and no order is active
        returns whether or not should enter long.
        """
        return self.strategy.should_long()

    def live_should_cancel_entry(self):
        """
        If there is an open order that has not been executed yet then this funciton
        returns whether that order should be cancelled
        """

        return self.strategy.should_cancel_entry()
