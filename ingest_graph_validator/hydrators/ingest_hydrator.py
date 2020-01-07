# -*- coding: utf-8 -*-

"""Ingest Service Submission hydrator."""

# from py2neo import Node, Relationship

from .hydrator import Hydrator


class IngestHydrator(Hydrator):
    """
    DCP Ingest Service Submission hydrator class.

    Enables importing of HCA Ingest Service submissions by specifying a Submission ID.
    """

    def __init__(self, graph, keep_constants, subid):
        super().__init__(graph, keep_constants)

        self._subid = subid

        self._logger.debug(f"started ingest hydrator [{self._subid}]")

        self._entity_map = self.fetch_submission(subid)
        self._nodes = self.get_nodes()
        self._edges = self.get_edges()


    def fetch_submission(self, subid):
        self._logger.info("fetching ingest submission")

        return None


    def get_nodes(self):
        nodes = {}

        self._logger.info("importing nodes")

        return nodes


    def get_edges(self):
        edges = []

        self._logger.info("importing edges")

        return edges