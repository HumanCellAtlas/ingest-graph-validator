__author__ = "hewgreen"
__license__ = "Apache 2.0"
__date__ = "4/04/2019"

from os import listdir
import re
import pandas as pd

class graphTests:
    def __init__(self, subid, graph):
        self.submissionID = subid
        self.graph = graph
        self.match_pattern = '_violation.adoc'
        self.query_path = './graph_validate'
        self.cypher_query = get_tests(self)
        self.test_results = self.run_tests()

    def run_tests(self):
        test_results = {}

        for test in self.cypher_query:
            formatted_query = format_query(self, test)
            result = run_cypher(self, formatted_query)
            if result:
                test_results[test] = False
            else:
                test_results[test] = True

        return test_results


class graphReports:
    def __init__(self, subid, graph):
        self.submissionID = subid
        self.graph = graph
        self.match_pattern = '_report.adoc'
        self.query_path = './graph_report'
        self.cypher_query = get_tests(self)
        self.reports = self.get_reports()

        # Add new report functions here:
        reportname = 'assay_diff_report.adoc' # reports should deliver dict that can be put into dataframes
        self.unique_node_identifiers = self.get_unique_assays(reportname) # each report should have a corresponding function for processing


    # function finds unique assay graphs and returns the uuid of each represenative for plotting

    def get_unique_assays(self, reportname):
        report_result = self.reports.get(reportname)
        df = pd.DataFrame.from_dict(report_result).set_index('unique_node_identifier').astype(str).drop_duplicates()
        return df.index.values

    def get_reports(self):
        reports = {}
        for report in self.cypher_query:
            formatted_query = format_query(self, report)
            result = run_cypher(self, formatted_query)
            reports[report] = result
        return reports


# helper functions

def get_tests(self):
    return [x for x in listdir(self.query_path) if x.endswith(self.match_pattern)]

def format_query(self, test):
    filepath = self.query_path + '/' + test
    with open(filepath) as f:
        test_file = f.read()
        query = re.search(r'\[source,cypher\]\n----(.*?)----', test_file, re.DOTALL)[1]

        formatted_query = query.replace(
            '{submissionID}', self.submissionID
        )

        return formatted_query

def run_cypher(self, formatted_query):
    result = self.graph.run(formatted_query)
    return result.data()

def get_cypher_for_bundle_return(unique_node_identifier_list): # just returns cypher to use in neo4J at the moment :-( still working out how to present this
    commands = []
    for unique_node_identifier in unique_node_identifier_list:
        query = "MATCH x=(:files)-[:DERIVED_FROM]->(p:processes {unique_node_identifier:'{unique_node_identifier}'})-[*]->(n) WHERE n.specificType = 'donor_organism' or n.schema_type = 'protocol' RETURN x"
        formatted_query = query.replace('{unique_node_identifier}', unique_node_identifier)
        commands.append(formatted_query)
    return commands