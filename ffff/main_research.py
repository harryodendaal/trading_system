# # # # # # # # # # # # # # #
# imports
# # # # # # # # # # # # # # #
from cmath import pi
from pickle import TRUE
from pprint import pprint
from re import L
from typing import Union
import numpy as np
import jesse.helpers as jh
import jesse.indicators as ta
from jesse import utils
from jesse.research import (backtest, candles_from_close_prices,
                            candlestick_chart, get_candles, import_candles)
from jesse.strategies import Strategy
from strategies.death_cross_20_40 import death_cross_20_40
import matplotlib.pyplot as plt
# # # # # # # # # # # # # # #
# generate fake candles
# # # # # # # # # # # # # # #
# import_candles("Bybit USDT Perpetual", "BTC-USDT",
#                "2022-08-01", show_progressbar=True)

fake_candles01 = get_candles("Bybit USDT Perpetual", "BTC-USDT",
                             "4h", "2022-09-10", "2022-10-06")

# print((max(fake_candles01[1:3][:, 3])))
# candles = np.flip(fake_candles01, 0)

# print(max(candles[32: 32+10+1][:, 3]))

# if (candles[32][3] >= max(candles[32: 32+10+1][:, 3])):
#     print("bigger than left")
#     # the current candle is bigger than 10 to it's right.
#     if (candles[32][3] >= max(candles[32-10-1: 32][:, 3])):
#         print('bigger than right')
#         print("the pivot point high:", candles[32][3])


# candlestick_chart(candles[0:50])
# plt.savefig(str("g") + " output.png")


def trend_from_pivot_points(candles: np.ndarray):

    # so find previous 2 ups and downs
    # if higher low then medium uptrend
    # if that and higher high then strong uptrend.
    pp_length = 10
    candles = np.flip(candles, 0)
    pivot_highs = {}
    pivot_lows = {}

    for idx in range(1+pp_length, len(candles)):
        if (idx > len(candles) - (pp_length+1)):
            break

        # search for pivot highs

        # the current candle is bigger than 10 to it's left
        if (candles[idx][3] >= max(candles[idx: idx + (pp_length+1)][:, 3])):
            # the current candle is bigger than 10 to it's right.
            if (candles[idx][3] >= max(candles[idx - (pp_length + 1): idx][:, 3])):
                # store both idx and value.
                pivot_highs[idx] = candles[idx][3]

        # search for pivot lows
        if (candles[idx][3] <= min(candles[idx: idx + (pp_length+1)][:, 3])):
            # the current candle is bigger than 10 to it's right.
            if (candles[idx][3] <= min(candles[idx - (pp_length + 1): idx][:, 3])):
                # store both idx and value.
                pivot_lows[idx] = candles[idx][3]

        if (len(pivot_highs) > 2 and len(pivot_lows) > 2):
            break

    pivot_low_keys = (list(pivot_lows.keys()))
    pivot_high_keys = (list(pivot_highs.keys()))
    print(pivot_highs)
    print(pivot_lows[pivot_low_keys[0]])
    print(pivot_highs[pivot_high_keys[0]])

    # previous low is not lower and previous high is higher
    if (pivot_lows[pivot_low_keys[0]] > pivot_lows[pivot_low_keys[1]]):
        if (pivot_highs[pivot_high_keys[0]] > pivot_highs[pivot_high_keys[1]]):
            print('uptrend')
            return True
    # the second low cannot be broken.
    print('not uptrend')
    return False


trend_from_pivot_points(fake_candles01)


# # # # # # # # # # # # # # #
# strategy
# # # # # # # # # # # # # # #

# # # # # # # # # # # # # # #
# prepare inputs
# # # # # # # # # # # # # # #
# exchange_name = 'Bybit Perpetual'
# symbol = 'BTC-USDT'
# timeframe = '15m'
# config = {
#     'starting_balance': 10_000,
#     'fee': 0,
#     'futures_leverage': 2,
#     'futures_leverage_mode': 'cross',
#     'exchange': exchange_name,
#     'settlement_currency': 'USDT',
#     'warm_up_candles': 0
# }
# routes = [
#     {'exchange': exchange_name, 'strategy': death_cross_20_40,
#      'symbol': symbol, 'timeframe': timeframe}
# ]
# extra_routes = []
# candles = {
#     # keys must be in this format: 'Fake Exchange-BTC-USDT'
#     jh.key(exchange_name, symbol): {
#         'exchange': exchange_name,
#         'symbol': symbol,
#         'candles': fake_candles01,
#     },
# }

# # # # # # # # # # # # # # # #
# # execute backtest
# # # # # # # # # # # # # # # #
# result = backtest(
#     config,
#     routes,
#     extra_routes,
#     candles,
#     generate_charts=True
# )
# # to access the metrics dict:
# result['metrics']
# # to access the charts string (path of the generated file):
# result['charts']
# # to access the logs list:
# pprint(result['charts'])

# # show chart
# candlestick_chart(fake_candles01)
# # ta testing
# # pprint(ta.ema(fake_candles01, 20))
