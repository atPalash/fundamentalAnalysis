from dataAnalysis.indicators.config import Config
from dataAnalysis.indicators.indicator import Indicator
from utility.logger import Logger, LogLevel

import talib
import pandas


class RsiConfig(Config):
    def __init__(self, name, timeperiod=14, ohlc="Close", upper=70, lower=30):
        super().__init__(name)
        self.timeperiod = timeperiod
        self.ohlc = ohlc
        self.upper = upper
        self.lower = lower


class TickersRsi(Indicator):
    def __init__(self, config: RsiConfig, data: pandas.DataFrame):
        super().__init__(config, data)

    def do_analysis(self, selected_stocks: list):
        try:
            for stock in selected_stocks:
                # compute indicator analysis
                rsi_result = self.__get_result(self.data[self.config.ohlc][stock])
                # Logger.log(msg=f"{stock} Rsi value={rsi_result[-1]}", log_level=LogLevel.Info)

                if rsi_result[-1] > self.config.upper:
                    Logger.log(msg=f"Overbought {stock}", log_level=LogLevel.Info)

                if rsi_result[-1] < self.config.lower:
                    Logger.log(msg=f"Oversold {stock}", log_level=LogLevel.Info)
        except Exception as e:
            Logger.log(msg=f"exception during rsi analysis: {str(e)}", log_level=LogLevel.Critical)

    def __get_result(self, col_data):
        rsi = talib.RSI(col_data, timeperiod=self.config.timeperiod)
        return rsi


