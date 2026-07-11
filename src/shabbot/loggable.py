import logging
from functools import cached_property


class Loggable:
    @cached_property
    def logger(self) -> logging.Logger:
        return logging.getLogger(f"{type(self).__module__}.{type(self).__name__}")
