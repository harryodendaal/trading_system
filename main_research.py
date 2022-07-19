# # # # # # # # # # # # # # #
# imports
# # # # # # # # # # # # # # #
from pprint import pprint
from typing import Union

import jesse.helpers as jh
import jesse.indicators as ta
from jesse import utils
from jesse.research import (backtest, candles_from_close_prices,
                            candlestick_chart, get_candles, import_candles)
from jesse.strategies import Strategy
from research_strategies.death_cross_20_40 import Death_cross_20_40
# # # # # # # # # # # # # # #
# generate fake candles
# # # # # # # # # # # # # # #

fake_candles01 = get_candles("Bybit Perpetual", "BTC-USDT",
                             "15m", "2022-05-02", "2022-05-10")

# # # # # # # # # # # # # # #
# strategy
# # # # # # # # # # # # # # #

# # # # # # # # # # # # # # #
# prepare inputs
# # # # # # # # # # # # # # #
exchange_name = 'Bybit Perpetual'
symbol = 'BTC-USDT'
timeframe = '15m'
config = {
    'starting_balance': 10_000,
    'fee': 0,
    'futures_leverage': 2,
    'futures_leverage_mode': 'cross',
    'exchange': exchange_name,
    'settlement_currency': 'USDT',
    'warm_up_candles': 0
}
routes = [
    {'exchange': exchange_name, 'strategy': Death_cross_20_40,
     'symbol': symbol, 'timeframe': timeframe}
]
extra_routes = []
candles = {
    # keys must be in this format: 'Fake Exchange-BTC-USDT'
    jh.key(exchange_name, symbol): {
        'exchange': exchange_name,
        'symbol': symbol,
        'candles': fake_candles01,
    },
}

# # # # # # # # # # # # # # #
# execute backtest
# # # # # # # # # # # # # # #
result = backtest(
    config,
    routes,
    extra_routes,
    candles,
    generate_charts=True
)
# to access the metrics dict:
result['metrics']
# to access the charts string (path of the generated file):
result['charts']
# to access the logs list:
pprint(result['charts'])

# show chart
candlestick_chart(fake_candles01)
# ta testing
# pprint(ta.ema(fake_candles01, 20))
