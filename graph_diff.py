# maybe scrap

# import graphviz
# from py2neo import Node, Graph, Relationship

# keep

import sys
import json
import os
import networkx as nx
import pandas as pd
from networkx import Graph
from networkx.algorithms.coloring.greedy_coloring_with_interchange import Node
from pandas.testing import assert_frame_equal
from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt
from py2neo import Relationship

def load_graph_networkx_old(data):
	G=nx.DiGraph()
	links = data#['links']
	node_names = {}
	node_types = {}
	for process in links:
		process_uuid = process['process']
		input_node_uuids = process['inputs']
		output_node_uuids = process['outputs']
		protocols = process['protocols']
		for in_node in input_node_uuids:
			node_names[in_node] = process['input_specific_type']
			node_types[in_node] = process['input_type']
			G.add_edge(in_node,process_uuid)
		for out_node in output_node_uuids:
			node_names[out_node] = process['output_specific_type']
			node_types[out_node] = process['output_type']
			G.add_edge(process_uuid, out_node)
		for protocol in protocols:
			protocol_id = protocol['protocol_id']
			node_names[protocol_id] = protocol['protocol_type']
			node_types[protocol_id] = protocol['protocol_type']
			G.add_edge(process_uuid,protocol_id)
		node_names[process_uuid] = 'process'
		node_types[process_uuid] = 'process'

	nx.set_node_attributes(G, node_types, 'entity_type')
	nx.set_node_attributes(G, node_names, 'entity_name')

	# print(G.nodes(data=True))
	# print(node_names)

	return G, node_names

def load_graph_networkx(data):
	G=nx.DiGraph()
	links = data#['links']
	node_names = {}
	node_types = []
	nonspecific_node_types = {}
	specific_node_types = {}

	def counter(type_name, uuid):
		# print(type_name)
		# print(uuid)
		if uuid in node_names:
			new_name = type_name + '_' + str(node_types.count(type_name))
			return new_name
		else:
			node_types.append(type_name)
			new_name = type_name + '_' + str(node_types.count(type_name))
			node_names[uuid] = new_name
			nonspecific_node_types[uuid] = type_name
			return new_name

	for process in links:
		process_uuid = process['process']
		input_node_uuids = process['inputs']
		output_node_uuids = process['outputs']
		protocols = process['protocols']
		for in_node in input_node_uuids:
			# node_names[in_node] = counter(process['input_type'], in_node)
			counter(process['input_type'], in_node)
			specific_node_types[in_node] = process['input_specific_type']
			G.add_edge(in_node,process_uuid)
		for out_node in output_node_uuids:
			# node_names[out_node] = counter(process['output_type'], out_node)
			counter(process['output_type'], out_node)
			specific_node_types[out_node] = process['output_specific_type']
			G.add_edge(process_uuid, out_node)
		for protocol in protocols:
			protocol_id = protocol['protocol_id']
			specific_node_types[protocol_id] = protocol['protocol_type']
			# node_names[protocol_id] = counter(protocol['protocol_type'], protocol_id)
			counter(protocol['protocol_type'], protocol_id)
			G.add_edge(process_uuid,protocol_id)
		# node_names[process_uuid] = counter('process', process_uuid)
		counter('process', process_uuid)
		specific_node_types[process_uuid] = 'process'

	nx.set_node_attributes(G, node_names, 'unique_name')
	nx.set_node_attributes(G, specific_node_types, 'entity_name') # needs adding in again

	nx.set_node_attributes(G, nonspecific_node_types, 'entity_type')

	nx.relabel_nodes(G, node_names, copy=False)
	uuid_switch = {y:x for x,y in node_names.items()}
	nx.set_node_attributes(G, uuid_switch, 'uuid')

	# print(G.nodes(data=True))
	# print(specific_node_types)

	return G, specific_node_types

