import time

from utility.reader import read_config
from utility.logger import Logger, LogLevel
from dataFetch.yfinanceLiveData import YFinanceLiveData
from dataAnalysis.indicators.rsi import RsiConfig, TickersRsi


class Orchestrator:
    def __init__(self, user_config: str, indicator_config: str, selected_stocks_config: str):
        try:
            self.user_config = read_config(user_config)
            self.indicator_config = read_config(indicator_config)
            self.selected_stocks_config = read_config(selected_stocks_config)
        except Exception as e:
            Logger.log(msg=f"exception during config read: {str(e)}", log_level=LogLevel.Critical)

    def run(self):
        selected_stocks = self.selected_stocks_config['to_buy'] + self.selected_stocks_config['to_sell']
        selected_stocks = [stock + ".NS" for stock in selected_stocks]

        while not self.user_config['stop']:
            try:
                # fetch data till current
                stock_config = {
                    'tickers': selected_stocks,
                    'interval': self.user_config['yf_interval'],
                    'period': self.user_config['yf_period']
                }
                yfinance = YFinanceLiveData(stock_config)
                data = yfinance.get_ticker_data()

                # RSI analysis
                rsi_config = RsiConfig(name="RSI", timeperiod=self.indicator_config['rsi']['window'],
                                       ohlc=self.indicator_config['rsi']['ohlc'],
                                       upper=self.indicator_config['rsi']['upper'],
                                       lower=self.indicator_config['rsi']['lower'])
                tickers_rsi = TickersRsi(rsi_config, data=data)
                tickers_rsi.do_analysis(selected_stocks=selected_stocks)

                time.sleep(1)

            except Exception as e:
                Logger.log(msg=f"exception during run: {str(e)}", log_level=LogLevel.Critical)







