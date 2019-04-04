## Graph validation suite

In development.

Requires you to be running Neo4J _Graph("bolt://localhost:11005", user="neo4j", password="neo5j"_. You can change these settings in graph_import/subid2neo.py.


### graph_import

These modules are for loading nodes and edges into Neo4J.

**subid2neo** allows you to load a graph using a submission ID. Once a submission has been submitted to ingest the ID can be used to query ingest via the API using HAL links. This is currently quite slow so the method allows you to send multiple requests at once using multithreading. Provide a thread number to increase the speed.

Ingest hits a connection error for submissions with lots of bundles. This issue has been reported to ingest. Number of threads is not the limit but total number of requests seems to be the problem. Even with 2 threads large datasets cannot be downloaded.

**sheet2neo** has not been started yet. This function will use the ingest importer to convert a stand alone preadsheet into JSON which will then be loaded into Neo4J. This should be faster but not as useful for integration of this validator into ingest.

### graph_validation

Loads a one submission subgraph identified using the submission ID.

Checks the following:

