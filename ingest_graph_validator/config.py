import os


Config = {
    'INGEST_API': os.environ.get('INGEST_API', 'https://api.ingest.data.humancellatlas.org'),
    'NEO4J_DB_URL': os.environ.get('NEO4J_DB_URL', 'bolt://localhost:7687'),
    'NEO4J_DB_USERNAME': os.environ.get('NEO4J_DB_USERNAME', 'neo4j'),
    'NEO4J_DB_PASSWORD': os.environ.get('NEO4J_DB_PASSWORD', 'password'),
}
