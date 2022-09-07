import logging
from datetime import datetime

from singleton import Singleton


class LoggerFactory(metaclass=Singleton):
    _LOG = None

    @staticmethod
    def __create_logger(log_file):
        """
        A private method that interacts with the python
        logging module
        """
        # set the logging format
        log_format = "%(asctime)s|%(levelname)s|%(message)s"

        # Initialize the class variable with logger object
        LoggerFactory._LOG = logging.getLogger(log_file)

        logging.basicConfig(filename=log_file, filemode="w",
                            format=log_format, datefmt="%Y-%m-%d %H:%M:%S")
        logging.getLogger('werkzeug').setLevel(logging.WARNING)
        LoggerFactory._LOG.setLevel(level=logging.DEBUG)
        return LoggerFactory._LOG

    @staticmethod
    def get_logger(log_folder):
        """
        A static method called by other modules to initialize logger in
        their own module
        """
        logfile = datetime.now().strftime('%Y_%m_%d_%H_%M.log')
        log = log_folder + "\\" + logfile
        logger = LoggerFactory.__create_logger(log_file=log)

        # return the logger object
        return logger
