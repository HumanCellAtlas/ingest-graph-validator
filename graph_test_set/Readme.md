# Tests directory
In this folder you will find the tests the Human Cell Atlas uses for validating entities in their experiments

## How to run the tests
In order to run the tests in this directory, you just have to follow these steps:
1. Install `ingest-graph-validator` with `pip` (As indicated in the [main page](https://github.com/HumanCellAtlas/ingest-graph-validator#install_pypi))
1. In a shell, run:
```
ingest-graph-validator init
ingest-graph-validator hydrate ingest <ingest_uuid>
ingest-graph-validator action test <path_to_tests>
```

## How to add new tests
To create new tests, please follow this guide:

1. Open an issue with the template `Test addition`, filling in all the fields (When possible)
1. If you don't know how to create/modify cypher queries or create pull requests (PR) in GitHub, please wait for the admins of the repository to create a PR for you and skip to step x.
1. Create a new branch and copy the contents of `graph_test_set/template.txt` into a new document inside the same folder. The newly created rule should be evident in the filename (e.g. `file_have_links.adoc`)
1. Fill in the template. The test is a Cypher query which should try to identify when a dataset is not following the rule. For example:
```
File: 10x_has_more_than_2_files.adoc
---
MATCH (r:library_preparation_protocol)<-[:PROTOCOLS]-(p:process)<-[d]-(f:file)
WITH r, p, COUNT(d) as num_files
WHERE r.`library_construction_method.ontology_label` =~ "10[xX] ([35]' ){0,1}v[1-3] sequencing" // 10x v2 and v3
AND NOT 2 <= num_files <= 4 // Number of files is more than 1 and less than 5
RETURN num_files
---
```
Will identify those 10x experiments in which the `num_files` is not in between 2 and 4 (Both included).
 
5. Commit your changes and push into your branch.
1. Create a PR indicating:
   - Title: `<Short description of issue>.Fixes #<Issue number>`
   - Name of the new file created
   - Description of the test
1. If the creator of the PR is an admin of the repository, please ping the creator of the ticket to confirm this is the issue they want to tackle.
If the person who created the PR is the same one as the person who created the ticket, wait for the administrators to review the PR.
1. The PR should be reviewed within 3-4 working days, and the last person to review the PR should merge it to master.
