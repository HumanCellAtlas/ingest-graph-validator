# HCA Ingest Service graph validation suite

The purpose of this suite is double:

1. Enables data wranglers to visually analyze the relationships inside a submission to look for inconsistencies.
2. Provides an automated graph validator that runs a series of specified tests and can be run fully containerized.


## Usage

At the moment only the interactive visualizer is ready, loading the data from a spreadsheet. It uses Neo4j Bloom web frontend.

```
pip install .
ingest-graph-validator --xls PATH_TO_SPREADSHEET
```

This will install the package and start the neo4j server, convert a XLS spreadsheet to a graph and show the bloom web frontend.

The documentation will be expanded soon.


## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter).