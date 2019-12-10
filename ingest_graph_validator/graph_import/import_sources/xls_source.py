# -*- coding: utf-8 -*-

"""Excel spreadsheet importer class."""

import click
import logging


class XlsSource:
    def __init__(self, xls_filename):
        self.xls_filename = xls_filename

        __name__ = "ingest_graph_validator.graph_import.import_sources.xls_source"
        self.logger = logging.getLogger(__name__)

        self.logger.debug(f"started {__class__.__name__} source with params {self.xls_filename}")


@click.command()
@click.argument("xls_filename", type=click.Path(exists=True))
def main(xls_filename):
    """Import data from an XLS spreadsheet."""

    source = XlsSource(xls_filename)

    return source
