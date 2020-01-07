# -*- coding: utf-8 -*-

"""Hydrator module definition and parent class for the ingest-graph-validator."""

import click
import logging

from .xls_hydrator import XlsHydrator
from .ingest_hydrator import IngestHydrator
from .biomodels_hydrator import BiomodelsHydrator


def check_backend(backend):
    logger = logging.getLogger(__name__)

    if backend is None:
        logger.error("no backend container found")
        exit(1)

    logger.debug("backend container is up")


def get_hydrators():
    """ List of available hydrators """
    return [xls, ingest, biomodels]


""" XLS Hydrator cli command definition """
@click.command()
@click.argument("xls_filename", type=click.Path(exists=True))
@click.pass_context
def xls(ctx, xls_filename):
    """Import data from an XLS spreadsheet."""

    check_backend(ctx.obj.backend)
    XlsHydrator(ctx.obj.graph, ctx.obj.params['keep_contents'], xls_filename).hydrate()


""" Ingest Service Hydrator cli command definition """
@click.command()
@click.argument("subid", type=click.UUID)
@click.pass_context
def ingest(ctx, subid):
    """Import data from a Ingest Service submission."""

    check_backend(ctx.obj.backend)
    IngestHydrator(ctx.obj.graph, ctx.obj.params['keep_contents'], subid).hydrate()


""" Biomodels hydrator cli command definition """
@click.command()
@click.argument("param", type=click.STRING)
@click.pass_context
def biomodels(ctx, param):
    """Import data from BioModels."""

    check_backend(ctx.obj.backend)
    BiomodelsHydrator(ctx.obj.graph, ctx.obj.params['keep_contents'], param).hydrate()
