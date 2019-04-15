__author__ = "hewgreen"
__license__ = "Apache 2.0"
__date__ = "4/04/2019"


class graphFeatures:
    def __init__(self, subid, graph):

        self.subid = subid
        self.graph = graph

        # per dataset attributes
        self.no_of_assays_in_dataset = self.no_of_assays()
        self.specific_node_types = self.get_specific_node_types_in_dataset()
        self.specific_node_counts = self.specific_node_counter()
        self.total_nodes = sum(self.specific_node_counts.values())
        self.total_no_of_edges = self.get_no_of_edges
        self.file_to_donor_lengths = self.get_file_to_donor_lengths() # use to diff assay
        self.longest_chain = self.get_longest_oneway_link()
        self.longest_backbone_paths = self.get_longest_backbone_paths()
        self.node_degrees = self.get_all_node_degs()
        self.end_graph_protocols = self.get_last_two_protocols()
        self.seq_files_per_assay = self.get_seq_files_per_assay()
        self.cyclical_nodes = self.get_cyclical_nodes()


    def no_of_assays(self): # return total number of assay processes aka bundles
        query = '''
                MATCH (p)
                WHERE (:files {submissionID: '%s'})-[:DERIVED_FROM]->(p:processes)
                RETURN count(p) AS no_assays
                '''
        query = query % (self.subid)
        result = self.graph.run(query)
        return next(result)['no_assays']

    def get_specific_node_types_in_dataset(self):
        query = '''
                MATCH (n)
                WHERE n.submissionID = '%s'
                RETURN DISTINCT n.specificType AS specific_node_types
                '''
        query = query % (self.subid)
        result = self.graph.run(query)
        specific_node_types = []
        while result.forward():
            specific_node_types.append(result.current['specific_node_types'])

        return specific_node_types

    def specific_node_counter(self): # return dict with counts of specific node types in dataset
        specific_node_counts = {}
        for specific_node_type in self.specific_node_types:
            query = '''
                    MATCH (n)
                    WHERE n.submissionID = '{0}' AND n.specificType = '{1}'
                    RETURN count(n) AS no_nodes
                    '''
            query = query.format(self.subid, specific_node_type)
            result = self.graph.run(query)
            count = next(result)['no_nodes']
            specific_node_counts[specific_node_type] = count
        return specific_node_counts

    def get_no_of_edges(self):
        query = '''
                MATCH p=(a)-[r:DERIVED_FROM]->(b)
                WHERE a.submissionID = '%s' AND b.submissionID = '%s'
                RETURN count(r) AS edge_count
                        '''
        query = query % (self.subid, self.subid)
        result = self.graph.run(query)
        return next(result)['edge_count']


    def get_file_to_donor_lengths(self):
        query = '''
            MATCH p=(a:files)-[:DERIVED_FROM*]->(b:biomaterials {specificType:"donor_organism"})
            WHERE a.submissionID = '%s' AND b.submissionID = '%s'
            RETURN length(p) AS length
            '''
        query = query % (self.subid, self.subid)
        result = self.graph.run(query)
        unpack = [x.get('length') for x in result.data()]
        return set(unpack)


    def get_longest_oneway_link(self): # if this query takes too long it may need further constraining
        query = '''
            MATCH p = (a) - [:DERIVED_FROM *]->(b)
            WHERE a.submissionID = '%s'
            AND b.submissionID = '%s'
            RETURN length(p) AS len, a.specificType AS from, b.specificType AS to
            ORDER BY length(p) DESC
            LIMIT 1
            '''
        query = query % (self.subid, self.subid)
        result = self.graph.run(query)
        return result.data()[0]

    def get_longest_backbone_paths(self): # uses DERIVED_FROM link only so does not return protocols
        query = '''
            MATCH p = (a) - [:DERIVED_FROM *]->(b)
            WHERE a.submissionID = '%s'
            AND b.submissionID = '%s'
            AND length(p) = %s
            RETURN a.specificType AS from,
            b.specificType AS to,
            length(p) AS length
            '''
        query = query % (self.subid, self.subid, self.longest_chain.get('len'))
        result = self.graph.run(query)
        return result.data()


    def get_all_node_degs(self):
        query = '''
        MATCH(a)
        WHERE a.submissionID = '%s'
        RETURN size((a) < --()) AS In_Degree,
        size((a) -->()) AS Out_Degree,
        a.specificType AS specificType,
        ID(a) AS id,
        a.schema_type AS schema_type
        '''
        query = query % (self.subid)
        result = self.graph.run(query)
        return result.data()

    def get_last_two_protocols(self):
        self.end_of_graph_data_file_types = {'sequence_file' : ['library_preparation_protocol', 'sequencing_protocol'],'image_file' : ['imaging_preparation_protocol', 'imaging_protocol']} # assumption may change
        self.ultimate_biomaterial_type_map_to_file = {'image_file' : ['imaged_specimen'], 'sequence_file' : ['cell_suspension']}

        query = '''
            MATCH (b:biomaterials)<-[:DERIVED_FROM]-(p:processes)<-[:DERIVED_FROM]-(f:files)
            WHERE b.submissionID = '{0}'
            AND p.submissionID = '{1}'
            AND f.submissionID = '{2}'
            AND f.specificType IN {3}
            WITH p, b, f
            MATCH (p)-[r]-(n)
            WHERE n.schema_type = 'protocol'
            RETURN n.specificType AS protocol_specific_type,
            b.specificType AS biomaterial_specific_type,
            f.specificType AS data_file_specific_type,
            size((p)-[:IMPLEMENTS]-()) AS no_final_protocols

        '''
        query = query.format(self.subid, self.subid, self.subid, str(list(self.end_of_graph_data_file_types.keys())))
        result = self.graph.run(query)
        return result.data()

    def get_seq_files_per_assay(self):
        query = '''
            MATCH(p: processes) < -[r: DERIVED_FROM]-(f:files)
            WHERE p.submissionID = '{0}'
            AND f.submissionID = '{1}'
            AND f.specificType = 'sequence_file'
            WITH(p)
            RETURN size((p) - [: DERIVED_FROM]-(:files)) AS no_seq_files
            '''
        query = query.format(self.subid, self.subid)
        result = self.graph.run(query)
        return result.data()

    def get_cyclical_nodes(self):
        query = '''
            MATCH p = (a)-[:DERIVED_FROM *]->(a)
            WHERE a.submissionID = '{0}'
            RETURN a
            '''
        query = query.format(self.subid)
        result = self.graph.run(query)
        return result.data()
