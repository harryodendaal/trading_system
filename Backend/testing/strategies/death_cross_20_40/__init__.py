import jesse.indicators as ta
from jesse import utils
from jesse.strategies import Strategy, cached
from strategies.__research_strategies.death_cross_20_40 import (
    should_cancel,
    should_long,
    should_short,
    update_position,
)


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

    def should_short(self):
        return should_short(self)

    def should_cancel(self):
        return should_cancel(self)

    def should_cancel_entry(self) -> bool:
        return super().should_cancel_entry()

    def go_long(self):
        # Open long position and use entire balance to buy
        qty = utils.size_to_qty(self.balance, self.price, fee_rate=self.fee_rate)

        self.buy = qty, self.price

    def go_short(self):
        # Open short position and use entire balance to sell
        qty = utils.size_to_qty(self.balance, self.price, fee_rate=self.fee_rate)

        self.sell = qty, self.price

    def update_position(self) -> None:
        update_position(self)
