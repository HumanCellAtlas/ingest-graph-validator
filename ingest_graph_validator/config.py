import os

Defaults = {
    'LOG_LEVEL': "ERROR",
    'NEO4J_BOLT_PORT': 7687,
    'NEO4J_FRONTEND_PORT': 7474
}

Config = {
    'LOG_LEVEL': os.environ.get("INGEST_GRAPH_VALIDATOR_LOG_LEVEL",
                                "ERROR"),
    'INGEST_API': os.environ.get("INGEST_GRAPH_VALIDATOR_INGEST_API_URL",
                                 "https://api.ingest.data.humancellatlas.org"),
    'NEO4J_BOLT_PORT': os.environ.get("INGEST_GRAPH_VALIDATOR_NEO4J_BOLT_PORT",
                                      Defaults['NEO4J_BOLT_PORT']),
    'NEO4J_FRONTEND_PORT': os.environ.get("INGEST_GRAPH_VALIDATOR_NEO4J_FRONTEND_PORT",
                                          Defaults['NEO4J_FRONTEND_PORT']),
    'NEO4J_DB_URL': os.environ.get("INGEST_GRAPH_VALIDATOR_NEO4J_FRONTEND_URL",
                                   "bolt://127.0.0.1:7687"),
    'NEO4J_DB_USERNAME': os.environ.get("INGEST_GRAPH_VALIDATOR_NEO4J_DB_USERNAME",
                                        "neo4j"),
    'NEO4J_DB_PASSWORD': os.environ.get("INGEST_GRAPH_VALIDATOR_NEO4J_DB_PASSWORD",
                                        "password"),
    'BACKEND_CONTAINER_NAME': "neo4j-server"
}
