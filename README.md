# HCA Ingest Service Graph Validation Suite

## What is this useful for in the scope of the HCA:

1. Enables data wranglers to visually analyze the relationships inside a submission to look for inconsistencies.
2. Provides an automated graph validator for which to create tests using step 1 and can be run fully containerized.


## Features

The suite is divided in two separate, extensible parts:

* **hydrators** enable users to import and populate data into a graph database. The reason not to call them importers is `import` is a reserved keyword in Python and `from importers import importer` is a bit confusing. :dizzy_face:

* **actions** provide different tools to work with the generated graph. The first and most important is to run a series of tests to validate the constraints Data Wranglers want to impose on submissions. Another action is generating reports and extracting statistics from the graph to send to the submitters. Any other actions can be implemented to extend the suite.

## Functionality

So far, the functionality planned is as follows (WIP items are still not fully implemented):

* Hydrators:
    * Ingest Service Spreadsheet.
    * Ingest Service API Submission.
    * BioSamples API (WIP).

* Actions:
    * Opening an interactive visualizer to query the graph.
    * Running tests on the graph.
    * Generating reports for the graph (WIP).


## Installation

The Graph Validator Suite requires docker running in the host machine.

### From the git repo

```
git clone git@github.com:HumanCellAtlas/ingest-graph-validator.git
cd ingest-graph-validator
pip install .
```

### <a name="install_pypi"></a>From PyPI

A Python package has been published in (PyPI)[https://pypi.org/project/ingest-graph-validator].

```pip install ingest-graph-validator```

If you install the Graph Validator Suite this way, you should head to the [github repo](https://github.com/HumanCellAtlas/ingest-graph-validator) to get the [graph tests](https://github.com/HumanCellAtlas/ingest-graph-validator/tree/master/graph_test_set) and the [graph reports](https://github.com/HumanCellAtlas/ingest-graph-validator/tree/master/graph_report_set).


## Usage

### Step by step usage for data wranglers

1. Once [installed from the Python package](#install_pypi), start the backend by opening a terminal and typing:

    `ingest-graph-validator init`

**Keep in mind**, first time executing the `init` command will take longer as it has to pull the Neo4j Docker image from dockerhub.

2. Import a spreadsheet:

    `ingest-graph-validator hydrate xls <spreadsheet filename>`

3. Go to <http://localhost:7474> in a browser to open the frontend.

4. Connect to the backend (you do not need to change any fields, leave username/password empty):

   ![](.readme/connect_backend.png)

5. You can then start writing [cypher queries](https://neo4j.com/graphacademy/online-training/introduction-to-neo4j/) in the input field on top of the web frontend to visualize the graph. For example:

    ```MATCH p=(n) RETURN p```

    Will show the entire graph. Keep in mind this will crash the browser on huge datasets.

**Note**
The server backend will continue running in the background, and you only need to open the browser again to continue your work. If you want to shutdown the backend, open a terminal and type:

`ingest-graph-validator shutdown`


### More help

The Graph Validator Suite uses a CLI similar to [git](https://git-scm.com/). Running a command without specifying anything else will show help for that command. At each level, the commands have different arguments and options. Running any subcommand with `-h` or `--help` with give you more information about it.

The root level commands are:

* **`ingest-graph-validator init`** starts the database backend and enables a frontend visualizer to query the database, in `http://localhost:7474` by default.

* **`ingest-graph-validator hydrate`** shows the list of available hydrators.

* **`ingest-graph-validator actions`** shows the list of available actions.

* **`ingest-graph-validator shutdown`** stops the backend.


## Containerized execution

WIP


## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter).
