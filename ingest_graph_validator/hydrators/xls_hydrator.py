# -*- coding: utf-8 -*-

"""Excel spreadsheet hydrator class."""

import logging


class XlsHydrator:

    def __init__(self, xls_filename):
        self.xls_filename = xls_filename
        self.logger = logging.getLogger(__name__)

        self.logger.debug(f"started xls hydrator with params {self.xls_filename}")


    def hydrate(self):
        return ("TEST!", {"a": 1, "b": 2})

    # TODO: AMOALLA