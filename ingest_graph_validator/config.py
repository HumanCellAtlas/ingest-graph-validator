import os


Config = {
    'INGEST_API': os.environ.get('INGEST_API', 'https://api.ingest.data.humancellatlas.org'),
    'NEO4J_BOLT_PORT': os.environ.get('NEO4J_BOLT_PORT', 7687),
    'NEO4J_FRONTEND_PORT': os.environ.get('NEO4J_FRONTEND_PORT', 7474),
    'NEO4J_DB_URL': os.environ.get('NEO4J_FRONTEND_URL', 'bolt://127.0.0.1:7687'),
    'NEO4J_DB_USERNAME': os.environ.get('NEO4J_DB_USERNAME', 'neo4j'),
    'NEO4J_DB_PASSWORD': os.environ.get('NEO4J_DB_PASSWORD', 'password'),
}
