import jesse.indicators as ta
from jesse import utils
from jesse.strategies import Strategy, cached

from strategies.__research_strategies.death_cross_20_40 import (go_long, go_short,
                                                                long_ema, short_ema,
                                                                should_cancel,
                                                                should_long,
                                                                should_short,
                                                                update_position)


class death_cross_20_40(Strategy):
    @property
    def short_ema(self):
        # returns the new candles ema value
        return ta.ema(self.candles, 20)

    @property
    def long_ema(self):
        return ta.ema(self.candles, 40)

    def should_long(self):
        return should_long(self)
        # return self.short_ema > self.long_ema

    def should_short(self):
        return should_short(self)
        # return self.short_ema < self.long_ema

    def should_cancel(self):
        return should_cancel(self)

    def go_long(self):
        go_long(self)

    def go_short(self):
        go_short(self)

    def update_position(self) -> None:
        update_position(self)
