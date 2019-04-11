
from py2neo import Graph
from graph_validate.graphfeatures import graphFeatures
from graph_validate.graphtests import graphTests


graph = Graph("bolt://localhost:11005", user="neo4j", password="neo5j")
features = graphFeatures(subid='5c2dfb101603f500078b28de', graph=graph) # treutlein
graphTests(features=features)



