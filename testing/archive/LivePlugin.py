from pickle import TRUE
import pandas as pd
import ccxt
import talib as ta
from archive.bot import prepare
from strategies._LIVE.config import APIkey, APIsecret
from archive.shared_functions import should_liquidate, should_long, should_short
from archive.non_shared_functions import go_trade, has_active_orders, has_open_position, should_cancel
# def live_plugin():
# 	before()#generate needed candles.
import time


class LivePlugin():

    # define all the things it needs
    def __init__(self, capital, symbols, size, candles) -> None:
        self.capital = capital
        self.symbols = symbols
        self.size = size
        self.candles = candles
        self.exchange = ccxt.bybit({
            'apiKey': APIkey,
            'secret': APIsecret,
            'enableRateLimit': True,
            # 'verbose': True,
        })
        self.is_long = False
        self.is_short = False

        # just copy past in the necessary properties or how to adjust and decide which?
    @property
    def short_ema(self):
        # returns the new candles ema value
        return ta.EMA(self.candles, 20)

    @property
    def long_ema(self):
        return ta.EMA(self.candles, 40)

    def prepare(self, symbol: str, time: str) -> pd.DataFrame:
        '''
                Takes the symbol and time 
                returns a dataframe with ohlcv and indicators caculated.
        '''

        bars = self.exchange.fetch_ohlcv(
            symbol=symbol, timeframe=time, limit=100)
        df = pd.DataFrame(bars[:-1], columns=['timestamp',
                                              'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

        return df

    def run(self):

        while True:
            for symbol in self.symbols:
                # needs to create indicators
                # creates the values for the "property ones" and also
                # creates teh valeus for the price
                data = self.prepare(symbol, '1m')

                # in_trade = check_if_in_position(symbol=symbol)

                if has_open_position():

                    # if open position possible update it
                    # MAIN = update_position()
                    # broken down into should_liquidate, should adjust take profit, should adjust stoploss
                    if(should_liquidate(self)):
                        print('I should liquidate this position')

                else:
                    # if not in position check if orders submitted
                    # dont care about this for now.
                    if has_active_orders():
                        # for now do nothing since won't have orders
                        pass

                        # if in active order should this order be cancelled?
                        # cancel = should_cancel(self)  # for now just return false
                        # if(cancel):
                        #     go_cancel()

                    else:
                        # do not have active orders;
                        if should_long(self):
                            go_trade('L', self.size, symbol, self.exchange)
                        elif should_short(self):
                            go_trade('S', self.size, symbol, self.exchange)

            time.sleep(10)
            # after()  # message myself on telegram


symbols = ['ETHUSDT']
while True:
    for symbol in symbols:
        time.sleep(10)

    # bot = LivePlugin(...)
    # add the scheduler so called every minute
    # bot.run()
    # the indicators are the most difficult it seems

    # NOW DO move the prepare away
    # run this file see if it works
