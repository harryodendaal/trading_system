import jesse.indicators as ta
from jesse import utils
from jesse.strategies import Strategy, cached

from testing.new_archive.communal_strategy_blocks import trend_from_pivot_points


class the_trading_channel_inspired_strat(Strategy):
    # create another property do this based of of pivot points and then since we are making long trades
    # the trend will be if a ll of pull back is not broken. so when new higher high, cannot brake previous lower low.

    @property
    def uptrend_according_pivot_points(self):
        higher_timeframe_candles = self.get_candles(self.exchange, self.symbol, "12h")

        return trend_from_pivot_points(higher_timeframe_candles, "u")

    @property
    def downtrend_according_pivot_points(self):
        higher_timeframe_candles = self.get_candles(self.exchange, self.symbol, "12h")

        return trend_from_pivot_points(higher_timeframe_candles, "d")

    @property
    def short_trend(self):
        # 15 min
        short_ema = ta.ema(self.candles, 21)
        long_ema = ta.ema(self.candles, 50)

        if short_ema > long_ema:
            return 1
        else:
            return -1

    @property
    def long_trend(self):
        # 1hr
        short_ema = ta.ema(self.get_candles(self.exchange, self.symbol, "12h"), 21)
        long_ema = ta.ema(self.get_candles(self.exchange, self.symbol, "12h"), 50)

        if short_ema > long_ema:
            return 1
        else:
            return -1

    def before(self):
        return

    def should_long(self):
        return self.short_trend == 1 and self.long_trend == 1

    def should_short(self):
        return False

    def should_cancel(self):
        return True

    def should_cancel_entry(self) -> bool:
        return True

    def go_long(self):
        entry_price = self.price
        qty = utils.size_to_qty(self.balance, entry_price)
        self.buy = qty, entry_price

    def go_short(self):
        pass

    def update_position(self):
        if self.short_trend == -1:
            self.liquidate()


# the trading strategy:
# trade on the 1hr timeframe, keep in mind the 1day trend and follow it.
# how to identify regions of support and resistance?
# use ATR for setting stoploss and take profit, by setting it alwyas at 1 atr, then at 2 atr for other reggion.
# use the moving average as a trailing stoploss
# rsi divergence
# candle stick pattern analysis
# also to identify double bottoms... tops


# make these functionalities general and accessible from elsewehere.

###################################################
# day trader = uses 15 min chart
# swing trader = uses 4hr chart
