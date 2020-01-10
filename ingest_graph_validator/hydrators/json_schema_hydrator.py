# -*- coding: utf-8 -*-

"""JSON Schema hydrator."""

import json
from pathlib import Path

from py2neo import Node, Relationship

from .hydrator import Hydrator


class JsonSchemaHydrator(Hydrator):
    """
    JSON Schema hydrator class.

    Enables importing of a JSON Schema to the graph validator application.
    """

    def __init__(self, graph, schema_path):
        super().__init__(graph)

        self._schema_path = schema_path

        self._logger.debug(f"started json schema hydrator for path [{self._schema_path}]")

        self._schema_elements = self.import_schema(schema_path)
        self._nodes = self.get_nodes()
        self._edges = self.get_edges()


    def _extract_labels_from_path(self, path):
        def path_strip(path):
            return str(path).strip('.').rstrip('/').lstrip('/').split('/')

        excluded_labels = path_strip(self._schema_path)
        labels = [x for x in path_strip(path) if x not in excluded_labels]

        return labels


    def import_schema(self, schema_path):
        self._logger.info("importing json schema")

        schema_file_paths = Path(schema_path).rglob("*.json")
        schema_elements = {}

        for schema_file_path in schema_file_paths:
            with open(schema_file_path) as schema_file:
                schema_element_data = json.load(schema_file)
                labels = self._extract_labels_from_path(schema_file_path.parents[0])

                schema_element = {
                    'labels': labels,
                    'properties': {
                        'entity_name': schema_file_path.stem,
                    },
                    'edges': [],
                }

                for key, value in schema_element_data['properties'].items():
                    if "$ref" in value.keys():
                        ref = value['$ref'].split('/')[-1].split('.')[0]
                        schema_element['edges'].append(ref)
                    else:
                        schema_element['properties'][key] = value['type']

                schema_elements[schema_element_data['name']] = schema_element

        return schema_elements


    def get_nodes(self):
        nodes = {}

        self._logger.info("importing nodes")

        for node_id, node in self._schema_elements.items():
            nodes[node_id] = Node(*node['labels'], **node['properties'], id=node_id)

        return nodes


    def get_edges(self):
        edges = []

        self._logger.info("importing edges")

        for node_id, node in self._schema_elements.items():
            for edge in node['edges']:
                start_node = self._nodes[node_id]
                end_node = self._nodes[edge]
                edges.append(Relationship(start_node, "INCLUDES", end_node))

        return edges
