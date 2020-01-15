# -*- coding: utf-8 -*-

"""Ingest Service Submission hydrator."""

from py2neo import Node, Relationship

from ingest.api.ingestapi import IngestApi

from .common import flatten, convert_to_macrocase
from ..config import Config
from ..utils import benchmark
from .hydrator import Hydrator


# Example subid for a small submission (wong retina): 668791ed-deec-4470-b23a-9b80fd133e1c


class IngestHydrator(Hydrator):
    """
    DCP Ingest Service Submission hydrator class.

    Enables importing of HCA Ingest Service submissions by specifying a Submission ID.
    """

    def __init__(self, graph, subid):
        super().__init__(graph)

        self._subid = subid

        self._logger.info(f"started ingest hydrator for subid [{self._subid}]")

        self._ingest_api = IngestApi(Config['INGEST_API'])
        self._entities = self.fetch_submission(subid)
        self._nodes = self.get_nodes()
        self._edges = self.get_edges()

    def fetch_submission(self, subid):
        self._logger.debug("fetching ingest submission")

        entities = {}
        fetch_url = f"{Config['INGEST_API']}/submissionEnvelopes/search/findByUuidUuid?uuid={subid}"
        id_field_map = {
            'biomaterials': "biomaterial_core.biomaterial_id",
            'files': "file_core.file_name",
            'processes': "process_core.process_id",
            'projects': "project_core.project_short_name",
            'protocols': "protocol_core.protocol_id",
        }

        for entity_type in ["biomaterials", "files", "processes", "projects", "protocols"]:
            for entity in self._ingest_api.get_entities(fetch_url, entity_type):
                properties = flatten(entity['content'])

                new_entity = {
                    'properties': properties,
                    'labels': [entity['type'].lower()],
                    'node_id': properties[id_field_map[entity_type]],
                    'links': entity['_links'],
                    'uuid': entity['uuid']['uuid'],
                }

                concrete_type = new_entity['properties']['describedBy'].rsplit('/', 1)[1]
                new_entity['labels'].append(concrete_type)

                entities[entity['uuid']['uuid']] = new_entity

        return entities

    @benchmark
    def get_nodes(self):
        self._logger.debug("importing nodes")

        nodes = {}

        for entity_uuid, entity in self._entities.items():
            node_id = entity['node_id']
            nodes[entity_uuid] = Node(*entity['labels'], **entity['properties'], id=node_id)

            self._logger.debug(f"({node_id})")

        self._logger.info(f"imported {len(nodes)} nodes")

        return nodes

    @benchmark
    def get_edges(self):
        self._logger.debug("importing edges")

        edges = []
        relationship_map = {
            'projects': "projects",
            'protocols': "protocols",
            'inputToProcesses': "processes",
            'derivedByProcesses': "processes",
            'inputBiomaterials': "biomaterials",
            'derivedBiomaterials': "biomaterials",
            'supplementaryFiles': "files",
            'inputFiles': "files",
            'derivedFiles': "files",
        }

        for entity_uuid, entity in self._entities.items():
            for relationship_type in relationship_map.keys():
                if relationship_type in entity['links']:
                    relationships = self._ingest_api.get_all(
                        entity['links'][relationship_type]['href'],
                        relationship_map[relationship_type]
                    )

                    for end_entity in relationships:
                        start_node = self._nodes[entity_uuid]
                        relationship_name = convert_to_macrocase(relationship_type)
                        try:
                            end_node = self._nodes[end_entity['uuid']['uuid']]
                            edges.append(Relationship(start_node, relationship_name, end_node))
                        except KeyError:
                            self._logger.debug(f"Missing end node at a {start_node['label']} entity.")

                        self._logger.debug(f"({start_node['id']})-[:{relationship_name}]->({end_node['id']})")

        self._logger.info(f"imported {len(edges)} edges")

        return edges
