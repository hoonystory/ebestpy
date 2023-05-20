import logging

# logger instance 생성
logger = logging.getLogger(__name__)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] %(message)s')

streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)

logger.addHandler(streamHandler)

#  DEBUG, INFO, WARNING, ERROR, CRITICAL
logger.setLevel(level=logging.DEBUG)
