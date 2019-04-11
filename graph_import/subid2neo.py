__author__ = "hewgreen"
__license__ = "Apache 2.0"
__date__ = "3/04/2019"

# todo add links to protocols
# todo check that nodes are merging and never getting duplicated. How do I merge on uuid to double ensure this?
# todo add more metadata to the nodes. currently only strings are added.


from ingest.api.ingestapi import IngestApi
import os
from py2neo import Graph, Node
import json
import requests
from tqdm import tqdm
from multiprocessing.dummy import Pool
from functools import reduce
import itertools


GRAPH = Graph("bolt://localhost:11005", user="neo4j", password="neo5j")
DEFAULT_INGEST_URL = os.environ.get('INGEST_API', 'http://api.ingest.data.humancellatlas.org')
DEFAULT_SUBMISSION_URL = 'https://api.ingest.data.humancellatlas.org/submissionEnvelopes/'


def subid2neo(sub_id, fresh_start=False, threads=1):


    if fresh_start == True:
        GRAPH.delete_all()

    ingest_api = IngestApi(DEFAULT_INGEST_URL)

    subs_url = DEFAULT_SUBMISSION_URL + str(sub_id)

    node_types = {}
    node_types['protocols'] = ingest_api.getEntities(subs_url, "protocols", pageSize=500)
    node_types['biomaterials'] = ingest_api.getEntities(subs_url, "biomaterials", pageSize=500)
    node_types['files'] = ingest_api.getEntities(subs_url, "files", pageSize=500)
    node_types['processes'] = ingest_api.getEntities(subs_url, "processes", pageSize=500)
    for node_type_name, nodes in node_types.items():
        totalElements = get_totals(subs_url, node_type_name)  # just for progress bar
        print('Building {} nodes in Neo4J... \n'.format(node_type_name))
        node_list_2neo(GRAPH, nodes, node_type_name, totalElements, sub_id)

    processes = ingest_api.getEntities(subs_url, "processes", 500)
    totalElements = get_totals(subs_url, 'processes')  # just for progress bar
    make_links(processes, threads)


def node_list_2neo(graph, nodes, type, totalElements, sub_id): # pass a generator, node type
    counter = 0
    tx = graph.begin()
    for node in tqdm(nodes, total=totalElements):
        counter += 1
        node_name = 'node' + str(counter)
        content = node.get('content')
        uuid = str(node.get('uuid').get('uuid'))
        node_name = Node(type, uuid=uuid, submissionID=sub_id)
        for key, value in content.items():
            if key == 'describedBy':
                specific_type = value.split('/')[-1:][0]
                node_name['specificType'] = specific_type
                node_name['describeBy'] = value
            elif isinstance(value, str): #todo look for other data types and get them added to neo4j
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

    ingest_api = IngestApi(DEFAULT_INGEST_URL)

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



def make_links(processes, threads):

    print('Building edges in Neo4J...\n')

    processes_list = list(processes)
    processes_chunked = list(split(processes_list, threads))
    thread_pool = Pool(threads)
    rel_batch_lists = reduce(lambda linked_uuids_acc, linked_uuids: linked_uuids_acc + [linked_uuids],
                               thread_pool.map(lambda process_node: get_rels(process_node, process_node["uuid"]["uuid"]), processes_list),
                               [])

    rel_batch_ = list(itertools.chain.from_iterable(rel_batch_lists))
    rel_batch = str(rel_batch_).replace("'from'", "from").replace("'to'", "to").replace("'", '"')

    pre_query = "WITH REL_BATCH AS batch UNWIND batch as row MATCH (n1 {uuid : row.from}) MATCH (n2 {uuid : row.to}) MERGE(n1)-[rel: DERIVED_FROM]->(n2)"
    query = pre_query.replace('REL_BATCH', rel_batch)
    GRAPH.run(query)
    print('Edge building complete.\n')


def split(list_to_split, num_chunks):
    k, m = divmod(len(list_to_split), num_chunks)
    return (list_to_split[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(num_chunks))