# from pprint import pprint
# from typing import Union

# import jesse.helpers as jh
# import jesse.indicators as ta
# from jesse import utils

# from jesse.strategies import Strategy


# # properties
# def short_ema(self):
#     # returns the new candles ema value
#     return ta.ema(self.candles, 20)


# def long_ema(self):
#     return ta.ema(self.candles, 40)
# # normal functions


def should_long(self):
    # 20 > 40 ; blue > red
    return self.short_ema > self.long_ema


def should_short(self):
    return self.short_ema < self.long_ema


def should_cancel(self):
    return True


# def go_long(self):
#     qty = utils.size_to_qty(
#         self.capital, self.price, fee_rate=self.fee_rate)
#     self.buy = qty, self.price
#     # go_long_util(self)


# def go_short(self):
#     qty = utils.size_to_qty(
#         self.capital, self.price, fee_rate=self.fee_rate)
#     self.sell = qty, self.price


def update_position(self) -> None:
    #  If there exist long position, but the signal shows Death Cross, then close the position, and vice versa.
    # should_liquidate()
    if self.is_long and self.short_ema < self.long_ema:
        self.liquidate()

    if self.is_short and self.short_ema > self.long_ema:
        self.liquidate()
        # update_position_util(self)
