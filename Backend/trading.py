# This should use the functions from the research strategies.
# and then another layer above this teh cerebro which
# will decide which strategies to use.
import datetime
from time import sleep

from Backend.exchange_interface import (
    go_trade,
    has_active_order,
    has_open_position,
    invalidNonce_fix_somehow,
    set_leverage,
)
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
        # set_leverage(1, "BITUSDT")

        while True:
            for symbol in self.symbols:
                strats = Strategies.available_strategies(symbol)
                for s in strats:
                    strategy_interface = Strategies(s)

                    print("Trading: ", symbol)
                    print("strategy: ")
                    strategy_interface.strategy_name()

                    ############## START #############
                    strategy_interface.live_before()
                    in_trade, side = has_open_position(symbol)

                    if in_trade:
                        if side == "short":
                            strategy_interface.strategy.is_short = True
                        else:
                            strategy_interface.strategy.is_long = True
                        print("In Trade")
                        strategy_interface.live_update_position(symbol)

                    if not in_trade:
                        print("Not In Trade")

                        if has_active_order(symbol):
                            if strategy_interface.live_should_cancel_entry():
                                # cancel active entry orders. currently only doing market orders.
                                pass
                            # the stop loss and take profit orders
                        else:
                            if strategy_interface.live_should_long():
                                go_trade("L", self.trade_size, symbol)
                                print("Long Entered")

                            elif strategy_interface.live_should_short():
                                go_trade("S", self.trade_size, symbol)
                                print("Short Entered")

                    now = datetime.datetime.now()
                    print("__________________________________________________")
                    # print(now.strftime("%H:%M:%S ") + " | " + symbol + " |")
                    sleep(2)

            # live_after()  # message myself on telegram
