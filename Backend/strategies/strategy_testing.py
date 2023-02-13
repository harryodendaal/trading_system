from Backend.strategies.strategy.death_cross_20_40 import DeathCross as Particular


def before(self):
    return Particular.before(self)


def update_position(self):
    return Particular.update_position(self)


def should_cancel_entry(self):
    return Particular.should_cancel_entry(self)


def should_long(self):
    return Particular.should_long(self)


def should_short(self):
    return Particular.should_short(self)


def go_long(self):
    return Particular.go_long(self)


def go_short(self):
    return Particular.go_short(self)


def after(self):
    return Particular.after(self)
