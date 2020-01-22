# -*- coding: utf-8 -*-

"""Shared utility methods."""


from time import time
import logging
import requests

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


def download_file(url, destination_filename):
    """Downloads a file using a stream buffer."""
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(destination_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    return destination_filename
