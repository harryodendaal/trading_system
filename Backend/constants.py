import ccxt
from .config import APIkey, APIsecret
EXCHANGE = ccxt.bybit({
    'apiKey': APIkey,
    'secret': APIsecret,
    'options': {
        'recvWindow': 7000,
        'adjustForTimeDifference': True,
    },
    'enableRateLimit': True,
    # 'verbose': True
})
# EXCHANGE = ccxt.bybit({
#     'enableRateLimit': True,
#     'apiKey': APIkey,
#     'secret': APIsecret,
#     'options': {
#         'adjustForTimeDifference': True,
#         'verbose': True,
#         'defaultType': 'spot',
#     },
# })

# really need to get better interface for below zero is just nothing now.
STRATEGIES = ['0', '1', '2', '3']
