# -*- coding: utf-8 -*-

"""
Package entrypoint for use as a standalone application.

Spins up the database backend if needed, and either runs tests or starts up the ui.
The command line parameter parsing is also performed here, as is logging initialization.
"""

import atexit
import click
import docker
import logging
import requests
import time
import webbrowser

from .graph_import.sheet2neo import fillNeoGraph
from .config import Config
from .logger import init_logger


@click.command(context_settings={'help_option_names': ["-h", "--help"]})
@click.option("-t", "--test", default=False, is_flag=True, help="Run validation tests without starting the user interface.")
@click.option("-x", "--xls", type=click.Path(exists=True), help="Fetch data from xls spreadsheet.")
@click.option("-u", "--subid", type=click.UUID, help="Fetch data from ingest using submission id.")
@click.option("-b", "--bolt_port", type=click.INT, help="Neo4j backend bolt port.", default=Config['NEO4J_BOLT_PORT'], show_default=True)
@click.option("-w", "--web_port", type=click.INT, help="Neo4j web frontend port.", default=Config['NEO4J_FRONTEND_PORT'], show_default=True)
@click.option("-k", "--keep_backend", default=False, is_flag=True, help="Do not close the neo4j backend on exit,\
    useful for keeping the data for further executions.")
@click.option("-l", "--log_level", default="INFO", help="Log level (INFO, WARNING, ERROR)", show_default=True)
def main(test,
         xls,
         subid,
         bolt_port=Config['NEO4J_BOLT_PORT'],
         web_port=Config['NEO4J_FRONTEND_PORT'],
         keep_backend=False,
         log_level="INFO"):

    init_logger(__name__, log_level)
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


if __name__ == "__main__":
    main()
