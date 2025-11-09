import logging
from src.utils.logging.colored_log_handler import ColoredLogHandler

# streamHandler = logging.StreamHandler()
# streamHandler.setLevel(logging.DEBUG)

# formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] %(message)s')
# formatter = ColoredFormatter(
#     # "%(log_color)s[%(asctime)s] %(message)s",
#     '[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] %(message)s',
#     datefmt=None,
#     reset=True,
#     log_colors={
#         'DEBUG':    'white,bold',
#         'INFO':     'cyan',
#         # 'INFOV':    'cyan,bold',
#         'WARNING':  'yellow',
#         'ERROR':    'red,bold',
#         'CRITICAL': 'red,bg_white',
#     },
#     secondary_log_colors={},
#     style='%'
# )
# streamHandler.setFormatter(formatter)

# grey = "\x1b[38;20m"
# yellow = "\x1b[33;20m"
# red = "\x1b[31;20m"
# bold_red = "\x1b[31;1n"
# reset = "\x1b[0m"

# logger instance 생성
# logger = logging.getLogger(__name__)
# logger.setLevel(level=logging.DEBUG)
# logger.handlers = []       # No duplicated handlers
# logger.propagate = False   # workaround for duplicated logs in ipython
# logger.addHandler(streamHandler)

logging.basicConfig(level="WARNING", handlers=[ColoredLogHandler()])
log = logging.getLogger(__name__)