def load_graph_neo4j(data): # not working on hold
	graph = Graph('http://localhost:7474/db/data/', user='neo4j', password='neo5j')  # initialising graph
	links = data['links']

	# def make_node(node_type, uuid):
	# 	graph.merge(Node(node_type, name=str(uuid)), node_type, 'name')
	# 	return Node(node_type, name=str(uuid))

	def make_relationship(graph, in_node_type, in_uuid, out_node_type, out_uuid):
		tx = graph.begin()
		in_node = Node(in_node_type, name=str(in_uuid))
		tx.create(in_node)
		out_node = Node(out_node_type, name=str(out_uuid))
		ab = Relationship(in_node, "LINK", out_node)
		# tx.create(ab)
		tx.merge(ab)

	for process in links:
		process_uuid = process['process']
		input_node_uuids = process['inputs']
		output_node_uuids = process['outputs']
		protocols = process['protocols']
		# rel_type = 'LINK'

		# neo4j_relationships = []
		# neo4j_nodes = []


		# neo4j_process_node = make_node('process', process_uuid)
		# neo4j_nodes.append(neo4j_process_node)

		# convert links.json in to neo relationships

		for in_node in input_node_uuids:

			make_relationship(graph, process['input_type'], in_node, 'process', process_uuid)


			# neo4j_in_node = make_node(process['input_type'], in_node)
			# neo4j_relationships.append(Relationship(neo4j_in_node, rel_type, neo4j_process_node))
			# neo4j_nodes.append(neo4j_in_node) # temp for test remove

		for out_node in output_node_uuids:

			make_relationship(graph, 'process', process_uuid, process['output_type'], out_node)


			# neo4j_out_node = make_node(process['output_type'], out_node)
			# neo4j_relationships.append(Relationship(neo4j_process_node, rel_type, neo4j_out_node))
			# neo4j_nodes.append(neo4j_out_node) # temp for test remove

		for protocol in protocols:

			make_relationship(graph, 'process', process_uuid, protocol['protocol_id'], protocol)


			# neo4j_protocol_node = make_node(protocol['protocol_id'], protocol)
			# neo4j_relationships.append(Relationship(neo4j_process_node, rel_type, neo4j_protocol_node))
			# neo4j_nodes.append(neo4j_protocol_node) # temp for test remove

		# merge relationships into main graph

		# for neo4j_node in neo4j_nodes: # temp for test remove
		# 	graph.merge(neo4j_node) # temp for test remove

		# for neo_relationship in neo4j_relationships:
		# 	graph.merge(neo_relationship, "name") # merge is important to prevent duplicates

def plot_graph(G, node_names, outfile_name, layout_option=2, save_fig=False):

	node_color = []
	for node in G.nodes(data=True):

		if 'biomaterial' in node[1]['entity_type']:
			node_color.append('darkorange')
		elif 'file' in node[1]['entity_type']:
			node_color.append('lightskyblue')
		elif 'process' in node[1]['entity_type']:
			node_color.append('mistyrose')
		else:
			node_color.append('olive')


	if layout_option == '1':
		# pos = nx.spectral_layout(G)
		pos = nx.spring_layout(G)
		nodes = nx.draw_networkx_nodes(G, pos, node_size=100,
			node_color=node_color,
			font_size=8,
			labels=node_names,
			with_labels=True)
		edges = nx.draw_networkx_edges(G, pos,
			arrowstyle='->',
			arrowsize=10,
			width=2)

	elif layout_option == '2':
		A = G.to_undirected() # can only get edges to size correctly with an undirected graph for some reason
		nx.draw(A, with_labels=True, node_color=node_color, node_size=800, font_size=8)
		plt.show()
		# if save_fig is True:
		# 	plt.savefig(outfile_name + '.png')


	elif layout_option == '3':
		A = nx.nx_agraph.to_agraph(G)        # convert to a graphviz graph
		# print(A)

def graph_stats(G):
	total_nodes = G.number_of_nodes()
	# print('Total nodes is %d' % total_nodes)
	total_edges = G.number_of_edges()
	# print('Total edges is %d' % total_edges)

	biomaterialNodes = [x for x, y in G.nodes(data=True) if y['entity_type'] == "biomaterial"]
	biomaterialNodes.sort()
	biomaterial_out_degrees = [x[1] for x in G.out_degree(biomaterialNodes)]
	# print('Biomaterial node outdegrees are: ', *biomaterial_out_degrees)
	biomaterial_in_degrees = [x[1] for x in G.in_degree(biomaterialNodes)]
	# print('Biomaterial node indegrees are: ', *biomaterial_in_degrees)

	processNodes = [x for x, y in G.nodes(data=True) if y['entity_type'] == "process"]
	processNodes.sort()
	process_out_degrees = [x[1] for x in G.out_degree(processNodes)]
	# print('Process node outdegrees are: ', *process_out_degrees)
	process_in_degrees = [x[1] for x in G.in_degree(processNodes)]
	# print('Process node indegrees are: ', *process_in_degrees)

	fileNodes = [x for x, y in G.nodes(data=True) if y['entity_type'] == "file"]
	fileNodes.sort()
	file_out_degrees = [x[1] for x in G.out_degree(fileNodes)]
	# print('File node outdegrees are: ', *file_out_degrees)
	file_in_degrees = [x[1] for x in G.in_degree(fileNodes)]
	# print('File node indegrees are: ', *file_in_degrees)

	max_depth= nx.dag_longest_path_length(G)
	# print('Max depth is %d' % max_depth)
	# print('\n')

	features = {
		'totalNodes': total_nodes,
		'totalEdges': total_edges,
		'maxDepth': max_depth,
		'nodeList': ",".join(str(x) for x in sorted(list(set(G)))),
		'biomaterialOutdegrees': ",".join(str(x) for x in biomaterial_out_degrees),
		'biomaterialIndegrees': ",".join(str(x) for x in biomaterial_in_degrees),
		'processOutdegrees': ",".join(str(x) for x in process_out_degrees),
		'processIndegrees': ",".join(str(x) for x in process_in_degrees),
		'fileOutdegrees': ",".join(str(x) for x in file_out_degrees),
		'fileIndegrees': ",".join(str(x) for x in file_in_degrees)
	}

	return features

