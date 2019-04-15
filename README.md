## Graph validation suite

**In development.**

**Note that these graph tests are not schema aware because the tested assumptions are not declared in the schema. Therefore, they are vunerable to breaking as HCA datasets diversify. Nevertheless, wranglers should be aware of these breaking assumptions as they happen. This graph validation suite aims to warn wranglers or users about uncharacteristic patterns rather than block ingestion. We have tried to make well described conservative assumptions.**

Requires you to be running Neo4J _Graph("bolt://localhost:11005", user="neo4j", password="neo5j"_. You can change these settings in graph_import/subid2neo.py.


### graph_import/

These modules are for loading nodes and edges into Neo4J.

**subid2neo** allows you to load a graph using a submission ID. Once a submission has been submitted to ingest the ID can be used to query ingest via the API using HAL links. This is currently quite slow so the method allows you to send multiple requests at once using multithreading. Provide a thread number to increase the speed.

Ingest hits a connection error for submissions with lots of bundles. This issue has been reported to ingest. Number of threads is not the limit but total number of requests seems to be the problem. Even with 2 threads large datasets cannot be downloaded.

**sheet2neo** has not been started yet. This function will use the ingest importer to convert a stand alone preadsheet into JSON which will then be loaded into Neo4J. This should be faster but not as useful for integration of this validator into ingest.

### graph_validation/

#### graphfeatures.py
graphfeatures.py calculates graph features of a submission graph. These features are later used to test assumptions. As new tests are added graph features used to power these queries should be added to this class.

#### graphtests.py

Graph [assumptions](https://github.com/HumanCellAtlas/hca-data-wrangling/blob/master/docs/Graph_assumptions.md) and [usecases](https://github.com/HumanCellAtlas/hca-data-wrangling/blob/master/docs/20181211_graph_use_cases.md) were previously captured on a per assay basis. This validator now operates over the whole submission graph and therefore implementation details differ. Assumptions are detailed below to ensurecode can evole as biological assumptions change.

##### TEST Donor biomaterial node is the uppermost node on the graph.
1. Out degrees of donor should be 0 because a donor is not derived from anything.
1. All graphs should have a donor entity.
1. All files should be ultimately derived from a donor.
1. Donor nodes in degrees should be greater than 1. Donor nodes should never be floating. 

In the future we may want to add an exception to allow a donor to be derived from another donor (via a process node).


##### TEST sequence_file node or image_file node should be at the end of the graph
1. In degrees of sequencing_file and imaging_file should be 0.
1. The end of the longest paths should be a sequencing_file or imaging_file (ignoring protocols).

In the future we may want to allow files to be inputs to processes to capture synthetic biology but we have not encoutered this requirement yet.

##### TEST Graph should have no hanging biomaterial nodes
1. Test all biomaterial nodes for at least 1 degree

##### TEST Last process has two protocols type specified by downstream and upstream nodes
1. Ultimate process should always have 2 protocols
1. These protocols should be library_preparation_protocol and sequencing if the last file is a sequencing_file
1. These protocols should be imaging_preparation_protocol or imaging_protocol 

To change these assumptions update this line:

`self.end_of_graph_data_file_types = {'sequence_file' : ['library_preparation_protocol', 'sequencing_protocol'],'image_file' : ['imaging_preparation_protocol', 'imaging_protocol']}`

##### TEST The last biomaterial is appropreate and corresponds to the ultimate file type
1. If the last filetype is image_file the ultimate biomaterial should be imaged_specimen.
1. If the las filetype is sequence_file the ultimate biomaterial should be cell_suspension.
To change these assumptions update this line:
`self.ultimate_biomaterial_type_map_to_file = {'image_file' : ['imaged_specimen'], 'sequence_file' : ['cell_suspension']}`


##### TEST There can only be 1, 2, or 3 sequencing file nodes in the graph
1. no more than 3 sequencing_file type nodes should every be connected to a process. 

##### TEST Minimum path length per assay is 5
1. Number of edges connecting the final data file and the donor should be minimum 5 (NB process nodes are included so there are two jumps per entity.)

##### TEST Backbone of graph is acyclical.
1. The same node should not be encountered downstream of itself.

This test does not fail if protocols are implemented by multiple processes in an assay backbone's chain.


## Mising Tests

There are many conditional validation tests that  can be added. For example, species conformity. These assumptions need to be defined before implementation.
