import json
import sys
import networkx as nx
import matplotlib.pyplot as plt
import graphviz

def load_graph(data):
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

def plot_graph(G, node_names, layout_option=2):

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
		A = G.to_undirected()
		nx.draw(A, with_labels=True, labels=node_names, node_color=node_color, node_size=800, font_size=8)
		plt.show()

	elif layout_option == 3:
		A = nx.nx_agraph.to_agraph(G)        # convert to a graphviz graph
		print(A)


def graph_stats(G):
	# total_edges = G.number_of_edges()
	max_depth= nx.dag_longest_path_length(G)
	print('Max depth is {}'.format(max_depth))


	# no_of_nodes=
	# no_biomaterials=
	# no_files=
	# no_processes=


if __name__ == '__main__':
	
	# Get bundle

	with open('9e385fa3-4af5-4847-8576-2d5fd1549da4/links.json') as f:

		data = json.load(f)
		graph = load_graph(data)
		G = graph[0]
		node_names = graph[1]
		plot_graph(G, node_names)
		graph_stats(G)



		














