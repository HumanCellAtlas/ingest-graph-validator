__author__ = "hewgreen"
__license__ = "Apache 2.0"
__date__ = "4/04/2019"

from os import listdir
import re
import pandas as pd


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


class graphTests:
    def __init__(self, subid, graph):
        self.submissionID = subid
        self.graph = graph
        self.match_pattern = '_violation.adoc'
        self.query_path = './graph_validate'
        self.cypher_query = get_tests(self)
        self.test_results = self.run_tests()

        print(self.test_results)


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

        reportname = 'assay_diff_report.adoc'
        self.uuids = self.get_unique_assays(reportname)


    def get_reports(self):
        reports = {}
        for report in self.cypher_query:
            formatted_query = format_query(self, report)
            result = run_cypher(self, formatted_query)
            reports[report] = result
        return reports

    def get_unique_assays(self, reportname): # function finds unique assay graphs and returns the uuid of each represenative for plotting
        df = pd.DataFrame.from_dict(self.reports.get(reportname)).set_index('process_uuid').astype(str).drop_duplicates()
        return df.index.values

class assayPlot: # just returns cypher to use in neo4J at the moment :-( still working out how to present this
    def __init__(self, graph, uuids):
        self.graph = graph
        self.uuids = uuids
        self.commands = self.get_cypher()



    def get_cypher(self):
        commands = []
        for uuid in self.uuids:
            query = "MATCH x=(:files)-[:DERIVED_FROM]->(p:processes {uuid:'{assay_uuid}'})-[*]->(n) WHERE n.specificType = 'donor_organism' or n.schema_type = 'protocol' RETURN x"

            formatted_query = query.replace('{assay_uuid}', uuid)
            # formatted_query = re.sub('\s+', ' ', query.replace('{assay_uuid}', uuid))
            commands.append(formatted_query)
        return commands













