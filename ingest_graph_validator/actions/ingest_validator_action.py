# -*- coding: utf-8 -*-

"""Runs graph validation tests in the specified folder."""

import logging

from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin

from ..hydrators.ingest_hydrator import IngestHydrator
from .test_action import TestAction

from .common import load_test_queries

from ..config import Config


class ValidationHandler():

    def __init__(self, subid, graph, test_path):
        self._subid = subid
        self._graph = graph
        self._test_path = test_path

    def run(self):
        IngestHydrator(self._graph, self._subid).hydrate()
        return TestAction(self._graph, self._test_path, False).run()



class ValidationListener(ConsumerMixin):

    def __init__(self, connection, validation_queue, graph, test_path):
        self.connection = connection
        self.validation_queue = validation_queue
        self._graph = graph
        self._test_path = test_path

        self._logger = logging.getLogger(__name__)

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.validation_queue, accept=["json"], on_message=self.handle_message, prefetch_count=10)]

    def handle_message(self, message):
        subid = message.payload['submissionEnvelopeUuid']
        self._logger.info(f"received validation request for {subid}")

        validation_result = ValidationHandler(subid, self._graph, self._test_path).run()

        if validation_result is not None:
            self._logger.info(f"validation finished for {subid}")
            self._logger.debug(f"result: {validation_result}")

            message.ack()


class IngestValidatorAction:

    def __init__(self, graph, test_path, connection, exchange_name, queue_name, routing_key):
        self._graph = graph
        self._test_path = test_path
        self._connection = connection
        self._exchange_name = exchange_name
        self._queue_name = queue_name
        self._routing_key = routing_key

        self._test_queries = {}
        """Test query dict. Keys are test file names, values are cypher queries"""

        self._logger = logging.getLogger(__name__)

    def run(self):
        self._logger.info("loading tests")

        self._test_queries = load_test_queries(self._test_path)
        self._logger.info(f"loaded [{len(self._test_queries)}] test queries")

        validation_exchange = Exchange(self._exchange_name, type='direct')
        validation_queue = Queue(self._queue_name, validation_exchange, routing_key=self._routing_key)

        with Connection(Config['AMQP_CONNECTION']) as conn:
            self._logger.info(f"listening for messages at {conn}")
            try:
                ValidationListener(conn, validation_queue, self._graph, self._test_path).run()
            except KeyboardInterrupt:
                self._logger.info("AMQP listener stopped")
