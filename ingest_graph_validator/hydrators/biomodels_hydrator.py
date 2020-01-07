# -*- coding: utf-8 -*-

"""BioModels API hydrator."""

# from py2neo import Node, Relationship

from .hydrator import Hydrator


class BiomodelsHydrator(Hydrator):
    """
    BioModels API hydrator class.

    Enables importing of data from BioModels API.
    """

    def __init__(self, graph, keep_constants, param):
        super().__init__(graph, keep_constants)

        self._param = param

        self._logger.debug(f"started biomodels hydrator [{self._param}]")

        self._entity_map = self.fetch(param)
        self._nodes = self.get_nodes()
        self._edges = self.get_edges()


    def fetch(self, param):
        self._logger.info("fetching biomodels data")

        return None


    def get_nodes(self):
        nodes = {}

        self._logger.info("importing nodes")

        return nodes


    def get_edges(self):
        edges = []

        self._logger.info("importing edges")

        return edges
