import logging
from enum import Enum
from inspect import getframeinfo, stack
from urllib3 import connectionpool
from discord import webhook
from pathlib import Path
from datetime import datetime

from utility.singleton import Singleton


class LogLevel(Enum):
    Debug = 1
    Info = 2
    Warning = 3
    Error = 4
    Critical = 5


class Logger(metaclass=Singleton):
    # TODO1: update logger with DI for log path
    def __init__(self):
        self.logger = None
        self.log_folder = Path("logs")
        self.logfile = datetime.now().strftime('%Y_%m_%d_%H_%M.log')
        self.all_log = self.log_folder / self.logfile

        # create a log file if not exist
        file_handler = logging.FileHandler(self.all_log, mode="w", encoding=None, delay=False)
        file_handler.close()

        self.all_log = self.all_log.resolve(strict=True).as_posix()
        logging.basicConfig(filename=self.all_log,
                            format='%(asctime)s-%(levelname)s-%(message)s',
                            filemode='w')
        self.logger = logging.getLogger()

        # Setting the threshold of logger to DEBUG
        self.logger.setLevel(logging.DEBUG)

        # http CRITICAL level to be logged only
        logging.getLogger(connectionpool.__name__).setLevel(logging.CRITICAL)
        logging.getLogger(webhook.__name__).setLevel(logging.CRITICAL)
        logging.getLogger('discord').setLevel(logging.CRITICAL)

    def log(self, msg: str, log_level: LogLevel):
        try:
            caller = getframeinfo(stack()[1][0])
            caller_info = "%s-%d-" % (caller.filename, caller.lineno)
        except:
            caller_info = "Exception in logger-"

        if log_level is LogLevel.Info:
            self.logger.info(caller_info + msg)
        elif log_level is LogLevel.Error:
            self.logger.error(caller_info + msg)
        elif log_level is LogLevel.Warning:
            self.logger.warning(caller_info + msg)
        elif log_level is LogLevel.Critical:
            self.logger.critical(caller_info + msg)
        else:
            self.logger.debug(caller_info + msg)
