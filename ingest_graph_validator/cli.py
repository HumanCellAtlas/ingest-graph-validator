# -*- coding: utf-8 -*-

"""
Package entrypoint for use as a standalone application.
Spins up the database backend if needed, and either runs tests or starts up the ui.
"""

import atexit
import click
import docker
import requests
import time
import webbrowser


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-s", "--silent", default=False, is_flag=True, help="Run validation tests without starting the user interface.")
@click.option("-x", "--xls", type=click.Path(exists=True), help="Fetch data from xls spreadsheet.")
@click.option("-u", "--subid", type=click.UUID, help="Fetch data from ingest using submission id.")
@click.option("-b", "--bolt_port", type=click.INT, help="Neo4j backend bolt port.", default=7687, show_default=True)
@click.option("-w", "--web_port", type=click.INT, help="Neo4j web frontend port.", default=7474, show_default=True)
@click.option("-k", "--keep_backend", default=False, is_flag=True, help="Do not close the neo4j backend on exit,\
    useful for keeping the data for further executions")
def main(silent, xls, subid, bolt_port, web_port, keep_backend):
    if xls and subid:
        click.echo("Error: \"-x\" / \"--xls\" and \"-u\" / \"--subid\" are mutually exclusive.")
        exit(1)

    if not xls and not subid:
        click.echo("Error: please specify either \"-x\" / \"--xls\" or \"-u\" / \"--subid\".")
        exit(1)

    neo4j_frontend_url = f"http://127.0.0.1:{web_port}"
    start_neo4j_server(bolt_port, web_port, neo4j_frontend_url, keep_backend)

    # TODO: CHOOSE BETWEEN XLS AND UUID
    from .graph_import.sheet2neo import fillNeoGraph
    fillNeoGraph(xls, fresh_start=True)

    if not silent:
        webbrowser.open_new_tab(neo4j_frontend_url)
        print(f"[START] all done! web interface for neo4j in {neo4j_frontend_url}")
        print(f"[START] press ctrl+c when you are finished")
        while True:
            input()


def cleanup_handler(container, keep_backend):
    if not keep_backend:
        print("[STOP] cleaning up containers")
        container.stop()
        container.remove()
    exit()


# Starts a neo4j docker instance.
def start_neo4j_server(bolt_port, web_port, neo4j_frontend_url, keep_backend):
    docker_client = docker.from_env()

    # Returns if container exists already (coming from docker-compose).
    containers_list = docker_client.containers.list(filters={"name": "neo4j-server"})
    if len(containers_list):
        atexit.register(cleanup_handler, containers_list[0], keep_backend)
        print("[START] neo4j backend is already running")
        return

    neo4j_server_env = ["NEO4J_AUTH=neo4j/password"]
    neo4j_server_ports = {bolt_port: bolt_port, web_port: web_port}

    print("[START] starting neo4j backend")
    neo4j_server = docker_client.containers.run(
        "neo4j:latest",
        name="neo4j-server",
        ports=neo4j_server_ports,
        environment=neo4j_server_env,
        detach=True)

    # Cleanup of docker containers when the application ends.
    atexit.register(cleanup_handler, neo4j_server, keep_backend)

    # Wait for server initialization.
    while True:
        frontend_up = 0
        try:
            frontend_up = requests.head(neo4j_frontend_url).status_code
        except requests.ConnectionError:
            time.sleep(2)

        if frontend_up == 200:
            print("[START] neo4j server is up")
            break


if __name__ == "__main__":
    main()