def graph_assumptions(G):
	# Every graph starts from donor biomaterial node: donor_in_degree = 0, donor_out_degrees >= 1.
	donorNodes = [x for x, y in G.nodes(data=True) if y['entity_name'] == "donor_organism"]
	donorNodes.sort()
	donor_in_degrees = [x[1] for x in G.in_degree(donorNodes)]
	donor_out_degrees = [x[1] for x in G.out_degree(donorNodes)]
	# print('Donor node indegrees are: ', *donor_in_degrees)
	# print('Donor node outdegrees are: ', *donor_out_degrees)

	if all(x == 0 for x in donor_in_degrees) and all(x >= 1 for x in donor_out_degrees) and len(donorNodes) >= 1:
		donorFirstNode = True
	else:
		donorFirstNode = False

	# print('Graph starts with donor node: %s' % donorFirstNode)

	# Every graph should end with file node(s). sequence_file_in_degrees = 1, sequence_file_out_degree = 0.
	sequenceFileNodes = [x for x, y in G.nodes(data=True) if y['entity_name'] == "sequence_file"]
	sequenceFileNodes.sort()
	sequence_file_in_degrees = [x[1] for x in G.in_degree(sequenceFileNodes)]
	sequence_file_out_degrees = [x[1] for x in G.out_degree(sequenceFileNodes)]
	# print('Sequence file node indegrees are: ', *sequence_file_in_degrees)
	# print('Sequence file node outdegrees are: ', *sequence_file_out_degrees)

	if all(x == 1 for x in sequence_file_in_degrees) and all(x == 0 for x in sequence_file_out_degrees) and len(sequenceFileNodes) >= 1:
		sequenceFileLastNode = True
	else:
		sequenceFileLastNode = False

	# print('Graph ends with sequence file node(s): %s' % sequenceFileLastNode)

	# There can only be 1, 2, or 3 sequencing file nodes in the graph.

	if len(sequenceFileNodes) in [1,2,3]:
		sequenceFileNodeCount = True
	else:
		sequenceFileNodeCount = False

	# print('Graph has 1, 2, or 3 sequence file node(s): %s' % sequenceFileNodeCount)

	# Graph should have no hanging biomaterial nodes.
	biomaterialNodes = [x for x, y in G.nodes(data=True) if y['entity_type'] == "biomaterial"]
	biomaterialNodes.sort()
	biomaterial_out_degrees = [x[1] for x in G.out_degree(biomaterialNodes)]
	# print('Biomaterial node outdegrees are: ', *biomaterial_out_degrees)

	if all(x >= 1 for x in biomaterial_out_degrees):
		noHangingBiomaterialNode = True
	else:
		noHangingBiomaterialNode = False

	# print('Graph has no hanging biomaterial nodes: %s\n' % noHangingBiomaterialNode)

	# The ultimate process node should have 2 protocols (library preparation and sequencing or imaging preparation and imaging).
	assayProtocolEdge = [x for x in G.edges() if 'process_1' in x[0] and 'protocol' in x[1]]
	# print(assayProtocolEdge)

	if len(assayProtocolEdge) == 2:
		assayHasTwoProtocols = True
	else:
		assayHasTwoProtocols = False

	# Cell suspension or imaged specimen is the last biomaterial node.
	lastBiomaterialNode = [y for x, y in G.nodes(data=True) if y['unique_name'] == "biomaterial_1"]
	for x in lastBiomaterialNode:
		if x['entity_name'] == 'cell_suspension' or x['entity_name'] == 'imaged_specimen':
			cellSuspensionLastBiomaterial = True
		else:
			cellSuspensionLastBiomaterial = False

	# The minimal longest path length of the graph should be 5 (sequencing or imaging).
	max_depth= nx.dag_longest_path_length(G)
	# print(max_depth)
	if max_depth >= 5:
		minLongestPathIsFive = True
	else:
		minLongestPathIsFive = False

	# Not checked:
	# Graph has a direction from biomaterial node to file node and cannot have cycle (is directional acyclical).
	# Graph can have more than one first biomaterial (biomaterial with indegree 0).

	assumptions = {
		'donorFirstNode': donorFirstNode,
		'sequenceFileLastNode': sequenceFileLastNode,
		'sequenceFileNodeCount': sequenceFileNodeCount,
		'noHangingBiomaterialNode': noHangingBiomaterialNode,
		'assayHasTwoProtocols': assayHasTwoProtocols,
		'minLongestPathIsFive': minLongestPathIsFive,
		'cellSuspensionLastBiomaterial': cellSuspensionLastBiomaterial
	}

	return assumptions

