# maybe import in a better way? also the func names the same and maybe have default here so dont for example
# have to import before

from .strategies.__research_strategies import death_cross_20_40
from .strategies.__research_strategies import simple_bollinger
from .strategies.__research_strategies import macd_ema

# should_cancel, should_cancel_entry, should_long, should_short, update_position, before)
from .constants import STRATEGIES


def live_before(self):
    strategy = STRATEGIES[self.strategy]

    if strategy == '1':
        return death_cross_20_40.before(self)
    elif strategy == '2':
        return simple_bollinger.before(self)
    elif strategy == '3':
        return macd_ema.before(self)


def live_update_position(self):
    strategy = STRATEGIES[self.strategy]

    if strategy == '1':
        return death_cross_20_40.update_position(self)
    elif strategy == '2':
        return simple_bollinger.update_position(self)
    elif strategy == '3':
        return macd_ema.update_position(self)


def live_should_short(self):
    strategy = STRATEGIES[self.strategy]

    if strategy == '1':
        return death_cross_20_40.should_short(self)
    elif strategy == '2':
        return simple_bollinger.should_short(self)
    elif strategy == '3':
        return macd_ema.should_short(self)


def live_should_long(self):
    strategy = STRATEGIES[self.strategy]

    if strategy == '1':
        return death_cross_20_40.should_long(self)
    elif strategy == '2':
        return simple_bollinger.should_long(self)
    elif strategy == '3':
        return macd_ema.should_long(self)


def live_should_cancel_entry(self):
    strategy = STRATEGIES[self.strategy]

    if strategy == '1':
        return death_cross_20_40.should_cancel_entry(self)
    elif strategy == '2':
        return simple_bollinger.should_cancel_entry(self)
    elif strategy == '3':
        return macd_ema.should_cancel_entry(self)


def live_should_cancel(self):
    strategy = STRATEGIES[self.strategy]

    if strategy == '1':
        return death_cross_20_40.should_cancel(self)
    elif strategy == '2':
        return simple_bollinger.should_cancel(self)
    elif strategy == '3':
        return macd_ema.should_cancel(self)

        # def live_after(self):
        # 	after(self)
        # 	return
