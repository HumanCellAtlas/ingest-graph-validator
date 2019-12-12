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
import logging

from .config import Config
from .logger import init_logger, log_levels_map
from .data_store import DataStore
from .actions import get_actions
from .hydrators import get_hydrators


@click.group(context_settings={'help_option_names': ["-h", "--help"]})
@click.option("-l", "--log-level", type=click.Choice(list(log_levels_map.keys())), help="Log level", show_default=True,
              show_choices=True, default=Config['LOG_LEVEL'])
@click.option("-b", "--bolt-port", type=click.INT, help="Specify bolt port.", show_default=True,
              default=Config['NEO4J_BOLT_PORT'])
@click.option("-f", "--frontend-port", type=click.INT, help="Specify web frontend port.", show_default=True,
              default=Config['NEO4J_FRONTEND_PORT'])
@click.pass_context
def entry_point(ctx, log_level, bolt_port, frontend_port):
    # TODO: COMPLETE DOC
    """HCA Ingest graph validation tool."""

    Config['LOG_LEVEL'] = log_level
    Config['NEO4J_BOLT_PORT'] = bolt_port
    Config['NEO4J_FRONTEND_PORT'] = frontend_port

    init_logger("ingest_graph_validator", log_level)
    logger = logging.getLogger(__name__)
    logger.debug("at entrypoint")

    ctx.obj = DataStore()
    ctx.obj.backend = Neo4jServer()
    populate_commands()


@entry_point.command()
@click.pass_context
def init(ctx):
    """Start Neo4j backend."""

    logger = logging.getLogger(__name__)
    logger.info("starting graph validator Neo4j backend container")

    ctx.obj.backend.start()


@entry_point.command()
@click.option("-r", "--remove", default=False, is_flag=True, help="Remove container (clean up all data).")
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
@click.pass_context
def hydrate(ctx):
    """Populate the Neo4j graph database using different sources."""
    pass


@entry_point.group()
@click.pass_context
def action(ctx):
    """Run different actions on the graph database."""
    pass


def populate_commands():
    logger = logging.getLogger(__name__)

    for hydrator in get_hydrators():
        hydrate.add_command(hydrator)
        logger.debug(f"added hydrator {hydrator.name}")

    for action_command in get_actions():
        action.add_command(action_command)
        logger.debug(f"added action {action_command.name}")


def attach_backend_container(container_name):
    logger = logging.getLogger(__name__)
    docker_client = docker.from_env()
    containers_list = docker_client.containers.list(filters={"name": container_name})

    if len(containers_list):
        logger.info(f"attached to backend container [{container_name}]")
        return containers_list[0]

    logger.debug("found no backend container")
    return None


class Neo4jServer:

    def __init__(self, bolt_port=Config['NEO4J_BOLT_PORT'], frontend_port=Config['NEO4J_FRONTEND_PORT']):
        self._bolt_port = bolt_port
        self._frontend_port = frontend_port

        self._logger = logging.getLogger(__name__)
        self._docker_client = docker.from_env()
        self.container_name = Config['BACKEND_CONTAINER_NAME']
        self._container = attach_backend_container(self.container_name)

    def start(self):
        if self._container is not None:
            self._logger.error("a backend container already exists, shut down first")
            exit(1)

        neo4j_server_env = [f"NEO4J_AUTH={Config['NEO4J_DB_USERNAME']}/{Config['NEO4J_DB_PASSWORD']}"]
        neo4j_server_ports = {self._bolt_port: self._bolt_port, self._frontend_port: self._frontend_port}

        self._logger.info(f"starting backend container [{self.container_name}]")
        self._container = self._docker_client.containers.run("neo4j:latest", name=self.container_name,
                                                             ports=neo4j_server_ports, environment=neo4j_server_env,
                                                             detach=True)

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


if __name__ == "__main__":
    entry_point()
