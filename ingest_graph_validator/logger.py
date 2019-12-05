# -*- coding: utf-8 -*-

"""
Logging module enabling and configuring a central log for the whole application.
"""

import logging
import sys
from importlib import reload


log_levels_map = {
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR
}


def init_logger(name, level):
    # Fix libraries using root logger.
    reload(logging)

    effective_level = log_levels_map[level]

    logger = logging.getLogger(name)
    logger.setLevel(effective_level)

    log_format = logging.Formatter("{asctime} [{name}] - {levelname}: {message}",
                                   "%y-%m-%d %H:%M:%S",
                                   "{")

    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(log_format)

    logger.addHandler(log_handler)
    log_handler.setLevel(effective_level)

    if effective_level not in [logging.INFO, logging.WARNING, logging.ERROR]:
        logger.error(f"Wrong log level specified: {effective_level}")
    else:
        logger.setLevel(level)
