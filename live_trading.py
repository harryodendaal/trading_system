# This should use the functions from the research strategies.
# and then another layer above this teh cerebro which
# will decide which strategies to use.
from math import floor
from time import sleep
import datetime
import pandas as pd
from pprint import pprint
from auxillary_functions import add_strategy_components, fetch_position_side, fetch_position_size, go_trade, has_active_order, has_open_position
from live_strategy_functions import live_before, live_should_cancel, live_should_cancel_entry, live_should_long, live_should_short, live_update_position
from constants import EXCHANGE

# should we have a class for the overarching trading system
# and then another class for indivdual symbols/trades?


class LiveTrading():
    def __init__(self, capital=10000, symbols=['ETHUSDT'], timeframe='15m') -> None:
        self.capital = capital
        self.symbols = symbols
        self.timeframe = timeframe

        self.is_long = False
        self.is_short = False

    def prepare(self) -> pd.DataFrame:
        '''
                        Takes the symbol and time
                        returns a dataframe with ohlcv and indicators caculated.
        '''

        bars = EXCHANGE.fetch_ohlcv(
            symbol=self.symbol, timeframe=self.timeframe, limit=100)
        df = pd.DataFrame(bars[:-1], columns=['Date',
                                              'Open', 'High', 'Low', 'Close', 'Volume'])
        df['Date'] = pd.to_datetime(df['Date'], unit='ms')

        # add the things necessary for strategy function.
        add_strategy_components(self, df)

        self.close = df['Close'].iloc[-1]

        # The always ones?
        return df

    def liquidate(self):
        # get side here and also amount

        symbol = self.symbol
        side = fetch_position_side(EXCHANGE, symbol)
        size = fetch_position_size(EXCHANGE, symbol)

        # generally will only be called if in position but in case
        # exit position here if not in position
        if (side == "" or size == 0):
            return

        side = 'sell' if (side == 'long') else 'buy'

        trade_res = EXCHANGE.create_order(
            symbol, 'market', side, amount=size, params={'reduce_only': True})
        print("Liquidated " + symbol)

        return

    def run(self):

        self.strategy = 1

        trade_size = floor(EXCHANGE.fetch_balance()[
            'USDT']['total']/len(self.symbols)/2)

        # self.liquidate()

        while True:
            for symbol in self.symbols:
                self.symbol = symbol

                self.prepare()  # this is kinda apart of what before should do
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
                        # only cancels the order not
                        live_should_cancel_entry(self)
                        # the stop loss and take profit orders
                    else:

                        if live_should_long(self):
                            go_trade('L', trade_size, symbol)
                            print("Long Entered")
                        elif live_should_short(self):
                            go_trade('S', trade_size, symbol)
                            print("Short Entered")
                        else:
                            live_should_cancel(self)

                now = datetime.datetime.now()
                print(now.strftime('%H:%M:%S ') + self.symbol + " |  ")
                sleep(2)

        # after()  # message myself on telegram
symbols = ['ETHUSDT', 'ETCUSDT', 'BITUSDT',
           'GMTUSDT', 'OPUSDT', 'RUNEUSDT', 'TRBUSDT']
cerebro = LiveTrading(capital=10000, symbols=symbols, timeframe='15m',)
cerebro.run()
# Next up instead trave for now only with inverse perpetual

# things not yet. need to add another strategy maybe.
# for now stick with all orders later to the specific ones.
# EXCHANGE.cancel_all_orders('ETHUSDT')
