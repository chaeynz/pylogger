"""This module provides simple access to creating logs"""
import logging
import os
from datetime import datetime
# pylint: disable=all

LOGFILE = "" # Define yourself

class Logger:
    """
    Provides logging capabilities
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            logger = logging.getLogger('Logger') 

            # File Handler with milliseconds
            file_formatter = logging.Formatter('[%(asctime)s.%(msecs)03d] %(levelname)s: %(message)s',
                                                datefmt='%Y-%m-%d %H:%M:%S')
            current_time = datetime.now().strftime('%Y-%m-%d')
            if not os.path.exists('logs'):
                os.makedirs('logs')
            file_handler = logging.FileHandler(f'logs/{current_time}_{LOGFILE}.log')
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

            # Stream Handler without milliseconds
            stream_formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%H:%M')
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(stream_formatter)
            stream_handler.addFilter(cls.ColorFilter())
            logger.addHandler(stream_handler)

            logger.setLevel(logging.INFO)

            cls._instance.logger = logger

        return cls._instance

    class ColorFilter(logging.Filter):
        def filter(self, record):
            if record.levelname == 'DEBUG':
                record.msg = "\033[36mDEBUG\033[0m: " + record.msg
            elif record.levelname == 'INFO':
                record.msg = "\033[92mINFO\033[0m: " + record.msg
            elif record.levelname == 'WARNING':
                record.msg = "\033[33mWARNING:\033[0m: " + record.msg
            elif record.levelname == 'ERROR':
                record.msg = "\033[31mERROR\033[0m: " + record.msg
            elif record.levelname == 'CRITICAL':
                record.msg = "\033[91mCRITICAL\033[0m: " + record.msg
            else:
                return False

            return True

    def log_info(self, message):
        self.logger.info(message)

    def log_debug(self, message): 
        self.logger.debug(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_critical(self, message):
        self.logger.critical(message)


# Creation of logger instance and methods
logger = Logger()
log_debug = logger.log_debug
log_info = logger.log_info
log_warning = logger.log_warning
log_error = logger.log_error
log_critical = logger.log_critical
    
