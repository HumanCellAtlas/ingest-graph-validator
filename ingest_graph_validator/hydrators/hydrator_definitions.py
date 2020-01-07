# -*- coding: utf-8 -*-

"""Hydrator module definition and parent class for the ingest-graph-validator."""

import click
import logging

from .xls_hydrator import XlsHydrator


def check_backend(backend):
    logger = logging.getLogger(__name__)

    if backend is None:
        logger.error("no backend container found")
        exit(1)

    logger.debug("backend container is up")


def get_hydrators():
    """ List of available hydrators """
    return [xls]


""" XLS Hydrator cli command definition """
@click.command()
@click.argument("xls_filename", type=click.Path(exists=True))
@click.pass_context
def xls(ctx, xls_filename):
    """Import data from an XLS spreadsheet."""

    check_backend(ctx.obj.backend)
    XlsHydrator(ctx.obj.graph, ctx.obj.params['keep_contents'], xls_filename).hydrate()
