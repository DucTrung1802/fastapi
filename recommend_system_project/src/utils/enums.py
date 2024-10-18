from enum import Enum


class TokenLocation(Enum):
    HEADER = 0
    COOKIES = 1


class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4
