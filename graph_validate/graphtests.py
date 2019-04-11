__author__ = "hewgreen"
__license__ = "Apache 2.0"
__date__ = "4/04/2019"


from py2neo import Graph


GRAPH = Graph("bolt://localhost:11005", user="neo4j", password="neo5j")

class graphTests:
    def __init__(self, features):

        self.features = features


    





#
#
# ## Graph assumptions (if fail, throw a warning)
#
# 1. Every graph starts from donor biomaterial node.
# 1. Every graph should end with a file node.
# 1. Graph should have no hanging biomaterial nodes.
# 1. The ultimate process node should have 2 protocols (library preparation and sequencing or imaging preparation and imaging).
# 1. Cell suspension or imaged specimen is the last biomaterial node.
# 1. There can only be 1, 2, or 3 sequencing file nodes in the graph. (10x should have 2 or 3, and SS2 should have 1 or 2, but this is schema-aware.)
# 1. The minimal longest path length of the graph should be 5 (sequencing or imaging).
#
# ## Other sanity checks
#
# 1. Graph has a direction from biomaterial node to file node and cannot have cycle (is directional acyclical).
# 1. Graph can have more than one first biomaterial (biomaterial with indegree 0).
# 1. Every non-process node should touch at least one process node. **This would be a result of a problem in ingest.**
# 1. All entities in submission should appear in at least 1 graph (except project (and supplemental files, for now); check in ingest?)



# if donor to file isnt the longest link (all forward) throw an error

# use self.file_to_donor_lengths to check all are greater than 5 in future may have to specfify data files only this is an indicator of multi bundle presence
# check that longest chain if file to donor type with longest_chain
# also use it to check length is the right one vs other list

