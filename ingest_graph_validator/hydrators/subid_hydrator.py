# -*- coding: utf-8 -*-

"""Ingest API submission id hydrator."""

import click
import logging


class SubidSource:
    def __init__(self, subid):
        self.subid = subid
        self.logger = logging.getLogger(__name__)

        self.logger.debug(f"started {__name__} source with params {self.subid}")


@click.command()
@click.argument("subid", type=click.UUID)
def main():
    """Import data from the specified Ingest Submission ID."""
    pass
