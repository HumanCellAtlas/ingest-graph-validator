# -*- coding: utf-8 -*-

"""Runs graph validation tests in the specified folder."""

import logging
import re
from os import listdir


class TestAction:

    def __init__(self, graph, test_path, exit_on_failure):
        self._graph = graph
        self._test_path = test_path
        self._exit_on_failure = exit_on_failure

        self._test_queries = {}
        """Test query dict. Keys are test file names, values are cypher queries"""

        self._test_file_name_pattern = ".adoc"
        """Pattern for test file name"""

        self._query_regex = r"\[source,\s?cypher\]\n----(.*?)----"
        """The regex to extract queries from test files"""

        self._logger = logging.getLogger(__name__)

    def load_test_queries(self):
        test_filenames = [x for x in listdir(self._test_path) if x.endswith(self._test_file_name_pattern)]

        self._logger.info(f"found {len(test_filenames)} test files")

        for test_filename in test_filenames:
            with open(f"{self._test_path}/{test_filename}") as test_file:
                test_file_contents = test_file.read()
                test_query = re.search(self._query_regex, test_file_contents, re.DOTALL) or None

                if test_query is not None:
                    self._test_queries[test_filename] = test_query[1]

        self._logger.info(f"loaded [{len(self._test_queries)}] test queries")

    def run(self):
        self._logger.info("loading tests")

        self.load_test_queries()

        self._logger.info("running tests")

        bad_tests = 0

        for test_name, test_query in self._test_queries.items():
            self._logger.debug(f"running test [{test_name}]")
            result = self._graph.run(test_query).data()

            if len(result) != 0:
                self._logger.error(f"test [{test_name}] failed: non-empty result.")
                self._logger.error(f"result: {result}")

                if self._exit_on_failure is True:
                    self._logger.info("execution terminated")
                    exit(1)

        self._logger.info(f"all tests finished {'([{}] failed)'.format(bad_tests) if bad_tests > 0 else ''}")
