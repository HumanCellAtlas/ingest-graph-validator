
from ingest.api.ingestapi import IngestApi
from ingest.importer.importer import XlsImporter
from graph_import.helperFunctions import unpack_ignore_lists
from py2neo import Graph, Node
from tqdm import tqdm

import os

DEFAULT_INGEST_URL = os.environ.get('INGEST_API', 'https://api.ingest.data.humancellatlas.org')
GRAPH = Graph("bolt://localhost:11005", user="neo4j", password="neo5j")

# pip install -e git+https://github.com/HumanCellAtlas/ingest-client.git@4cb76e90a596cd53aeed13b1c06d65f7f52340df#egg=hca_ingest # temp needed until latest ingest release


class fillNeoGraph:
    def __init__(self, file_path, fresh_start=False):
        self.file_path = file_path
        self.entity_map = self.get_entity_map()
        print('\nUploaded sheet and converted to JSON...\n')

        if fresh_start == True:
            GRAPH.delete_all()

        self.fill_nodes()
        self.fill_relationships()


    def fill_nodes(self):
        nodes_by_type = self.entity_map.entities_dict_by_type
        for node_type in nodes_by_type:
            print('\nWorking on {} nodes...\n'.format(node_type))
            node_dict = nodes_by_type.get(node_type)
            tx = GRAPH.begin()
            for unique_node_identifier, value in tqdm(node_dict.items()):
                content = value.content
                submissionID = self.file_path # note there are no uuids or submission IDs with dry mode so the filename is used as a pseudo ID
                specificType = content.get('describedBy').split('/')[-1:][0]

                # Ingest does not have consistency between importer internal names and API names!!
                name_mismatch_buffer = {'process':'processes','file':'files','biomaterial':'biomaterials','protocol':'protocols'}
                if node_type in name_mismatch_buffer:
                    node_type = name_mismatch_buffer.get(node_type)


                node_obj = Node(node_type, specificType=specificType, submissionID=submissionID, unique_node_identifier=unique_node_identifier)
                flat_content = unpack_ignore_lists(content)
                for key, value in flat_content.items():
                    node_obj[key] = value
                tx.create(node_obj)
            tx.commit()

    def fill_relationships(self):
        print('\nAssimilating edges...\n')
        links_to_create = []
        nodes_by_type = self.entity_map.entities_dict_by_type
        for node_type, nodes in nodes_by_type.items():
            print('\nWorking on {} nodes...\n'.format(node_type))

            for unique_node_identifier, object in tqdm(nodes.items()):
                direct_links = object.direct_links
                for link in direct_links:
                    that_node_name = link.get('id')
                    that_rel_type = link.get('relationship')

                    if that_rel_type == 'projects':
                        pass
                    elif that_rel_type == 'inputToProcesses':
                        links_to_create.append({"from": that_node_name, "to": unique_node_identifier, "link": 'DERIVED_FROM'})
                    elif that_rel_type == 'derivedByProcesses':
                        links_to_create.append({"from": unique_node_identifier, "to": that_node_name, "link": 'DERIVED_FROM'})
                    elif that_rel_type == 'protocols':
                        links_to_create.append({"from": unique_node_identifier, "to": that_node_name, "link": 'IMPLEMENTS'})

        # until dynamic label parameterization is available in cypher 10 only 1 link type can be created at once hence the need for this splitting.
        rel_batch_types = {}
        for link in links_to_create:
            link_type = link.get('link')
            if link_type not in rel_batch_types:
                rel_batch_types[link_type] = []
            del link["link"]
            rel_batch_types.get(link_type).append(link)

        print('\nPushing Edges to Neo4J...\n')

        for link_type, pre_rel_batch in rel_batch_types.items():
            rel_batch = str(pre_rel_batch).replace("'from'", "from").replace("'to'", "to").replace("'link'","link").replace("'",'"')
            pre_query = "WITH REL_BATCH AS batch UNWIND batch as row MATCH (n1 {unique_node_identifier : row.from}) MATCH (n2 {unique_node_identifier : row.to}) MERGE(n1)-[rel: LINK_TYPE]->(n2)"
            query = pre_query.replace('REL_BATCH', rel_batch).replace('LINK_TYPE', link_type)
            GRAPH.run(query)
        print('\nEdge building complete.\n')

    def get_entity_map(self):
        ingest_api = IngestApi(url=DEFAULT_INGEST_URL)
        importer = XlsImporter(ingest_api)
        return importer.dry_run_import_file(file_path=self.file_path)