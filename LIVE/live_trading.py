# This should use the functions from the research strategies.
# and then another layer above this teh cerebro which
# will decide which strategies to use.
import datetime
from math import floor
from pprint import pprint
from time import sleep

import pandas as pd

from LIVE.strategies.auxillary_functions import (add_strategy_components, print_out_current_strategy)
from LIVE.exchange_interface.live_exchange_interface import (fetch_position_side, 
fetch_position_size, go_trade, has_active_order, has_open_position, fetch_ohlcv_data,
close_position, invalidNonce_fix_somehow)
from LIVE.exchange_interface.constants import EXCHANGE
from LIVE.strategies.live_strategies import (live_before, live_should_cancel,
                                      live_should_cancel_entry,
                                      live_should_long, live_should_short,
                                      live_update_position)



class LiveTrading():
    '''
        Want this to just do the trading. The strategies hsould be added before hand this only handle the trading. BUT it will still need to excahge 
        interface ones. maybe they should be subpackages then, things which are needed.
    '''
    def __init__(self, capital=10000, symbols=['ETHUSDT'], timeframe='15m', strategy=1, trade_size=10) -> None:

        self.capital = capital
        self.symbols = symbols
        self.timeframe = timeframe
        self.strategy = strategy
        self.trade_size = trade_size

    def prepare(self) -> pd.DataFrame:
        '''
                        Takes the symbol and time
                        returns a dataframe with ohlcv and indicators caculated.
        '''

        bars = fetch_ohlcv_data(self.symbol, self.timeframe)

            
        df = pd.DataFrame(bars[:-1], columns=['Date',
                                              'Open', 'High', 'Low', 'Close', 'Volume'])
        df['Date'] = pd.to_datetime(df['Date'], unit='ms')

        add_strategy_components(self, df)

        self.close = df['Close'].iloc[-1]

        return df


    def run(self):
        print_out_current_strategy(self.strategy)
        invalidNonce_fix_somehow()
        while True:
            for symbol in self.symbols:
                print('Searching for trade on: ', symbol)
                self.symbol = symbol
                self.prepare()

                ############## START #############
                live_before(self)
                # before()

                try:
                    in_trade = has_open_position(self.symbol)
                except Exception as e:
                    print(e)
                    continue

                if in_trade:
                    print("In Trade")
                    # used for dynamically exiting trade. and adjusting stop/take loss/profit
                    live_update_position(self)

                if (not in_trade):
                    print("Not In Trade")

                    if (has_active_order(symbol)):
                        if(live_should_cancel_entry(self)):
                            # cancel active orders.
                            pass
                        # the stop loss and take profit orders
                    else:

                        if live_should_long(self):
                            go_trade('L', self.trade_size, symbol)
                            print("Long Entered")
                        elif live_should_short(self):
                            go_trade('S', self.trade_size, symbol)
                            print("Short Entered")
                        else:
                            live_should_cancel(self)

                now = datetime.datetime.now()
                print(now.strftime('%H:%M:%S ') + self.symbol + " |  ")
                sleep(2)

            # live_after()  # message myself on telegram

    def liquidate(self):
        # does this completely close position?

        symbol = self.symbol
        side = fetch_position_side(symbol)
        size = fetch_position_size(symbol)

        # generally will only be called if in position but in case
        # exit position here if not in position
        if (side == "" or size == 0):
            return

        side = 'sell' if (side == 'long') else 'buy'

        trade_res = close_position(symbol=symbol, side=side, size=size)

        return
strut = ['1 ' , '2']