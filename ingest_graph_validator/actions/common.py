# -*- coding: utf-8 -*-

"""Common methods used by different actions."""

import re
from os import listdir


def load_test_queries(test_path):
    """
    Loads test queries from a path.

    This function will open all files following the pattern "ends in .adoc", and extract
    queries from them using the specified regex.
    """

    test_file_name_pattern = ".adoc"
    query_regex = r"\[source,\s?cypher\]\n----(.*?)----"

    test_filenames = [x for x in listdir(test_path) if x.endswith(test_file_name_pattern)]
    test_queries = {}

    for test_filename in test_filenames:
        with open(f"{test_path}/{test_filename}") as test_file:
            test_file_contents = test_file.read()
            test_query = re.search(query_regex, test_file_contents, re.DOTALL) or None

            if test_query is not None:
                test_queries[test_filename] = test_query[1]

    return test_queries
