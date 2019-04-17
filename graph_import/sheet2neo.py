
from ingest.importer.importer import XlsImporter
import os

DEFAULT_INGEST_URL = os.environ.get('INGEST_API', 'http://api.ingest.data.humancellatlas.org')

def get_entity_map(file_path):
    importer = XlsImporter(DEFAULT_INGEST_URL)

    entity_map = importer.dry_run_import_file(file_path=file_path)
    print(entity_map)
