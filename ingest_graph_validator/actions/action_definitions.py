# -*- coding: utf-8 -*-

"""Action modules for the ingest-graph-validator."""

import click

from .test_action import TestAction
from .ingest_validator_action import IngestValidatorAction

from ..config import Config


def get_actions():
    return [test, ingest_validator]


@click.command()
@click.option("-f", "--fail", is_flag=True, help="Immediately finish with an error status when a test fails.",
              default=False, show_default=True)
@click.pass_context
@click.argument("test_path", type=click.Path(exists=True))
def test(ctx, test_path, fail):
    """Runs graph validation tests in the specified folder."""

    TestAction(ctx.obj.graph, test_path, fail).run()


@click.command()
@click.pass_context
@click.argument("test_path", type=click.Path(exists=True))
@click.argument("connection", type=click.STRING, default=Config['AMQP_CONNECTION'])
@click.argument("exchange_name", type=click.STRING, default=Config['AMQP_EXCHANGE_NAME'])
@click.argument("queue_name", type=click.STRING, default=Config['AMQP_QUEUE_NAME'])
@click.argument("routing_key", type=click.STRING, default=Config['AMQP_ROUTING_KEY'])
def ingest_validator(ctx, test_path, connection, exchange_name, queue_name, routing_key):
    """Runs ingest graph validator tester service."""

    IngestValidatorAction(ctx.obj.graph, test_path, connection, exchange_name, queue_name, routing_key).run()
