import time
import traceback

from conf.conf_editor import read
from orchestrator.discord_routes import DiscordRoutes
from utility.reader import read_config
from utility.logger import LogLevel
from utility.aggregator import singletons
from dataFetch.yfinance_live_data import YFinanceLiveData
from dataAnalysis.indicators.rsi import RsiConfig, TickersRsi
from pytz import timezone
import datetime


class Orchestrator:
    def __init__(self, user_config: dict, indicator_config: dict, selected_stocks_config: dict, discord_config: dict):
        try:
            self.indicator_results = {}
            self.user_config = user_config
            self.indicator_config = indicator_config
            self.selected_stocks_config = selected_stocks_config

            self.discord_config = discord_config

            # First initialise discord messenger with general channel
            self.logger = singletons['logger']
            self.discord_messenger = singletons['discord_messenger']
            self.discord_routes = DiscordRoutes(name="query_routes", listener_config=self.discord_config['listener'],
                                                user_config=self.user_config)

        except Exception as e:
            self.logger.log(msg=f"exception during config read: {traceback.format_exc()}", log_level=LogLevel.Critical)
            self.discord_messenger.send_message(channel="general", msg=f"exception during config read: {str(e)}",
                                                title=f"{type(e).__name__}")

    def run(self):
        selected_stocks = self.selected_stocks_config['to_buy'] + self.selected_stocks_config['to_sell']
        selected_stocks = [stock + ".NS" for stock in selected_stocks]

        while not read()['user_config']['stop']:
            try:
                nse_delay = self.wait_for_next()
                start_time = time.time()

                # fetch data till current
                stock_config = {
                    'tickers': selected_stocks,
                    'interval': self.user_config['yf_interval'],
                    'period': self.user_config['yf_period']
                }
                yfinance = YFinanceLiveData(stock_config)
                data = yfinance.get_tickers_historical_data()
                time.sleep(20)
                '''
                # RSI analysis
                rsi_config = RsiConfig(name="rsi", timeperiod=self.indicator_config['rsi']['window'],
                                       ohlc=self.indicator_config['rsi']['ohlc'],
                                       upper=self.indicator_config['rsi']['upper'],
                                       lower=self.indicator_config['rsi']['lower'])
                tickers_rsi = TickersRsi(name="rsi", config=rsi_config, data=data)
                tickers_rsi.do_analysis(selected_stocks=selected_stocks)
                self.indicator_results[tickers_rsi.name] = tickers_rsi.get_result()

                self.discord_routes.set_indicator_results(self.indicator_results)

                end_time = time.time()
                # delay = nse_delay * 60 - (end_time - start_time)
                delay = 60

                # if delay is more than 12hrs, stop this instance and cron will run another instance tomorrow
                if delay >= 12 * 60 * 60 and not self.user_config['debugging']:
                    msg = f"stopping with this batch, next batch will be starting tomorrow"
                    self.logger .log(msg=msg, log_level=LogLevel.Info)
                    self.discord_messenger.send_message(msg=msg, channel="general", title="stop")
                    self.stop()
                    break
                else:
                    msg = f"starting next batch after {delay}s"
                    self.logger .log(msg=msg, log_level=LogLevel.Info)
                    self.discord_messenger.send_message(msg=msg, channel="general", title="next batch")
                    time.sleep(delay)
                    # self.user_config = read_config(self.user_config_file)
                '''
            except Exception as e:
                self.logger.log(msg=f"exception during run: {traceback.format_exc()}", log_level=LogLevel.Critical)
                self.discord_messenger.send_message("general", msg=f"exception during run: {str(e)}",
                                                    title=f"{type(e).__name__}")
        self.logger.log(msg=f"Stopping orchestrator loop", log_level=LogLevel.Critical)
        # self.discord_messenger.send_message("general", msg=f"Stopping orchestrator loop")

    def wait_for_next(self):
        time_zone = timezone("Asia/Kolkata")
        ind_time = datetime.datetime.now(timezone("Asia/Kolkata"))

        nse_open = self.user_config['nse']['open'].split(':')
        nse_open_hour = int(nse_open[0])
        nse_open_minute = int(nse_open[1])
        nse_close = self.user_config['nse']['close'].split(':')
        nse_close_hour = int(nse_close[0])
        nse_close_minute = int(nse_close[1])

        day_of_week = ind_time.isoweekday()
        today_open_time = datetime.datetime(year=ind_time.year, month=ind_time.month, day=ind_time.day,
                                            hour=nse_open_hour, minute=nse_open_minute, tzinfo=time_zone)
        today_close_time = datetime.datetime(year=ind_time.year, month=ind_time.month, day=ind_time.day,
                                             hour=nse_close_hour, minute=nse_close_minute, tzinfo=time_zone)

        def get_day_delay_minutes():
            delay_mins = self.user_config['poll_interval']

            # Saturday
            if day_of_week == 6:
                monday_open_time = today_open_time + datetime.timedelta(hours=24 * 2)
                delay_mins = (monday_open_time - ind_time).total_seconds() / 60
            # Sunday
            elif day_of_week == 7:
                monday_open_time = today_open_time + datetime.timedelta(hours=24)
                delay_mins = (monday_open_time - ind_time).total_seconds() / 60
            else:
                if today_open_time <= ind_time <= today_close_time:
                    delay_mins = self.user_config['poll_interval']
                else:
                    if ind_time < today_open_time:
                        delay_mins = (today_open_time - ind_time).total_seconds() / 60
                    elif ind_time > today_close_time:
                        tomorrow_open_time = today_open_time + datetime.timedelta(hours=24)
                        delay_mins = (tomorrow_open_time - ind_time).total_seconds() / 60

                        # Friday end
                        if day_of_week == 5:
                            monday_open_time = today_open_time + datetime.timedelta(hours=24 * 3)
                            delay_mins = (monday_open_time - ind_time).total_seconds() / 60

            return delay_mins

        delay_minutes = get_day_delay_minutes()
        return delay_minutes

    def stop(self):
        try:
            self.discord_routes.stop()
            self.logger.log(msg=f"Stopping Orchestrator", log_level=LogLevel.Info)
            self.discord_messenger.send_message(channel="general", msg=f"Stopping Orchestrator", title="stop orchestrator")
        except Exception as e:
            self.logger.log(msg=f"Exception while stopping Orchestrator {traceback.format_exc()}", log_level=LogLevel.Info)
            self.discord_messenger.send_message(channel="general", msg=f"Exception while stopping Orchestrator {str(e)}",
                                          title=f"{type(e).__name__}")
