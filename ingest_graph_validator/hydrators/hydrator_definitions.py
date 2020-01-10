# -*- coding: utf-8 -*-

"""Hydrator module definition and parent class for the ingest-graph-validator."""

import click

from .xls_hydrator import XlsHydrator
from .ingest_hydrator import IngestHydrator
from .biomodels_hydrator import BiomodelsHydrator
from .json_schema_hydrator import JsonSchemaHydrator


def get_hydrators():
    """ List of available hydrators """
    return [xls, ingest, biomodels, jsonschema]


""" XLS Hydrator cli command definition """
@click.command()
@click.argument("xls_filename", type=click.Path(exists=True))
@click.pass_context
def xls(ctx, xls_filename):
    """Import data from an XLS spreadsheet."""

    XlsHydrator(ctx.obj.graph, xls_filename).hydrate()


""" Ingest Service Hydrator cli command definition """
@click.command()
@click.argument("subid", type=click.UUID)
@click.pass_context
def ingest(ctx, subid):
    """Import data from a Ingest Service submission."""

    IngestHydrator(ctx.obj.graph, subid).hydrate()


""" Biomodels hydrator cli command definition """
@click.command()
@click.argument("param", type=click.STRING)
@click.pass_context
def biomodels(ctx, param):
    """Import data from BioModels."""

    BiomodelsHydrator(ctx.obj.graph, param).hydrate()


""" JSON Schema hydrator command definition """
@click.command()
@click.argument("schema_path", type=click.Path(exists=True))
@click.pass_context
def jsonschema(ctx, schema_path):
    """Import data from a JSON Schema."""

    JsonSchemaHydrator(ctx.obj.graph, schema_path).hydrate()
