# -*- coding: utf-8 -*-

"""Excel spreadsheet hydrator."""

from py2neo import Node, Relationship

from ingest.api.ingestapi import IngestApi
from ingest.importer.importer import XlsImporter

from .common import flatten
from ..config import Config
from .hydrator import Hydrator


class XlsHydrator(Hydrator):
    """
    Xls Spreadsheet hydrator class.

    Enables importing of HCA Ingest Service Xls Spreadsheets to the graph validator application.
    """

    def __init__(self, graph, xls_filename):
        super().__init__(graph)

        self._xls_filename = xls_filename

        self._logger.debug(f"started xls hydrator for file [{self._xls_filename}]")

        self._entity_map = self.import_spreadsheet(xls_filename)
        self._nodes = self.get_nodes()
        self._edges = self.get_edges()


    def import_spreadsheet(self, xls_filename):
        self._logger.info("importing spreadsheet")

        ingest_api = IngestApi(url=Config['INGEST_API'])
        importer = XlsImporter(ingest_api)

        return importer.dry_run_import_file(file_path=self._xls_filename)


    def get_nodes(self):
        nodes = {}

        self._logger.info("importing nodes")

        # We need to fetch all node types inside the entity map.
        for node_type in self._entity_map.entities_dict_by_type.keys():
            for node_id, node in self._entity_map.entities_dict_by_type.get(node_type).items():
                label = node.concrete_type or node.type
                nodes[node_id] = Node(label, **flatten(node.content), id=node.id)

                self._logger.debug(f"({node_id})")

        return nodes


    def get_edges(self):
        edges = []

        self._logger.info("importing edges")

        for node_type in self._entity_map.entities_dict_by_type.keys():
            for node_id, node in self._entity_map.entities_dict_by_type.get(node_type).items():
                for edge in node.direct_links:
                    start_node = self._nodes[node_id]
                    end_node = self._nodes[edge['id']]
                    edges.append(Relationship(start_node, edge['relationship'], end_node))

                    self._logger.debug(f"({node_id})-[{edge['relationship']}]->({end_node['id']})")

        return edges
