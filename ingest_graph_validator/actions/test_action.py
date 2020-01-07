# -*- coding: utf-8 -*-

"""Runs graph validation tests in the specified folder."""

import logging


class TestAction:

    def __init__(self, test_path):
        self._test_path = test_path
        self._logger = logging.getLogger(__name__)

    def run(self):
        self._logger.info("running tests")
