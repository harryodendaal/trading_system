def before(self):
    return


def should_long(self):
    # return true if close is above EMA and MACD line is above signal line
    if self.close > self.ema and self.macd[0] > self.macd[1]:
        return True
    return False


def should_short(self):
    return False


def should_cancel(self):
    return True


def should_cancel_entry(self) -> bool:
    return True


def update_position(self):
    # Close the position when MACD crosses below the signal line and closing prices is less than 100EMA
    if self.macd[0] < self.macd[1] and self.close < self.ema:
        self.liquidate("ETHUSDT")


# This is set up for optimization but if you just want to backtest with your own values then change the default value only.
# def hyperparameters(self):
#     return [
#         {'name': 'ema', 'type': int, 'min': 50, 'max': 200, 'default': 100},
#         {'name': 'fastperiod', 'type': int,
#          'min': 10, 'max': 18, 'default': 12},
#         {'name': 'slowperiod', 'type': int,
#          'min': 19, 'max': 36, 'default': 26},
#         {'name': 'signalperiod', 'type': int,
#          'min': 3, 'max': 9, 'default': 9},
#     ]
