import logging
from src.utils.logging.color_palette import RESET, GREEN, WHITE, YELLOW, MAGENTA, RED


class ColoredLogHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__()
        self.setLevel(logging.DEBUG)
        self.setFormatter(self.__LogFormatter())

    class __LogFormatter(logging.Formatter):
        __FORMAT_DEBUG = '[%(asctime)s] [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)'
        __FORMAT_INFO = '[%(asctime)s] [%(levelname)s] %(message)s'
        __FORMAT_WARNING = '[%(asctime)s] [%(levelname)s] %(message)s'
        __FORMAT_ERROR = '[%(asctime)s] [%(levelname)s] %(message)s'
        __FORMAT_CRITICAL = '[%(asctime)s] [%(levelname)s] %(message)s (%(filename)s:%(lineno)d)'

        FORMATS = {
            logging.DEBUG: WHITE + __FORMAT_DEBUG + RESET,
            logging.INFO: GREEN + __FORMAT_INFO + RESET,
            logging.WARNING: YELLOW + __FORMAT_WARNING + RESET,
            logging.ERROR: MAGENTA + __FORMAT_ERROR + RESET,
            logging.CRITICAL: RED + __FORMAT_CRITICAL + RESET
        }

        def format(self, record):
            log_fmt = self.FORMATS.get(record.levelno)
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)