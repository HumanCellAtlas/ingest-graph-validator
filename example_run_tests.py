
from py2neo import Graph
from testingAndReporting import graphTests



graph = Graph("bolt://localhost:11005", user="neo4j", password="neo5j")

'''
Graphs to test

subid = '5c8acacd53367400073122db' # Meyer 7 bundles, returns 2 unique
subid = '5c06c6ad9460a300074fc27f' # Humphreys 7 bundles, returns 1 unique
subid = '5c2dfb101603f500078b28de' # Treutlein 6 bundles, returns 1 unique

subid = '5c06cf339460a30007501909' # Peer 14 bundles, Not in demo DB
subid = '5c06a9cf9460a300074fc183' # Basu 22 bundles, quicker with 25 threads, 30 breaks ingest, Not in demo DB
subid = '5c06c34f9460a300074fc246' # Rsatija 3 bundles, Not in demo DB
'''



# results = graphTests(subid='5c2dfb101603f500078b28de', graph=graph).test_results
results = graphTests(subid='E-GEOD-81547_HCAformat_final.xlsx', graph=graph).test_results
# results = graphTests(subid='dcp_integration_test_metadata_1_SS2_bundle.xlsx', graph=graph).test_results


print(results)