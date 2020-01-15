# -*- coding: utf-8 -*-

"""Shared utility methods."""


from time import time
import logging

from functools import wraps


def benchmark(function):
    @wraps(function)
    def _time_it(*args, **kwargs):
        logger = logging.getLogger(__name__)
        start = int(round(time() * 1000))

        try:
            return function(*args, **kwargs)
        finally:
            end_ = int(round(time() * 1000)) - start
            logger.info(f"{function.__name__} took {end_} ms")

    return _time_it
