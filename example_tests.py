
from py2neo import Graph
from metadataGraph import graphTests, graphReports, assayPlot



graph = Graph("bolt://localhost:11005", user="neo4j", password="neo5j")

# results = graphTests(subid='5c2dfb101603f500078b28de', graph=graph).test_results

uuid_list = graphReports(subid='5c2dfb101603f500078b28de', graph=graph).uuids
cypher_to_view = assayPlot(graph=graph, uuids=uuid_list).commands
print(cypher_to_view)

