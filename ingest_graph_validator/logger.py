# -*- coding: utf-8 -*-

"""Logging module enabling and configuring a central log for the whole application."""

import logging
import sys
from importlib import reload


log_levels_map = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR
}


def init_logger(name, level):
    reload(logging)

    effective_level = log_levels_map[level]

    logger = logging.getLogger(name)
    logger.setLevel(effective_level)

    log_format = logging.Formatter("%(asctime)s [%(name)s] - %(levelname)s: %(message)s",
                                   "%y-%m-%d %H:%M:%S")

    log_handler = logging.StreamHandler(sys.stdout)
    log_handler.setFormatter(log_format)

    logger.addHandler(log_handler)
    log_handler.setLevel(effective_level)

    if effective_level not in list(log_levels_map.values()):
        logger.error(f"Wrong log level specified: {effective_level}")
    else:
        logger.setLevel(level)
        logger.debug(f"log started with level {level}")
