# -*- coding: utf-8 -*-

"""BioModels API hydrator."""

# from py2neo import Node, Relationship

from .hydrator import Hydrator


class BiomodelsHydrator(Hydrator):
    """
    BioModels API hydrator class.

    Enables importing of data from BioModels API.
    """

    def __init__(self, graph, param):
        super().__init__(graph)

        self._param = param

        self._logger.info(f"started biomodels hydrator [{self._param}]")

        self._entity_map = self.fetch(param)
        self._nodes = self.get_nodes()
        self._edges = self.get_edges()

    def fetch(self, param):
        self._logger.debug("fetching biomodels data")

        return None

    def get_nodes(self):
        nodes = {}

        self._logger.debug("importing nodes")

        return nodes

    def get_edges(self):
        edges = []

        self._logger.debug("importing edges")

        return edges
