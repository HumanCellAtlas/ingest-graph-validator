# maybe scrap

# import graphviz
# from py2neo import Node, Graph, Relationship

# keep

import sys
import json
import os
import networkx as nx
import pandas as pd
from pandas.testing import assert_frame_equal
# import matplotlib.pyplot as plt

def load_graph_networkx(data):
	G=nx.DiGraph()
	links = data['links']
	node_names ={}
	for process in links:
		process_uuid = process['process']
		input_node_uuids = process['inputs']
		output_node_uuids = process['outputs']
		protocols = process['protocols']
		for in_node in input_node_uuids:
			node_names[in_node] = process['input_type']
			G.add_edge(in_node,process_uuid)
		for out_node in output_node_uuids:
			node_names[out_node] = process['output_type']
			G.add_edge(process_uuid, out_node)
		for protocol in protocols:
			protocol_id = protocol['protocol_id']
			node_names[protocol_id] = protocol['protocol_type']
			G.add_edge(process_uuid,protocol_id)
		node_names[process_uuid] = 'process'

	nx.set_node_attributes(G, node_names, 'entity_type')

	return G, node_names

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


	if layout_option == 1:
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

	elif layout_option == 2:
		A = G.to_undirected() # can only get edges to size correctly with an undirected graph for some reason
		nx.draw(A, with_labels=True, labels=node_names, node_color=node_color, node_size=800, font_size=8)
		# plt.show()
		if save_fig is True:
			plt.savefig(outfile_name + '.png')


	elif layout_option == 3:
		A = nx.nx_agraph.to_agraph(G)        # convert to a graphviz graph
		# print(A)

def graph_stats(G):
	total_nodes = G.number_of_nodes()
	print('Total nodes is %d' % total_nodes)
	total_edges = G.number_of_edges()
	print('Total edges is %d' % total_edges)

	biomaterialNodes = [x for x, y in G.nodes(data=True) if y['entity_type'] == "biomaterial"]
	biomaterial_out_degrees = [x[1] for x in G.out_degree(biomaterialNodes)]
	print('Biomaterial node outdegrees are: ', *biomaterial_out_degrees)
	biomaterial_in_degrees = [x[1] for x in G.in_degree(biomaterialNodes)]
	print('Biomaterial node indegrees are: ', *biomaterial_in_degrees)

	processNodes = [x for x, y in G.nodes(data=True) if y['entity_type'] == "process"]
	process_out_degrees = [x[1] for x in G.out_degree(processNodes)]
	print('Process node outdegrees are: ', *process_out_degrees)
	process_in_degrees = [x[1] for x in G.in_degree(processNodes)]
	print('Process node indegrees are: ', *process_in_degrees)

	fileNodes = [x for x, y in G.nodes(data=True) if y['entity_type'] == "file"]
	file_out_degrees = [x[1] for x in G.out_degree(fileNodes)]
	print('File node outdegrees are: ', *file_out_degrees)
	file_in_degrees = [x[1] for x in G.in_degree(fileNodes)]
	print('File node indegrees are: ', *file_in_degrees)

	max_depth= nx.dag_longest_path_length(G)
	print('Max depth is %d' % max_depth)

	print('\n')

	features = {
		'totalNodes': total_nodes,
		'totalEdges': total_edges,
		'biomaterialOutdegrees': biomaterial_out_degrees,
		'biomaterialIndegrees': biomaterial_in_degrees,
		'processOutdegrees': process_out_degrees,
		'processIndegrees': process_in_degrees,
		'fileOutdegrees': file_out_degrees,
		'fileIndegrees': file_in_degrees,
		'maxDepth': max_depth
	}

	# print(features)
	return features

if __name__ == '__main__':

	indir = 'test2/'
	metadata_file = '/links.json'
	l = os.listdir(indir)
	infiles = [indir + x + metadata_file for x in l]
	print('Processing {} bundles'.format(len(infiles)))

	feature_list = []

	for infile in infiles:
		with open(infile) as f:
			data = json.load(f)
			graph = load_graph_networkx(data)
			G = graph[0]
			node_names = graph[1]
			# # plot_graph(G, node_names, infile, save_fig=False)
			G_features = graph_stats(G)
			feature_list.append(G_features)

			# load_graph_neo4j(data)

	feature_frame = pd.DataFrame(feature_list)
	# assert_frame_equal(feature_frame[0], feature_frame[3], check_dtype=False)
	# assert_frame_equal(feature_frame[0], feature_frame[2], check_dtype=False)
	print(feature_frame)
