__author__ = "hewgreen"
__license__ = "Apache 2.0"
__date__ = "3/04/2019"

from ingest.api.ingestapi import IngestApi
import os, sys
from py2neo import Graph, Node
import json
import requests
from tqdm import tqdm
from multiprocessing.dummy import Pool
from functools import reduce
from datetime import datetime
import itertools

def node_list_2neo(graph, nodes, type, totalElements): # pass a generator, node type
	counter = 0
	tx = graph.begin()
	for node in tqdm(nodes, total=totalElements):
		counter += 1
		node_name = 'node' + str(counter)
		content = node.get('content')
		uuid = str(node.get('uuid').get('uuid'))
		node_name = Node(type, uuid=uuid)
		for key, value in content.items():
			if isinstance(value, str): #todo look for other data types and get them added to neo4j
				# print('Adding {} : {}'.format(key, value))
				node_name[key] = value
		tx.create(node_name)
	tx.commit()

def get_totals(subs_url, node_type_name): # just for progress bar

	url = subs_url + '/' + node_type_name
	response = requests.request("GET", url)
	data = json.loads(response.text)
	return data.get('page').get('totalElements')



def get_rels(process_node, main_uuid):
	relations = {'inputBiomaterials':'biomaterials',
				 'derivedBiomaterials':'biomaterials',
				 'inputFiles':'files',
				 'derivedFiles':'files'} #todo add protocols

	link_uuids = []


	for relation, entityType in relations.items():

		links = ingest_api.getRelatedEntities(relation, process_node, entityType)

		for link in links:
			uuid = link.get('uuid').get('uuid')
			if relation == 'inputBiomaterials' or relation == 'inputFiles':
				link_uuids.append({"from": main_uuid, "to": uuid})
			elif relation == 'derivedBiomaterials' or relation == 'derivedFiles':
				link_uuids.append({"from": uuid, "to": main_uuid})

	return link_uuids



def make_links(processes, totalElements):

	processes_list = list(processes)
	processes_chunked = list(split(processes_list, 2))
	thread_pool = Pool(2)
	rel_batch_lists = reduce(lambda linked_uuids_acc, linked_uuids: linked_uuids_acc + [linked_uuids],
							   thread_pool.map(lambda process_node: get_rels(process_node, process_node["uuid"]["uuid"]), processes_list),
							   [])

	rel_batch_ = list(itertools.chain.from_iterable(rel_batch_lists))
	rel_batch = str(rel_batch_).replace("'from'", "from").replace("'to'", "to").replace("'", '"')

	print(datetime.now().time())
	print('DONE- Up to making rel_batch')
	print(rel_batch)

	pre_query = "WITH REL_BATCH AS batch UNWIND batch as row MATCH (n1 {uuid : row.from}) MATCH (n2 {uuid : row.to}) MERGE(n2)-[rel: DERIVED_BY]->(n1)"
	query = pre_query.replace('REL_BATCH', rel_batch)
	graph.run(query)


def split(list_to_split, num_chunks):
	k, m = divmod(len(list_to_split), num_chunks)
	return (list_to_split[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(num_chunks))


if __name__ == '__main__':

	graph = Graph("bolt://localhost:11005", user="neo4j", password="neo5j")
	graph.delete_all()

	DEFAULT_INGEST_URL=os.environ.get('INGEST_API', 'http://api.ingest.data.humancellatlas.org')
	ingest_api = IngestApi(DEFAULT_INGEST_URL)

	# subs_url = 'https://api.ingest.data.humancellatlas.org/submissionEnvelopes/5c054a529460a300074f5007' # EMTAB5061 3514 bundles
	# subs_url = 'https://api.ingest.data.humancellatlas.org/submissionEnvelopes/5c06c6ad9460a300074fc27f' #Humphreys 7 bundles
	subs_url = 'https://api.ingest.data.humancellatlas.org/submissionEnvelopes/5bf53a6a9460a300074dc824'  # Neuron diff 1733 bundles
	# subs_url = 'https://api.ingest.data.humancellatlas.org/submissionEnvelopes/5bdc209b9460a300074b7e67'  # Pancreas6D 2544 bundles

	node_types = {}
	node_types['protocols'] = ingest_api.getEntities(subs_url, "protocols", pageSize=500)
	node_types['biomaterials'] = ingest_api.getEntities(subs_url, "biomaterials", pageSize=500)
	node_types['files'] = ingest_api.getEntities(subs_url, "files", pageSize=500)
	node_types['processes'] = ingest_api.getEntities(subs_url, "processes", pageSize=500)
	for node_type_name, nodes in node_types.items():
		totalElements = get_totals(subs_url, node_type_name) # just for progress bar
		node_list_2neo(graph, nodes, node_type_name, totalElements)


	processes = ingest_api.getEntities(subs_url, "processes", 500)
	totalElements = get_totals(subs_url, 'processes')  # just for progress bar
	make_links(processes, totalElements)


	# todo check that nodes are merging and never getting duplicated. How do I merge on uuid to double ensure this?
	# todo bump page no's up for everything to bump speed