# maybe import in a better way? also the func names the same and maybe have default here so dont for example
# have to import before

from strategies.__research_strategies import death_cross_20_40
from strategies.__research_strategies import SimpleBollinger

# should_cancel, should_cancel_entry, should_long, should_short, update_position, before)
from constants import STRATEGIES


def live_before(self):
    STRATEGY = STRATEGIES[self.strategy]

    if STRATEGY == '1':
        return death_cross_20_40.before(self)
    elif STRATEGY == '2':
        return SimpleBollinger.before(self)


def live_update_position(self):
    STRATEGY = STRATEGIES[self.strategy]

    if STRATEGY == '1':
        return death_cross_20_40.update_position(self)
    elif STRATEGY == '2':
        return SimpleBollinger.update_position(self)


def live_should_short(self):
    STRATEGY = STRATEGIES[self.strategy]

    if STRATEGY == '1':
        return death_cross_20_40.should_short(self)
    elif STRATEGY == '2':
        return SimpleBollinger.should_short(self)


def live_should_long(self):
    STRATEGY = STRATEGIES[self.strategy]

    if STRATEGY == '1':
        return death_cross_20_40.should_long(self)
    elif STRATEGY == '2':
        return SimpleBollinger.should_long(self)


def live_should_cancel_entry(self):
    STRATEGY = STRATEGIES[self.strategy]

    if STRATEGY == '1':
        return death_cross_20_40.should_cancel_entry(self)
    elif STRATEGY == '2':
        return SimpleBollinger.should_cancel_entry(self)


def live_should_cancel(self):
    STRATEGY = STRATEGIES[self.strategy]

    if STRATEGY == '1':
        return death_cross_20_40.should_cancel(self)
    elif STRATEGY == '2':
        return SimpleBollinger.should_cancel(self)

# def live_after(self):
# 	after(self)
# 	return