def generate_report(FL, AL):

	print('--------------------\nREPORT\n--------------------')

	feature_frame = pd.DataFrame(FL)
	print("Number of feature sets (graphs): %d" % len(feature_frame))

	# Find unique rows
	feature_frame_unique = feature_frame.drop_duplicates()
	print("Number of unique feature sets (graphs): %d" % len(feature_frame_unique))

	print("\n\nUnique feature sets:")
	with pd.option_context('display.max_rows', None, 'display.max_columns', feature_frame_unique.shape[1]):
		print(feature_frame_unique)

	assumption_frame = pd.DataFrame(AL)
	print("--------------------\nNumber of assumption sets (graphs): %d" % len(assumption_frame))

	# Find unique rows
	assumption_frame_unique = assumption_frame.drop_duplicates()
	print("Number of unique assumption sets (graphs): %d" % len(assumption_frame_unique))

	print("\n\nUnique assumption sets:")
	with pd.option_context('display.max_rows', None, 'display.max_columns', assumption_frame_unique.shape[1]):
		print(assumption_frame_unique)

def graph_compare(graphs):
	# graph_sets = [sorted(list(set(x))) for x in graphs]
	# unique_data = [list(x) for x in set(tuple(x) for x in graph_sets)]
	# print('There are {} unique node sets out of {} graphs'.format(len(unique_data), len(graphs)))

	unique_by_node_groups = {} # str(sorted_node_list) : [G,G]

	for graph in graphs:
		sorted_node_list = sorted(list(set(graph)))
		if str(sorted_node_list) in unique_by_node_groups:
			unique_by_node_groups[str(sorted_node_list)].append(graph)
		else:
			unique_by_node_groups[str(sorted_node_list)] = [graph]

	print('There are {} unique node sets out of {} graphs'.format(len(unique_by_node_groups), len(graphs)))
	
	for group, graph_list in unique_by_node_groups.items():
		group_representative_graph = graph_list[0]
		# for grouped_graph in graph_list[1:]:

			# all too slow for now. We need to find an optimised graph comparison tool.

			# comparison = nx.difference(group_representative_graph, grouped_graph)
			# print(nx.graph_edit_distance(group_representative_graph, grouped_graph))
			# agenerator = nx.optimize_graph_edit_distance(group_representative_graph, grouped_graph) # not sure why I see a difference here
			# agenerator = nx.optimize_edit_paths(group_representative_graph, grouped_graph) # weird tuple output and slow


if __name__ == '__main__':

	parser = ArgumentParser()
	parser.add_argument("-d", "--directory", dest="inputDirectory",
						help="Path to the input files")
	parser.add_argument("-p", "--plot", action="store_true",
						help="Flag to draw the graphs")
	parser.add_argument("-l", "--layout", dest="layout",
						help="Graph layout option", default="2")

	arguments = parser.parse_args()

	indir = arguments.inputDirectory
	# metadata_file = '/links.json'
	l = os.listdir(indir)
	# infiles = [indir + x + metadata_file for x in l]
	infiles = [indir + x for x in l]
	print('Processing {} bundles...'.format(len(infiles)))

	feature_list = []
	assumption_list = []
	graphs = []

	for infile in infiles:
		with open(infile) as f:
			data = json.load(f)
			graph = load_graph_networkx(data)
			G = graph[0]
			node_names = graph[1]
			if arguments.plot:
				plot_graph(G, node_names, infile, arguments.layout, save_fig=False)

			# Calculate graph features
			G_features = graph_stats(G)
			feature_list.append(G_features)

			# Assess graph assumptions
			G_assumptions = graph_assumptions(G)
			assumption_list.append(G_assumptions)

		graphs.append(G)

	# load_graph_neo4j(data)
	generate_report(feature_list, assumption_list)
	graph_compare(graphs)
