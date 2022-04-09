import time
import traceback

from orchestrator.discord_routes import DiscordRoutes
from utility.reader import read_config
from utility.logger import Logger, LogLevel
from utility.discordBot.discord_messenger import DiscordMessenger
from dataFetch.yfinance_live_data import YFinanceLiveData
from dataAnalysis.indicators.rsi import RsiConfig, TickersRsi
from pytz import timezone
import datetime


class Orchestrator:
    def __init__(self, user_config: str, indicator_config: str, selected_stocks_config: str, discord_config: str):
        try:
            self.user_config_file = user_config
            self.user_config = read_config(user_config)
            self.indicator_config = read_config(indicator_config)
            self.selected_stocks_config = read_config(selected_stocks_config)

            self.discord_config = read_config(discord_config)

            # First initialise discord messenger with general channel
            DiscordMessenger.initialise(self.discord_config['messenger']['webhook']['general'])
            for name, url in self.discord_config['messenger']['webhook'].items():
                DiscordMessenger.add_webhook(webhook_name=name, webhook_url=url)

            self.discord_routes = DiscordRoutes(name="query_routes", listener_config=self.discord_config['listener'])

        except Exception as e:
            Logger.log(msg=f"exception during config read: {traceback.format_exc()}", log_level=LogLevel.Critical)
            DiscordMessenger.send_message(channel="general", msg=f"exception during config read: {str(e)}")

    def run(self):
        selected_stocks = self.selected_stocks_config['to_buy'] + self.selected_stocks_config['to_sell']
        selected_stocks = [stock + ".NS" for stock in selected_stocks]

        while not self.user_config['stop']:
            try:
                nse_delay = self.is_nse_open()
                start_time = time.time()

                # DiscordBot.send_message(msg=str(start_time), channel=DiscordBotChannel.GENERAL)
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
                tickers_rsi = TickersRsi(name="Rsi", config=rsi_config, data=data)
                tickers_rsi.do_analysis(selected_stocks=selected_stocks)

                end_time = time.time()
                delay = nse_delay * 60 - (end_time - start_time)

                msg = f"starting next batch after {delay}s"
                Logger.log(msg=msg, log_level=LogLevel.Info)
                DiscordMessenger.send_message(msg=msg, channel="general")
                time.sleep(delay)
                self.user_config = read_config(self.user_config_file)

            except Exception as e:
                Logger.log(msg=f"exception during run: {traceback.format_exc()}", log_level=LogLevel.Critical)
                DiscordMessenger.send_message("general", msg=f"exception during run: {str(e)}")

    def is_nse_open(self):
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
            elif day_of_week == 0:
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
            Logger.log(msg=f"Stopping {self.__name__}", log_level=LogLevel.Info)
            DiscordMessenger.send_message(channel="general", msg=f"Stopping {self.__name__}")
        except Exception as e:
            Logger.log(msg=f"Exception while stopping {self.__name__} {traceback.format_exc()}", log_level=LogLevel.Info)
            DiscordMessenger.send_message(channel="general", msg=f"Exception while stopping {self.__name__} {str(e)}")
