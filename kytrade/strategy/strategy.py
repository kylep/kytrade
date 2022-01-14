"""Trading strategy"""


class BaseDailyStrategy:
    def __init__(self, portfolio):
        """Trading strategy"""
        self.portfolio = portfolio

    def at_open():
        """Action to perform at open"""
        pass

    def at_close():
        """Action to perform at market close"""
        pass

    def at_condition(conditions: list):
        """accepts list of dicts [{condition_function, action_function}]"""
        pass
