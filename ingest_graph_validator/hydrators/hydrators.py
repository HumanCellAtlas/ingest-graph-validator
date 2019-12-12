import click
import logging
from py2neo import Graph

from ..config import Config
from .xls_hydrator import XlsHydrator


def get_hydrators():
    return [xls]


def init_graph(ctx):
    logger = logging.getLogger(__name__)

    ctx.obj.graph = Graph(Config['NEO4J_DB_URL'], user=Config['NEO4J_DB_USERNAME'],
                          password=Config['NEO4J_DB_PASSWORD'])

    if not ctx.obj.params['keep_contents']:
        logger.debug("cleaning up graph")
        ctx.obj.graph.delete_all()

    logger.debug("started neo4j graph instance")


def check_backend(ctx):
    logger = logging.getLogger(__name__)

    if ctx.obj.backend is None:
        logger.error("no backend container found")
        exit(1)
    logger.debug("backend container is up")


@click.command()
@click.argument("xls_filename", type=click.Path(exists=True))
@click.pass_context
def xls(ctx, xls_filename):
    """Import data from an XLS spreadsheet."""

    check_backend(ctx)
    init_graph(ctx)

    XlsHydrator(xls_filename).hydrate()
