# Index of tests currently performed by the validator

Last updated: 2020-05-14

## Processes using 10x library preparation protocols have 3 or 4 files linked
#### Test description
Processes using 10x library preparation protocols have 3 or 4 files linked.

## Donor to file path must have at least 5 nodes
#### Test description
There should be a minimum of 5 modes from a donor to a data file:
`(donor_organism)->(process)->(biomaterial)->(process)->(file)`

## If a protocol has a document, a matching supplementary file must exist
#### Test description
If a protocol defines a supplementary file as the document describing it, there must exist a supplementary file that
is named exactly the same.
If any filenames are returned by this test, that means those files are missing as they are specified in protocols and
do not exist.

## All files which are not a supplementary file must have a link
#### Test description
Files must be attached to something, unless they are a supplementary file. Those will be covered in other test.
The next query should help show the files which are not supplementary files and their first link, for visual checks:

## No biomaterials are disconnected
#### Test description
This test returns any biomaterial nodes that have degree 0.
The ingest exporter is more likely to skip an entity all together rather than create one with no links. This test may apply to issues with the importer.

## Sequencing files are linked to appropriate protocols
#### Test description
The first process upstream of a sequencing file should have two links to protocols and those should be
'library_preparation_protocol' and 'sequencing_protocol'.

## File nodes terminate experimental design
#### Test description
Checks that file nodes have no outwards relationships.

## Sequence files link to cell suspension
#### Test description
The biomaterial linked to the process linked to a sequence file must be a cell suspension.
This next query should provide all the subgraphs in the form (file)-(process)-(biomaterial).

## Experimental design is acyclical
#### Test description
This test searches for directed cycles in the experimental design.

## Donors are not derived
#### Test description
Makes sure the indegree of donor_organism nodes when excluding INPUT_BIOMATERIALS type is 0. They should be the root
of the _experimental design_.

## Processes using smartseq2 library preparation protocols have 2 or 3 files linked
#### Test description
Processes using smartseq2 library preparation protocols have 2 or 3 files linked.

