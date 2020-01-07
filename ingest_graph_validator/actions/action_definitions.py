# -*- coding: utf-8 -*-

"""Action modules for the ingest-graph-validator."""

import click
import logging

from .interactive_action import InteractiveAction
from ..config import Config


def get_actions():
    return [interactive]


@click.command()
@click.option("-w", "--web-port", type=click.INT, help="Neo4j web frontend port.",
              default=Config['NEO4J_FRONTEND_PORT'], show_default=True)
@click.pass_context
def interactive(ctx, web_port):
    """Launches the Neo4j web frontend."""

    logger = logging.getLogger(__name__)

    if ctx.obj.backend is None:
        logger.error("no backend container found")
        exit(1)

    InteractiveAction(web_port).run()
