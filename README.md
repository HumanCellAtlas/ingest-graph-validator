# ingest-graph-validator
Prototype code for ingest metadata graph validation. This is to test assumptions that are not encoded in the schema. For example, we would like a warning if a bundle links a donor directly to a sequencing file. This will eventually be an integrated user tool to run before submission to check that linking and data modelling have been done correctly.

## Background

Here are graph assumptions that this validator should check:
https://github.com/HumanCellAtlas/hca-data-wrangling/blob/master/docs/Graph_assumptions.md

Here are the use cases for this code (in progress):
https://github.com/HumanCellAtlas/hca-data-wrangling/blob/master/docs/20181211_graph_use_cases.md

## How to run code?
