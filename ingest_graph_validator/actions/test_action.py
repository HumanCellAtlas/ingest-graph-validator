# -*- coding: utf-8 -*-

"""Runs graph validation tests in the specified folder."""

import logging

from .common import load_test_queries


class TestAction:

    def __init__(self, graph, test_path, exit_on_failure):
        self._graph = graph
        self._test_path = test_path
        self._exit_on_failure = exit_on_failure

        self._test_queries = {}
        """Test query dict. Keys are test file names, values are cypher queries"""

        self._logger = logging.getLogger(__name__)

    def run(self):
        self._logger.info("loading tests")

        self._test_queries = load_test_queries(self._test_path)
        self._logger.info(f"loaded [{len(self._test_queries)}] test queries")

        self._logger.info("running tests")
        bad_tests = 0
        total_result = {}

        for test_name, test_query in self._test_queries.items():
            self._logger.debug(f"running test [{test_name}]")
            result = self._graph.run(test_query).data()

            if len(result) != 0:
                self._logger.error(f"test [{test_name}] failed: non-empty result.")
                self._logger.error(f"result: {result}")
                total_result[test_name] = result

                if self._exit_on_failure is True:
                    self._logger.info("execution terminated")
                    exit(1)

        self._logger.info(f"all tests finished {'([{}] failed)'.format(bad_tests) if bad_tests > 0 else ''}")
        return total_result
