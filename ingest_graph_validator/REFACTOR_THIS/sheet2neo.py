from py2neo import Graph, Node, Relationship
from tqdm import tqdm

from ingest.api.ingestapi import IngestApi
from ingest.importer.importer import XlsImporter

from .helper_functions import unpack_dictionary

from ..config import Config

DEFAULT_INGEST_URL = Config['INGEST_API']
GRAPH = Graph(Config['NEO4J_DB_URL'], user=Config['NEO4J_DB_USERNAME'], password=Config['NEO4J_DB_PASSWORD'])
CACHED_NODES = {}


class fillNeoGraph:
    def __init__(self, file_path, fresh_start=False, IngestApi=None, XlsImporter=None):
        self.file_path = file_path
        self.entity_map = self.get_entity_map()
        print('\nUploaded sheet and converted to JSON...\n')
        print(f'working with {Config["NEO4J_DB_URL"]}')

        if fresh_start:
            GRAPH.delete_all()

        self.fill_nodes()
        self.fill_relationships()

    # NOTES AS PER 10/02/2019:
    """
    submissionID was moved to beginning of function to avoid calling it many times
    content variable was removed (Not necessary now)
    specificType is defined by a entity value: 'concrete_type'

    This function gets the entity types (Biomaterial, project, etc) and fills out the node objects to return to Neo4j
    """
    def fill_nodes(self):
        nodes_by_type = self.entity_map.entities_dict_by_type
        submissionID = self.file_path  # note there are no uuids or submission IDs with dry mode so the filename is used as a pseudo ID
        for node_type in nodes_by_type:
            print('\nWorking on {} nodes...\n'.format(node_type))
            node_dict = nodes_by_type.get(node_type)
            tx = GRAPH.begin()
            for unique_node_identifier, value in tqdm(node_dict.items()):
                specificType = value.concrete_type

                # Ingest does not have consistency between importer internal names and API names!!
                name_mismatch_buffer = {'process': 'processes', 'file': 'files', 'biomaterial': 'biomaterials', 'protocol': 'protocols'}
                if node_type in name_mismatch_buffer:
                    node_type = name_mismatch_buffer.get(node_type)

                node_obj = Node(specificType if specificType else "Process", node_type, specificType=specificType, submissionID=submissionID, unique_node_identifier=unique_node_identifier)
                flat_content = unpack_dictionary(value.content, {})
                for key, value2 in flat_content.items():
                    node_obj[key] = value2
                    if "name" in key:
                        node_obj["name"] = value2
                del flat_content
                CACHED_NODES[unique_node_identifier] = node_obj
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

        for link_type, pre_rel_batch0 in rel_batch_types.items():
            unique = [dict(s) for s in set(frozenset(d.items()) for d in pre_rel_batch0)]
            for pre_rel_batch in tqdm(unique, desc=link_type):
                node1 = CACHED_NODES[pre_rel_batch["from"]]
                node2 = CACHED_NODES[pre_rel_batch["to"]]
                relationship = Relationship(node1, link_type, node2)
                GRAPH.create(relationship)
        print('\nEdge building complete.\n')

    """
    This function starts the entity maps for a spreadsheet.
    """
    def get_entity_map(self):
        print("getting entity map")
        ingest_api = IngestApi(url=DEFAULT_INGEST_URL)
        importer = XlsImporter(ingest_api)
        print("importing spreasheet")
        return importer.dry_run_import_file(file_path=self.file_path)
