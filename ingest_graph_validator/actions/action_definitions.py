# -*- coding: utf-8 -*-

"""Action modules for the ingest-graph-validator."""

import click

from .interactive_action import InteractiveAction
from .test_action import TestAction
from ..config import Config


def get_actions():
    return [interactive, test]


@click.command()
@click.option("-w", "--web-port", type=click.INT, help="Neo4j web frontend port.",
              default=Config['NEO4J_FRONTEND_PORT'], show_default=True)
@click.pass_context
def interactive(ctx, web_port):
    """Launches the Neo4j web frontend."""

    InteractiveAction(web_port).run()


@click.command()
@click.pass_context
@click.argument("test_path", type=click.Path(exists=True))
def test(ctx, test_path):
    """Runs graph validation tests in the specified folder."""

    TestAction(test_path).run()
