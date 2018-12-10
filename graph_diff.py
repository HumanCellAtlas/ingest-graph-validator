import json
import sys
import networkx as nx
import matplotlib.pyplot as plt

def load_graph(data):
	G=nx.Graph()
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

	# nx.set_node_attributes(G, node_names, 'entity_type')

	return G, node_names

def plot_graph(G, node_names):
	color_map = ['blue', 'green', 'red']
	nx.draw(G, with_labels = True, labels = node_names, node_color = color_map)
	plt.show()

def graph_stats(G):
	print(G.number_of_edges())

if __name__ == '__main__':
	
	# Get bundle

	with open('696008bb-10d0-4e5a-a7ff-ae0c84e1602c/links.json') as f:
	# with open('48a574c8-b210-4233-86d9-43981d59fd4b/links.json') as f:
		data = json.load(f)
		graph = load_graph(data)
		plot_graph(graph[0], graph[1])



		






