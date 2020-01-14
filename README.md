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

### From the git repo

```
git clone git@github.com:HumanCellAtlas/ingest-graph-validator.git
cd ingest-graph-validator
pip install .
```

### From PyPI

A PyPI package will be published soon.


## Usage

### Basic usage for data wranglers

```
ingest-graph-validator init
ingest-graph-validator hydrate xls <spreadsheet filename>
```

After the hydrator is done loading the data, point a browser to <http://localhost:7474> to take a look at the graph.

### More help

The Suite uses a CLI similar to [git](https://git-scm.com/). Running a command without specifying anything else will show help for that command. At each level, the commands have different arguments and options. Running any subcommand with `-h` or `--help` with give you more information about it.

The root level commands are:

* **`ingest-graph-validator init`** starts the database backend and enables a frontend visualizer to query the database, in `http://localhost:7474` by default.

* **`ingest-graph-validator hydrate`** shows the list of available hydrators.

* **`ingest-graph-validator actions`** shows the list of available actions.

* **`ingest-graph-validator shutdown`** stops the backend.


## Containerized execution

WIP


## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter).
