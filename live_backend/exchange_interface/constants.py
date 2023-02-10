import ccxt

from .config import APIkey, APIsecret

EXCHANGE = ccxt.bybit(
    {
        "apiKey": APIkey,
        "secret": APIsecret,
        "options": {
            "recvWindow": 10000,
            "adjustForTimeDifference": True,
        },
        "enableRateLimit": True,
        # 'verbose': True
    }
)


# really need to get better interface for below zero is just nothing now.
STRATEGIES = ["0", "1", "2", "3"]
