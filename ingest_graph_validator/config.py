# -*- coding: utf-8 -*-

"""Configuration dictionaries."""

import os

Defaults = {
    'LOG_LEVEL': "INFO",
    'NEO4J_BOLT_PORT': 7687,
    'NEO4J_FRONTEND_PORT': 7474,
    'NEO4J_DB_URL': "localhost",
    'NEO4J_DB_USERNAME': "neo4j",
    'NEO4J_DB_PASSWORD': "password",
    'INGEST_API': "https://api.ingest.data.humancellatlas.org",
}


Config = {
    'LOG_LEVEL': os.environ.get("INGEST_GRAPH_VALIDATOR_LOG_LEVEL", "ERROR"),
    'INGEST_API': os.environ.get("INGEST_GRAPH_VALIDATOR_INGEST_API_URL", Defaults['INGEST_API']),
    'NEO4J_IMAGE': "neo4j:3.5.14-enterprise",
    'NEO4J_BOLT_PORT': os.environ.get("INGEST_GRAPH_VALIDATOR_NEO4J_BOLT_PORT", Defaults['NEO4J_BOLT_PORT']),
    'NEO4J_FRONTEND_PORT': os.environ.get("INGEST_GRAPH_VALIDATOR_NEO4J_FRONTEND_PORT", Defaults['NEO4J_FRONTEND_PORT']),
    'NEO4J_DB_URL': os.environ.get("INGEST_GRAPH_VALIDATOR_NEO4J_URL", Defaults['NEO4J_DB_URL']),
    'NEO4J_DB_USERNAME': os.environ.get("INGEST_GRAPH_VALIDATOR_NEO4J_DB_USERNAME", Defaults['NEO4J_DB_USERNAME']),
    'NEO4J_DB_PASSWORD': os.environ.get("INGEST_GRAPH_VALIDATOR_NEO4J_DB_PASSWORD", Defaults['NEO4J_DB_PASSWORD']),
    'BACKEND_CONTAINER_NAME': "neo4j-server",
}


def init_config():
    Config['NEO4J_DB_ENV_VARS'] = [
        "NEO4J_ACCEPT_LICENSE_AGREEMENT=yes",
        "NEO4J_dbms_security_auth__enabled=false",
        f"NEO4J_AUTH={Config['NEO4J_DB_USERNAME']}/{Config['NEO4J_DB_PASSWORD']}",
        "NEO4J_dbms_security_procedures_unrestricted=algo.*",
        "NEO4J_dbms_security_procedures_unrestricted=apoc.*",
    ]
