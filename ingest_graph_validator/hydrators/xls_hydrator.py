# -*- coding: utf-8 -*-

"""Excel spreadsheet hydrator class."""

import logging

from ingest.api.ingestapi import IngestApi
from ingest.importer.importer import XlsImporter
from ..config import Config


class XlsHydrator:

    def __init__(self, xls_filename):
        self._xls_filename = xls_filename
        self._entity_map = None

        self._logger = logging.getLogger(__name__)
        self._logger.debug(f"started xls hydrator for file [{self._xls_filename}]")


    def hydrate(self):
        self.get_entity_map()

        print(f"\n\n\n{(self._entity_map.entities_dict_by_type)}\n\n\n")
        print(self._entity_map.entities_dict_by_type['project']['_unknown_1'].__dict__)

        return {"a": 1, "b": 2}


    def get_entity_map(self):
        self._logger.info("importing spreadsheet")

        ingest_api = IngestApi(url=Config['INGEST_API'])
        importer = XlsImporter(ingest_api)

        self._entity_map = importer.dry_run_import_file(file_path=self._xls_filename)