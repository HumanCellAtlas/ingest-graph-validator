#!/bin/bash
echo "Getting neo4j plugins..."
wget https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/3.5.0.7/apoc-3.5.0.7-all.jar -q --show-progress
wget https://s3-eu-west-1.amazonaws.com/com.neo4j.graphalgorithms.dist/neo4j-graph-algorithms-3.5.14.0-standalone.zip -q show-progress
unzip neo4j-graph-algorithms-3.5.14.0-standalone.zip
delete neo4j-graph-algorithms-3.5.14.0-standalone.zip
echo "plugins are ready"
