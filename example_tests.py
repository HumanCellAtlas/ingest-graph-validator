
from py2neo import Graph
from graph_validate.graphfeatures import graphFeatures
from graph_validate.graphtests import graphTests
from graph_view.testreport import graphReport


graph = Graph("bolt://localhost:11005", user="neo4j", password="neo5j")
features = graphFeatures(subid='5c2dfb101603f500078b28de', graph=graph) # treutlein
test_results = graphTests(features=features)
# test_results_dict = graphTests(features=features).test_results
# print(test_results_dict)
graphReport(test_results, graph, subid) # make HTML report with test results.




