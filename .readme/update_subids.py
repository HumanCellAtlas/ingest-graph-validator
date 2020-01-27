# -*- coding: utf-8 -*-

import dateutil.parser
import logging
import requests


def make_subid_list(project_list):
    subid_list = ""

    for project in project_list.values():
        subid_list += f"\n* {project['name']}: {project['subid']}"

    return subid_list


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s [%(name)s] - %(levelname)s: %(message)s", level=logging.INFO)
    logger = logging.getLogger(__name__)
    tracker_api_url = "https://tracker-api.data.humancellatlas.org/v0/projects"

    try:
        tracker_data = requests.get(tracker_api_url)
    except requests.exceptions.ConnectionError:
        logger.error(f"Not found: [{tracker_api_url}]")
        exit(1)

    if (tracker_data.status_code > 299):
        logger.error(f"API returned [{tracker_data.status_code}]")
        exit(1)

    project_data = tracker_data.json()
    project_list = {}

    for project in project_data:
        project_name = project['ingest-info'][0]['project_short_name'][0:64]
        project_subid = project['ingest-info'][0]['submission_uuid']
        project_date = dateutil.parser.isoparse(project['ingest-info'][0]['update_date'])

        for submission in project['ingest-info']:
            submission_date = dateutil.parser.isoparse(submission['update_date'])

            if project_date < submission_date:
                project_date = submission_date
                project_subid = submission['submission_uuid']

        new_project = {
            'name': project_name,
            'date': project_date,
            'subid': project_subid,
        }

        if project_name in project_list.keys():
            if project_date > project_list[project_name]['date']:
                project_list[project_name] = new_project
        else:
            project_list[project_name] = new_project

    subid_list = make_subid_list(project_list)

    with open("README.template", "rt") as template_file:
        with open("../README.md", "wt") as output_file:
            for line in template_file:
                if line == "{{SUBIDLIST}}\n":
                    output_file.write(subid_list)
                else:
                    output_file.write(line)
