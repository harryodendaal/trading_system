from ctypes import Union

from ccxt import bybit
from numpy import true_divide

from main_research import ResearchStrategy


def should_liquidate(self):
    # for now do the liquidate for this function will later check which function is being run
    # so will have different should liquidate checks
    # rename reserch strategy to live plugin? also maybe make all of it into one unified function?
    if self.is_long and self.fast_sma < self.slow_sma:
        return True

    if self.is_short and self.fast_sma > self.short_sma:
        return True


def should_long(self):
    return self.short_ema > self.long_ema


def should_short(self):
    return self.short_ema < self.long_ema
