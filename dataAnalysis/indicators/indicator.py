from abc import abstractmethod


class Indicator:
    """
    This is the interface class which is implemented by the individual child class.
    """

    def __init__(self, config, data):
        self.config = config
        self.data = data

    @abstractmethod
    def do_analysis(self, selected_stocks: list):
        pass

    # Set data on which the indicator calculation is to be done
    @abstractmethod
    def __get_result(self, col_data):
        pass
