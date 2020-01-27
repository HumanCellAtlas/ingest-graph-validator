# -*- coding: utf-8 -*-

"""
Package entrypoint for the graph validator application

This is the CLI application that will be used when running the graph validator as a standalone application. The
other option is to run a docker-compose with the whole architecture (that will only run tests, not open a interactive
instance of Neo4j's bloom).

Spins up the database backend if needed, and either runs tests or starts up the ui.
The command line parameter parsing is also performed here, as is logging initialization.HCA
"""

import click
import docker
import glob
import logging
import os
from pathlib import Path
import requests
import zipfile

from py2neo import Graph

from .config import Config, Defaults, init_config, NEO4J_PLUGINS
from .logger import init_logger, log_levels_map
from .data_store import DataStore
from .actions import get_actions
from .hydrators import get_hydrators
from .utils import download_file


@click.group(context_settings={'help_option_names': ["-h", "--help"]})
@click.option("-l", "--log-level", type=click.Choice(list(log_levels_map.keys())), default=Defaults['LOG_LEVEL'],
              show_default=True, show_choices=True, help="Log level")
@click.option("-b", "--bolt-port", type=click.INT, default=Defaults['NEO4J_BOLT_PORT'], show_default=True,
              help="Specify bolt port.")
@click.option("-f", "--frontend-port", type=click.INT, default=Defaults['NEO4J_FRONTEND_PORT'], show_default=True,
              help="Specify web frontend port.")
@click.pass_context
def entry_point(ctx, log_level, bolt_port, frontend_port):
    """HCA Ingest graph validation Suite."""

    init_config()

    Config['LOG_LEVEL'] = log_level
    Config['NEO4J_BOLT_PORT'] = bolt_port
    Config['NEO4J_FRONTEND_PORT'] = frontend_port

    init_logger("ingest_graph_validator", log_level)
    logger = logging.getLogger(__name__)
    logger.debug("at entrypoint")

    ctx.obj = DataStore()
    ctx.obj.backend = Neo4jServer()
    ctx.obj.graph = Graph(f"{Config['NEO4J_DB_URL']}:{Config['NEO4J_BOLT_PORT']}", user=Config['NEO4J_DB_USERNAME'],
                          password=Config['NEO4J_DB_PASSWORD'])

    populate_commands()


@entry_point.command()
@click.pass_context
def init(ctx):
    """Start Neo4j backend."""

    logger = logging.getLogger(__name__)
    logger.info("starting graph validator Neo4j backend container")

    ctx.obj.backend.start()


@entry_point.command()
@click.option("-r", "--remove", is_flag=True, default=False, help="Remove container (clean up all data).")
@click.pass_context
def shutdown(ctx, remove):
    """Stop Neo4j backend."""

    logger = logging.getLogger(__name__)
    logger.info("cleaning up containers")

    ctx.obj.backend = Neo4jServer()
    ctx.obj.backend.stop()

    if remove:
        ctx.obj.backend.remove()


@entry_point.group()
@click.option("-k", "--keep_contents", is_flag=True, default=False, help="Keep previous contents of the database.")
@click.pass_context
def hydrate(ctx, keep_contents):
    """Populate the Neo4j graph database using different sources."""

    logger = logging.getLogger(__name__)

    if not ctx.obj.backend.is_alive():
        logger.error("no backend container found")
        exit(1)

    if not keep_contents:
        logger.debug("cleaning up graph")
        ctx.obj.graph.delete_all()


@entry_point.group()
@click.pass_context
def action(ctx):
    """Run different actions on the graph database."""

    logger = logging.getLogger(__name__)

    if not ctx.obj.backend.is_alive():
        logger.error("no backend container found")
        exit(1)


def populate_commands():
    logger = logging.getLogger(__name__)

    for hydrator in get_hydrators():
        hydrate.add_command(hydrator)
        logger.debug(f"added hydrator [{hydrator.name}]")

    for action_command in get_actions():
        action.add_command(action_command)
        logger.debug(f"added action [{action_command.name}]")



