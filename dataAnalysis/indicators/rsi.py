import traceback

from dataAnalysis.indicators.config import Config
from dataAnalysis.indicators.indicator import Indicator
from utility.discord_bot import DiscordBot, DiscordBotChannel
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


_rsi_above_upper_stocks = {}
_rsi_below_lower_stocks = {}


class TickersRsi(Indicator):
    def __init__(self, config: RsiConfig, data: pandas.DataFrame):
        super().__init__(config, data)

    def do_analysis(self, selected_stocks: list):
        try:
            for stock in selected_stocks:
                # compute indicator analysis
                rsi_result = self.__get_result(self.data[self.config.ohlc][stock])
                # Logger.log(msg=f"{stock} Rsi value={rsi_result[-1]}", log_level=LogLevel.Info)
                msg = f"{stock}: rsi={rsi_result[-1]}"

                if rsi_result[-1] > self.config.upper:
                    if _rsi_above_upper_stocks.get(stock) is None:
                        Logger.log(msg=msg, log_level=LogLevel.Info)
                        DiscordBot.send_message(DiscordBotChannel.SELL, msg)
                        _rsi_above_upper_stocks[stock] = rsi_result[-1]
                    else:
                        _rsi_above_upper_stocks[stock] = rsi_result[-1]
                elif rsi_result[-1] < self.config.lower:
                    if _rsi_below_lower_stocks.get(stock) is None:
                        Logger.log(msg=msg, log_level=LogLevel.Info)
                        DiscordBot.send_message(DiscordBotChannel.BUY, msg)
                        _rsi_below_lower_stocks[stock] = rsi_result[-1]
                    else:
                        _rsi_below_lower_stocks[stock] = rsi_result[-1]
                else:
                    if _rsi_below_lower_stocks.get(stock) is not None:
                        _rsi_below_lower_stocks.pop(stock)
                    elif _rsi_above_upper_stocks.get(stock) is not None:
                        _rsi_above_upper_stocks.pop(stock)
        except Exception as e:
            Logger.log(msg=f"exception during rsi analysis: {traceback.format_exc()}", log_level=LogLevel.Critical)

    def __get_result(self, col_data):
        rsi = talib.RSI(col_data, timeperiod=self.config.timeperiod)
        return rsi


