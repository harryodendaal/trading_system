import datetime
import time
from pprint import pprint
# import jesse.indicators as ta
import ccxt
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from psycopg2 import paramstyle
# from tinydb import TinyDB
import talib as ta
import numpy as np
from ccxt import bybit
from strategies._LIVE.config import APIkey, APIsecret
# from shared_functions import has_open_position
# from strategies.General import General


# db = TinyDB('trades.json')

exchange = bybit({
    'apiKey': APIkey,
    'secret': APIsecret,
    'enableRateLimit': True,
    # 'nonce': bybit.milliseconds
    # 'adjustForTimeDifference': True
    # 'verbose': True,
})


def prepare(symbol: str, time: str) -> np.ndarray:
    '''
        Takes the symbol and time 
        returns a dataframe with ohlcv and indicators caculated.
    '''

    bars = exchange.fetch_ohlcv(symbol=symbol, timeframe=time, limit=100)
    df = pd.DataFrame(bars[:-1], columns=['timestamp',
                                          'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    df['rsi20'] = ta.RSI(df['close'], 20)
    # ta.rsi(
    #     close=df['close'], window=20, fillna=False).rsi()

    return df


# the ones above are same as debug i think
# live specific functions


def should_trade(data: pd.DataFrame) -> str:
    '''
       takes the data
       returns a string. F = do nothing, L = Long, S = short
    '''
    last_rsi_value = data['rsi20'].iloc[-1]
    # should long
    if(last_rsi_value > 50):
        return "L"

    # should short
    if(last_rsi_value < 50):
        return "S"

    return "F"


def go_trade(action: str, size: int, symbol: str):
    '''
        takes the action, size and symbol
        opens a position 
    '''

    current_price = float(exchange.fetch_ticker(symbol='ETHUSDT')['close'])
    take_profit = round(current_price + current_price*(0.1/100), 2)
    stop_loss = round(current_price - current_price*(0.1/100), 2)
    # print(f'stoploss = {stop_loss} and profit = {take_profit}')

    # go long and go short
    side = 'buy' if action == 'L' else 'sell'
    params = {'take_profit': take_profit, 'stop_loss': stop_loss} if action == 'L' else {
        'take_profit': stop_loss, 'stop_loss': take_profit}
    # params["reduce_only"] = True

    o = exchange.create_order(symbol, 'market', side,
                              amount=size, params=params)


def update_position():
    pass


def run_bot(time):

    size = 0.05
    symbols = ['ETHUSDT']

    for symbol in symbols:
        # add the necessary indicators this should probably updated?
        data = prepare(symbol, time)

        # def  has_open_position(exchange=exchange, symbol="ETHUSDT")
        in_trade = True

        if(not in_trade):
            print('not in trade')
            action = should_trade(data)
            if (action != 'F'):
                go_trade(action, size, symbol)
                in_trade = True
        elif (in_trade):
            print('in trade')
            # update_position()  # for trailing stoploss

        # after()  # notifications on telegram maybe?


scheduler = BackgroundScheduler()

run_bot('1m')
scheduler.add_job(run_bot, 'interval', ['1m'], seconds=5)
scheduler.start()

keepGoing = True
try:

    while keepGoing:
        keepGoing = True
except (KeyboardInterrupt, SystemExit):

    scheduler.shutdown()


# important what to do:
# move all these functions into a other file where can be called and make it so that the testing can also call it
# then that'll be live plugin feature then after that work on a few basic strategies
# then implement telegram for notifications. and more strates with web3 (part tiem larry) and Machine learning
# then a python kivy/ something like taht app
# lastly a user interface using next and this fully fledged api made with fastapi
