# This should use the functions from the research strategies.
# and then another layer above this teh cerebro which
# will decide which strategies to use.
import datetime
from time import sleep

from Backend.exchange_interface.live_exchange_interface import (
    go_trade,
    has_active_order,
    has_open_position,
    invalidNonce_fix_somehow,
)
from Backend.strategies.strategy.death_cross_20_40 import DeathCross
from Backend.strategies.strategy.macd_ema import Macd
from Backend.strategies.strategy_interface import Strategies


class Trading:
    """
    Trading class, handle the execution flow.
    """

    def __init__(
        self,
        symbols,
        trade_size,
    ) -> None:

        self.symbols = symbols
        self.trade_size = trade_size
        #
        # self.close

    def run(self):
        """Runs the strategy based of jesse structure."""
        invalidNonce_fix_somehow()

        # TODO filter the strategies and then apply each    strategy_interface to each symbol
        while True:
            for symbol in self.symbols:

                P = Macd.add_strategy_components(Strategies.prepare(symbol, "15m"))
                # for now just create teh df
                strategy_interface = Strategies(P)

                print("Searching for trade on: ", symbol)
                ############## START #############
                strategy_interface.live_before()
                in_trade = has_open_position(symbol)

                if in_trade:
                    print("In Trade")
                    strategy_interface.live_update_position()

                if not in_trade:
                    print("Not In Trade")

                    if has_active_order(symbol):
                        if strategy_interface.live_should_cancel_entry():
                            # cancel active entry orders.
                            pass
                        # the stop loss and take profit orders
                    else:

                        if strategy_interface.live_should_long():
                            go_trade("L", self.trade_size, symbol)
                            print("Long Entered")
                            strategy_interface.strategy.is_long = True

                        elif strategy_interface.live_should_short():
                            go_trade("S", self.trade_size, symbol)
                            print("Short Entered")
                            strategy_interface.strategy.is_short = True

                now = datetime.datetime.now()
                print(now.strftime("%H:%M:%S ") + symbol + " |  ")
                sleep(2)

        # live_after()  # message myself on telegram