class Neo4jServer:

    def __init__(self, bolt_port=Config['NEO4J_BOLT_PORT'], frontend_port=Config['NEO4J_FRONTEND_PORT']):
        self._bolt_port = bolt_port
        self._frontend_port = frontend_port

        self._plugins_full_path = os.path.abspath("./neo4j_plugins")
        Path(self._plugins_full_path).mkdir(parents=True, exist_ok=True)

        self._logger = logging.getLogger(__name__)
        self._docker_client = self.get_docker_client()
        self.container_name = Config['BACKEND_CONTAINER_NAME']
        self._container = self.attach_backend_container(self.container_name)

    def start(self):
        if not self.check_plugins():
            self.install_plugins()

        if self._container is not None:
            if self._container.status == "exited":
                self._container.start()
                self._logger.info("backend container already existed but was stopped, it has been started")
            else:
                self._logger.error("backend container is already running")
            exit(1)

        neo4j_server_ports = {self._bolt_port: self._bolt_port, self._frontend_port: self._frontend_port}

        self._logger.info(f"starting backend container [{self.container_name}]")

        neo4j_plugins_names = [os.path.basename(x) for x in glob.glob(f"{self._plugins_full_path}/*")]

        self._logger.debug(f"found {len(neo4j_plugins_names)} plugins for neo4j: {neo4j_plugins_names}")

        self._container = self._docker_client.containers.run(
            image=Config['NEO4J_IMAGE'],
            name=self.container_name,
            ports=neo4j_server_ports,
            detach=True,
            environment=Config['NEO4J_DB_ENV_VARS'],
            volumes={
                self._plugins_full_path: {
                    'bind': "/var/lib/neo4j/plugins",
                    'mode': "rw",
                }
            }
        )

        self._logger.info(f"The web interface is running at http://{Config['NEO4J_DB_URL']}:{self._frontend_port}")

    def stop(self):
        if self._container is None:
            self._logger.debug("stop: no backend container found")
            return

        self._container.stop()
        self._logger.info(f"backend container [{self.container_name}] stopped")

    def remove(self):
        if self._container is None:
            self._logger.debug("remove: no backend container found")
            return

        self._container.remove()
        self._logger.info(f"backend container [{self.container_name}] removed")

    def is_alive(self):
        return self._container is not None

    def attach_backend_container(self, container_name):
        docker_client = self.get_docker_client()
        containers_list = docker_client.containers.list(all=True, filters={"name": container_name})

        if len(containers_list):
            self._logger.info(f"attached to backend container [{container_name}]")
            return containers_list[0]

        self._logger.debug("found no backend container to attach")
        return None

    def get_docker_client(self):
        docker_client = docker.from_env()

        try:
            docker_client.ping()
        except requests.exceptions.ConnectionError:
            self._logger.error("docker is not running or unresponsive, you probably have to install docker")
            exit(1)

        return docker_client

    def check_plugins(self):
        """Checks the amount of plugins existing matches those specified in config."""
        installed_plugin_count = len([name for name in os.listdir(self._plugins_full_path)
                                     if os.path.isfile(f"{self._plugins_full_path}/{name}")])
        plugin_count = len(NEO4J_PLUGINS.keys())

        self._logger.debug(f"{installed_plugin_count}/{plugin_count} neo4j plugins found")

        return installed_plugin_count == plugin_count

    def install_plugins(self):
        """Fetches neo4j plugins, and unzips if needed."""
        self._logger.info(f"installing neo4j plugins to [{self._plugins_full_path}]")

        for plugin_name, plugin_url in NEO4J_PLUGINS.items():
            self._logger.debug(f"getting plugin {plugin_name}")

            destination_filename = f"{self._plugins_full_path}/{plugin_url.split('/')[-1]}"
            download_file(plugin_url, f"{destination_filename}")

            if destination_filename.split('.')[-1] == "zip":
                self._logger.debug(f"uncompresing plugin {plugin_name}")

                with zipfile.ZipFile(destination_filename, 'r') as zipped_plugin_file:
                    zipped_plugin_file.extractall(self._plugins_full_path)

                os.remove(destination_filename)

        self._logger.debug(f"done installing neo4j plugins")


if __name__ == "__main__":
    entry_point()
