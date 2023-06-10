class Strategy:
    def __init__(self) -> None:
        pass

    def before(self):
        pass

    def update_position(self, symbol):
        pass

    def should_cancel_entry(self):
        pass

    def should_long(self):
        pass

    def should_short(self):
        pass

    def go_long(self):
        pass

    def go_short(self):
        pass

    def after(self):
        pass


# events, filters and the more advanced features.
