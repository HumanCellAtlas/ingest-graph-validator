# -*- coding: utf-8 -*-

import logging


class Hydrator:
    """
    Hydrator main class, any hydrators implemented for the graph validator must implement this interface.
    """

    def __init__(self, graph):
        self._logger = logging.getLogger(__name__)
        self._graph = graph

        self._nodes = {}
        """Node dictionary. Keys are node ids, and values are py4neo Node objects."""

        self._edges = []
        """Edge list of py4neo Relationship objects."""


    def hydrate(self):
        """
        This method is called to populate the database. It will use the data contained
        in the _nodes and _edges attributes.
        """

        self.fill_nodes(self._graph, self._nodes)
        self.fill_edges(self._graph, self._edges)


    def fill_nodes(self, graph, nodes):
        tx = self._graph.begin()

        for node in list(nodes.values()):
            tx.create(node)

        tx.commit()


    def fill_edges(self, graph, edges):
        tx = self._graph.begin()

        for edge in edges:
            tx.create(edge)

        tx.commit()
