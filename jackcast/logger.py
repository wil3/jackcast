import logging
import os
import sys
from typing import Callable


class JackcastLogger:
    LOGGING_LEVELS = {
        "info": logging.INFO,
        "debug": logging.DEBUG,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
        "warning": logging.WARNING
    }

    def __init__(self):
        self.format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        self.level = self.get_level()
        self.loggers = {}

    def get_level(self):
        environment_level = os.environ.get("JACKCAST_LOGGING_LEVEL", None)
        if environment_level:
            level = self.LOGGING_LEVELS.get(environment_level.lower, logging.DEBUG)
        else:
            level = logging.DEBUG

        return level

    def get_logger(self, name: str, *, callback_fn: Callable = None):
        # if a logger has already been created for a specified file i.e. __name__ will simply return that logger;
        # otherwise it will create it and return that

        if not self.loggers.get(name):
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setFormatter(self.format)
            stderr_handler = logging.StreamHandler(sys.stderr)
            stderr_handler.setLevel(logging.ERROR)
            stdout_handler.setFormatter(self.format)

            logger = logging.getLogger(name)
            logger.setLevel(self.level)
            logger.addHandler(stdout_handler)
            logger.addHandler(stderr_handler)
            logger.propagate = False
            self.loggers[name] = logger

        return self.loggers[name]


jackcast_logger = JackcastLogger()
