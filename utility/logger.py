import logging
from enum import Enum
from inspect import getframeinfo, stack
from urllib3 import connectionpool
from discord import webhook


class LogLevel(Enum):
    Debug = 1
    Info = 2
    Warning = 3
    Error = 4
    Critical = 5


class Logger:
    _logger = None

    @staticmethod
    def __initialise():
        if Logger._logger is None:
            logging.basicConfig(filename="logs/all.log",
                                format='%(asctime)s-%(levelname)s-%(message)s',
                                filemode='w')
            Logger._logger = logging.getLogger()

            # Setting the threshold of logger to DEBUG
            Logger._logger.setLevel(logging.DEBUG)

            # http CRITICAL level to be logged only
            logging.getLogger(connectionpool.__name__).setLevel(logging.CRITICAL)
            logging.getLogger(webhook.__name__).setLevel(logging.CRITICAL)
        return Logger._logger

    @staticmethod
    def log(msg: str, log_level: LogLevel):
        logger = Logger.__initialise()
        try:
            caller = getframeinfo(stack()[1][0])
            caller_info = "%s-%d-" % (caller.filename, caller.lineno)
        except:
            caller_info = "Exception in logger-"

        if log_level is LogLevel.Info:
            logger.info(caller_info + msg)
        elif log_level is LogLevel.Error:
            logger.error(caller_info + msg)
        elif log_level is LogLevel.Warning:
            logger.warning(caller_info + msg)
        elif log_level is LogLevel.Critical:
            logger.critical(caller_info + msg)
        else:
            logger.debug(caller_info + msg)
