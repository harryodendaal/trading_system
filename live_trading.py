# This should use the functions from the research strategies.
# and then another layer above this teh cerebro which
# will decide which strategies to use.
from math import floor
from time import sleep
import datetime
import ccxt
import pandas as pd
from ta.trend import EMAIndicator
from pprint import pprint
from auxillary_functions import go_trade, has_open_position
from config import APIkey, APIsecret
from strategies.__research_strategies.death_cross_20_40 import (
    should_cancel, should_long, should_short, update_position)

# should we have a class for the overarching trading system
# and then another class for indivdual symbols/trades?

exchange = ccxt.bybit({
    'apiKey': APIkey,
    'secret': APIsecret,
    'enableRateLimit': True,
    # 'recvWindow': 10000000,
    'adjustForTimeDifference': True
    # 'verbose': True,
})


class Live_trading():
    def __init__(self, capital=10000, symbols=['ETHUSDT'], timeframe='15m') -> None:
        self.capital = capital
        self.symbols = symbols
        self.timeframe = timeframe

        self.exchange = ccxt.bybit({
            'apiKey': APIkey,
            'secret': APIsecret,
            'enableRateLimit': True,
            # 'recvWindow': 10000000,
            'adjustForTimeDifference': True
            # 'verbose': True,
        })
        self.is_long = False
        self.is_short = False

    def prepare(self) -> pd.DataFrame:
        '''
                        Takes the symbol and time
                        returns a dataframe with ohlcv and indicators caculated.
        '''

        global exchange
        bars = exchange.fetch_ohlcv(
            symbol=self.symbol, timeframe=self.timeframe, limit=100)
        df = pd.DataFrame(bars[:-1], columns=['Date',
                                              'Open', 'High', 'Low', 'Close', 'Volume'])
        df['Date'] = pd.to_datetime(df['Date'], unit='ms')

        self.short_ema = EMAIndicator(
            close=df['Close'], window=20).ema_indicator().iloc[-1]
        self.long_ema = EMAIndicator(
            close=df['Close'], window=40).ema_indicator().iloc[-1]

        # call function here that determines which indicators to add depending on the
        # strategy.
        return df

    def liquidate(self):
        global exchange
        side = 'short' if (self.side == "long") else "long"

        trade_res = exchange.create_order(
            self.symbol, 'market', side, amount=0.05, params={'reduce_only': True})

        print("Liquidated Position")

        return

    def run(self):
        global exchange
        size = floor(exchange.fetch_balance()[
                     'USDT']['total']/len(self.symbols)/2)

        while True:
            for symbol in self.symbols:
                self.symbol = symbol

                # create all that is needed to decide whether or not engage in trade.
                self.prepare()
                # this is the start of the cycle look at the current candle

                try:
                    in_trade, self.side = has_open_position(
                        exchange, self.symbol)
                except Exception as e:
                    print(e)
                    continue

                if in_trade:
                    print("In Trade")
                    # in update_position() check whether position should be closed
                    # or if parameters should be updated.
                    update_position(self)

                if (not in_trade):
                    print("Not In Trade")
                    # add should_cancel if order has not been executed yet.
                    if should_long(self):
                        go_trade('L', size, symbol, exchange)
                        print("Long Entered")
                    elif should_short(self):
                        go_trade('S', size, symbol, exchange)
                        print("Short Entered")

                now = datetime.datetime.now()
                print(now.strftime('%H:%M:%S ') + self.symbol + " |  ")
                sleep(1)


        # after()  # message myself on telegram
cerebro = Live_trading(capital=10000, symbols=[
                       'ETHUSDT', 'ETCUSDT', 'BITUSDT', 'GMTUSDT', 'OPUSDT', 'RUNEUSDT', 'TRBUSDT'], timeframe='15m',)
cerebro.run()
# Next up instead trave for now only with inverse perpetual
