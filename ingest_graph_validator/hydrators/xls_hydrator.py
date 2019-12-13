# -*- coding: utf-8 -*-

"""Excel spreadsheet hydrator class."""

import logging

from ingest.api.ingestapi import IngestApi
from ingest.importer.importer import XlsImporter

from py2neo import Node, Relationship

from ..config import Config
from .common import flatten



class XlsHydrator:

    def __init__(self, xls_filename, graph):
        self._xls_filename = xls_filename
        self._entity_map = None
        self.graph = graph
        self._node_cache = {}

        self._logger = logging.getLogger(__name__)
        self._logger.debug(f"started xls hydrator for file [{self._xls_filename}]")


    def hydrate(self):
        self.get_entity_map()
        self.fill_nodes()
        self.fill_edges()

        self._logger.info("importing finished correctly")


    def get_entity_map(self):
        self._logger.info("importing spreadsheet")

        ingest_api = IngestApi(url=Config['INGEST_API'])
        importer = XlsImporter(ingest_api)

        self._entity_map = importer.dry_run_import_file(file_path=self._xls_filename)


    def fill_nodes(self):
        for node_type in self._entity_map.entities_dict_by_type:
            self._logger.info(f"importing {node_type} nodes")

            node_dict = self._entity_map.entities_dict_by_type.get(node_type)
            tx = self.graph.begin()

            for node_id, properties in node_dict.items():
                concrete_type = properties.concrete_type if properties.concrete_type else "Process"
                node_obj = Node(concrete_type, node_type, submissionID=self._xls_filename, uniqueNodeIdentifier=node_id)

                flat_contents = flatten(properties.content)
                for key, value in flat_contents.items():
                    node_obj[key] = value
                    print(f"\n new key: {key}: {value}")
                    if "_name" in key:
                        node_obj['name'] = value

                self._node_cache[node_id] = node_obj
                tx.create(node_obj)
            tx.commit()


    def fill_edges(self):
        self._logger.info("importing edges")

        edges = []

        for node_type, nodes in self._entity_map.entities_dict_by_type.items():
            for node_id, object in nodes.items():
                direct_links = object.direct_links
                for link in direct_links:
                    that_node_name = link.get('id')
                    that_rel_type = link.get('relationship')

                    if that_rel_type == 'projects':
                        pass
                    elif that_rel_type == 'inputToProcesses':
                        edges.append({"from": that_node_name, "to": node_id, "link": 'DERIVED_FROM'})
                    elif that_rel_type == 'derivedByProcesses':
                        edges.append({"from": node_id, "to": that_node_name, "link": 'DERIVED_FROM'})
                    elif that_rel_type == 'protocols':
                        edges.append({"from": node_id, "to": that_node_name, "link": 'IMPLEMENTS'})

        rel_batch_types = {}
        for link in edges:
            link_type = link.get('link')
            if link_type not in rel_batch_types:
                rel_batch_types[link_type] = []
            del link["link"]
            rel_batch_types.get(link_type).append(link)

        for link_type, pre_rel_batch0 in rel_batch_types.items():
            unique = [dict(s) for s in set(frozenset(d.items()) for d in pre_rel_batch0)]
            for pre_rel_batch in unique:
                node1 = self._node_cache[pre_rel_batch["from"]]
                node2 = self._node_cache[pre_rel_batch["to"]]
                relationship = Relationship(node1, link_type, node2)
                self.graph.create(relationship)
