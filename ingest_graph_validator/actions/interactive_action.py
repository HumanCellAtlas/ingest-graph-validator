# -*- coding: utf-8 -*-

"""Launches the Neo4j web frontend."""

import logging
import requests
import time
import webbrowser


FRONTEND_MAX_RETRIES = 5
FRONTEND_RETRY_TIMEOUT = 2


class InteractiveAction:

    def __init__(self, web_port):
        self._web_port = web_port
        self._logger = logging.getLogger(__name__)

    def run(self):
        neo4j_frontend_url = f"http://127.0.0.1:{self._web_port}"

        # Wait for server initialization.
        retry_count = 0
        while True:
            frontend_up = 0

            try:
                frontend_up = requests.head(neo4j_frontend_url).status_code
            except requests.ConnectionError:
                if retry_count == FRONTEND_MAX_RETRIES:
                    self._logger.error("frontend connection timed out")
                    exit(1)

                retry_count += 1
                time.sleep(2)

            if frontend_up == 200:
                self._logger.info("neo4j server seems to be up")
                break

        webbrowser.open_new_tab(neo4j_frontend_url)

        self._logger.info(f"web interface for neo4j started at {neo4j_frontend_url}")
        print(f"The web interface is running {neo4j_frontend_url}. Press ctrl+c when you are finished.")

        while True:
            input()
