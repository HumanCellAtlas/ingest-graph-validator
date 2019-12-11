# -*- coding: utf-8 -*-

"""Biomodels API importer class."""

import click
import logging


class BiomodelsSource:
    def __init__(self, url):
        self.url = url
        self.logger = logging.getLogger(__name__)

        self.logger.debug(f"started {__name__} source with params {url}")


@click.command()
@click.argument("url", type=click.STRING)
def main(url):
    """Import data from the BioModels API."""

    BiomodelsSource(url)
    pass
