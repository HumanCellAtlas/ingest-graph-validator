## Graph validation suite

**In development.**

These high level assumptions are vunerable to breaking as HCA datasets diversify. Nevertheless, wranglers should be aware of these breaking assumptions as they happen. This graph validation suite aims to warn wranglers or users about uncharacteristic patterns rather than block ingestion. Assumptions are easy to add, edit or remove by wranglers as required.

Requires you to be running Neo4J _Graph("bolt://localhost:11005", user="neo4j", password="neo5j"_. You can change these settings in graph_import/subid2neo.py.


### graph_import/

**Please see example code in 'example_build_graph.py'**


These modules are for loading nodes and edges into Neo4J.

**subid2neo** allows you to load a graph using a submission ID. Once a submission has been submitted to ingest the ID can be used to query ingest via the API using HAL links. This is currently quite slow so the method allows you to send multiple requests at once using multithreading. Provide a thread number to increase the speed.

Ingest hits a connection error for submissions with lots of bundles. This issue has been reported to ingest. Number of threads is not the limit but total number of requests seems to be the problem. Even with 2 threads large datasets cannot be downloaded.

**sheet2neo** will use the ingest importer to convert a stand alone spreadsheet into JSON which will then be loaded into Neo4J. By avoiding crawling ingest API this can be used to ingest larger datasets although this still takes time. This script has not yet been optimised for speed but scales to all datasets we have (alough it has not been tested on TM).

### graph_validate/

**Please see example code in 'example_tests.py'**

To make a new test create another '_violation.adoc' in this directory. Tests are written in cypher and you should use the template when you make new tests. They must be written as violations and return nothing if they pass. See the tests that are already being ran in this directory.

### graph_report/

**Please see example code in 'example_build_graph.py'**

There is only limited viewing capability at the moment. graphReports is generic and able to run various cypher based report queries. At the moment there is one example. Given a submission ID, the function get_unique_assays uses 'assay_diff_report.adoc' to return list of assay process uuids with unique graph structures. For example, if a submission contains assays with two different structures (maybe one is missing a protocol node) it will return two uuids.

These uuids can then be fed to the assayPlot function (as shown in 'example_build_graph.py') to return cypher queries for you to use in the Neo4J browser. 

Eventually it would be great if we could implement something like this https://github.com/Nhogs/popoto/wiki/Getting-started.
### Some cypher examples:

Check if a required field is on all the nodes it should be:
```
MATCH (n {submissionID:'5c2dfb101603f500078b28de'})
WHERE n.specificType = 'donor_organism' and NOT EXISTS(n.genus_species)
RETURN count(n)
```

