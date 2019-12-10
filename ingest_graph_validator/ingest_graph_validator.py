# -*- coding: utf-8 -*-

"""
Package entrypoint for the graph validator application

This is the CLI application that will be used when running the graph validator as a standalone application. The
other option is to run a docker-compose with the whole architecture (that will only run tests, not open a interactive
instance of Neo4j's bloom).

Spins up the database backend if needed, and either runs tests or starts up the ui.
The command line parameter parsing is also performed here, as is logging initialization.HCA
"""

import atexit
import click
import docker
import logging
import os
import requests
import sys
import time
import webbrowser

from .graph_import.sheet2neo import fillNeoGraph
from .config import Config
from .logger import init_logger


source_dir = os.path.join(os.path.dirname(__file__), "graph_import", "import_sources")


class GraphImporterSourceCLI(click.MultiCommand):

    def list_commands(self, ctx):
        source_list = []

        for filename in os.listdir(source_dir):
            if filename.endswith("_source.py"):
                source_list.append(filename[:-10])

        source_list.sort()
        return source_list

    def get_command(self, ctx, name):
        ns = {}
        source_filename = os.path.join(source_dir, name + "_source.py")

        with open(source_filename) as source_file:
            code = compile(source_file.read(), source_filename, 'exec')
            eval(code, ns, ns)

        return ns['main']


@click.command(cls=GraphImporterSourceCLI, context_settings={'help_option_names': ["-h", "--help"]})
@click.option("-t", "--test", default=False, is_flag=True, help="Run validation tests without starting the user interface.")
@click.option("-b", "--bolt_port", type=click.INT, help="Neo4j backend bolt port.", default=Config['NEO4J_BOLT_PORT'], show_default=True)
@click.option("-w", "--web_port", type=click.INT, help="Neo4j web frontend port.", default=Config['NEO4J_FRONTEND_PORT'], show_default=True)
@click.option("-k", "--keep_backend", default=False, is_flag=True, help="Do not close the neo4j backend on exit,\
              useful for keeping the data for further executions.")
@click.option("-l", "--log_level", default="INFO", help="Log level (DEBUG, INFO, WARNING, ERROR)", show_default=True)
def cli(test, bolt_port, web_port, keep_backend, log_level):

    logger = logging.getLogger(__name__)

    # Check params.
    if xls and subid:
        click.echo("Error: \"-x\" / \"--xls\" and \"-u\" / \"--subid\" are mutually exclusive.")
        exit(1)

    if not xls and not subid:
        click.echo("Error: please specify either \"-x\" / \"--xls\" or \"-u\" / \"--subid\".")
        exit(1)

    # Start backend.
    logger.info("starting graph validator application")
    neo4j_frontend_url = f"http://127.0.0.1:{web_port}"
    neo4j_server = Neo4jServer(bolt_port, web_port, neo4j_frontend_url, keep_backend)
    neo4j_server.start()

    if xls:
        logger.info(f"starting xls import using source [{xls}]")
        fillNeoGraph(xls, fresh_start=True)
    elif subid:
        logger.info(f'starting ingest api import using submission uuid [{subid}]')
        # TODO: SUBID IMPORT

    if not test:
        webbrowser.open_new_tab(neo4j_frontend_url)
        logger.info(f"web interface for neo4j started at {neo4j_frontend_url}")
        click.echo(f"The web interface is running {neo4j_frontend_url}. Press ctrl+c when you are finished.")
        while True:
            input()


def cleanup_handler(container, keep_backend):
    logger = logging.getLogger(__name__)
    if not keep_backend:
        logger.info("cleaning up containers")
        container.stop()
        container.remove()
    exit()


# Starts a neo4j docker instance.
class Neo4jServer:
    def __init__(self, bolt_port, web_port, neo4j_frontend_url, keep_backend):
        self._bolt_port = bolt_port
        self._web_port = web_port
        self._neo4j_frontend_url = neo4j_frontend_url
        self._keep_backend = keep_backend

        self._logger = logging.getLogger(__name__)
        self._docker_client = docker.from_env()
        self.container_name = "neo4j-server"

    def start(self):
        # Returns if container exists already (coming from docker-compose).
        containers_list = self._docker_client.containers.list(filters={"name": self.container_name})

        if len(containers_list):
            atexit.register(cleanup_handler, containers_list[0], self._keep_backend)
            self._logger.info("neo4j backend is already running")
            return

        neo4j_server_env = [f"NEO4J_AUTH={Config['NEO4J_DB_USERNAME']}/{Config['NEO4J_DB_PASSWORD']}"]
        neo4j_server_ports = {self._bolt_port: self._bolt_port, self._web_port: self._web_port}

        self._logger.info("starting neo4j backend")
        neo4j_server = self._docker_client.containers.run(
            "neo4j:latest",
            name=self.container_name,
            ports=neo4j_server_ports,
            environment=neo4j_server_env,
            detach=True)

        # Cleanup of docker containers when the application ends.
        atexit.register(cleanup_handler, neo4j_server, self._keep_backend)

        # Wait for server initialization.
        while True:
            frontend_up = 0
            try:
                frontend_up = requests.head(self._neo4j_frontend_url).status_code
            except requests.ConnectionError:
                time.sleep(2)

            if frontend_up == 200:
                self._logger.info("neo4j server is up")
                break


# Stats logging before Click parses command line.
def main():
    log_level = "INFO"

    for index, param in enumerate(sys.argv):
        if param == "-l" or param == "--log_level":
            log_level = sys.argv[index + 1]

    init_logger("ingest_graph_validator", log_level)
    cli()


if __name__ == "__main__":
    main()
