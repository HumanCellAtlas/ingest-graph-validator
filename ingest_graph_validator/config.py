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
    'AMQP_CONNECTION': "amqp://guest:guest@localhost:5672",
    'AMQP_EXCHANGE_NAME': "ingest.validation.exchange",
    'AMQP_QUEUE_NAME': "ingest.graph.validation.queue",
    'AMQP_ROUTING_KEY': "ingest.graph.validation.queue",
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
    'AMQP_CONNECTION': os.environ.get("AMQP_CONNECTION", Defaults['AMQP_CONNECTION']),
    'AMQP_EXCHANGE_NAME': os.environ.get("AMQP_EXCHANGE_NAME", Defaults['AMQP_EXCHANGE_NAME']),
    'AMQP_QUEUE_NAME': os.environ.get("AMQP_QUEUE_NAME", Defaults['AMQP_QUEUE_NAME']),
    'AMQP_ROUTING_KEY': os.environ.get("AMQP_ROUTING_KEY", Defaults['AMQP_ROUTING_KEY']),

}


# These are the plugins to download. A way to automate new versions have to be refactored in here.
NEO4J_PLUGINS = {
    'algorithms': 'https://s3-eu-west-1.amazonaws.com/com.neo4j.graphalgorithms.dist/neo4j-graph-algorithms-3.5.14.0-standalone.zip',
    'apoc': 'https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/3.5.0.7/apoc-3.5.0.7-all.jar',
}


def init_config():
    Config['NEO4J_DB_ENV_VARS'] = [
        "NEO4J_ACCEPT_LICENSE_AGREEMENT=yes",
        "NEO4J_dbms_security_auth__enabled=false",
        f"NEO4J_AUTH={Config['NEO4J_DB_USERNAME']}/{Config['NEO4J_DB_PASSWORD']}",
        "NEO4J_dbms_security_procedures_unrestricted=algo.*",
        "NEO4J_dbms_security_procedures_unrestricted=apoc.*",
    ]
