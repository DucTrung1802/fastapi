import logging

from ..utils.enums import LogLevel


def initialize_logging():
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def log(log_level: LogLevel, message: str):
    if log_level == LogLevel.DEBUG:
        logging.debug(message)
    elif log_level == LogLevel.INFO:
        logging.info(message)
    elif log_level == LogLevel.WARNING:
        logging.warning(message)
    elif log_level == LogLevel.ERROR:
        logging.error(message)
    elif log_level == LogLevel.CRITICAL:
        logging.critical(message)
