__author__ = "hewgreen"
__license__ = "Apache 2.0"
__date__ = "4/04/2019"


class graphTests:
    def __init__(self, features): # testcase granularity is 1 submission

        # print(features.__dict__.keys())
        self.features = features

        self.test_results = {
            'Donor biomaterial node is the uppermost node on the graph.' : self.test_graph_starts_with_biomaterial_node(),
            'sequence_file node or image_file node at the end of the graph' : self.test_graph_ends_with_data_file(),
            'There are no detached biomaterials' : self.test_graph_has_no_detached_biomaterial_nodes(),
            'Last two protocols are correct' : self.test_last_two_protocol_types(),
            'Ultimate biomaterials are correct' : self.last_biomaterial_node_is_appropreate(),
            'Max number of sequencing files per assay is 3' : self.seq_file_max_3_per_assay(),
            'Minimum backbone path length per assay is 5' : self.min_assay_backbone_path_is_5(),
            'Backbone is acyclical' : self.test_backbone_is_acyclical()
        }

    def test_graph_starts_with_biomaterial_node(self):
        for node in self.features.node_degrees:
            if node.get('specificType') == 'donor_organism':
                indeg = node.get('In_Degree')
                outdeg = node.get('Out_Degree')
                if (outdeg != 0) or (indeg > 1):
                    return False
        if self.features.longest_chain.get('to') != 'donor_organism':
            return False

        return True

    def test_graph_ends_with_data_file(self):
        links = self.features.longest_backbone_paths
        data_files = ['sequence_file', 'image_file']
        for node in links:
            if (node.get('from') not in data_files):
                return False
        for node in self.features.node_degrees:
            if node.get('specificType') in data_files:
                indeg = node.get('In_Degree')
                outdeg = node.get('Out_Degree')
                if (indeg != 0) or (outdeg > 1):
                    return False
        return True

    def test_graph_has_no_detached_biomaterial_nodes(self):
        test = True
        for node in self.features.node_degrees:
            if node.get('schema_type') == 'biomaterial' and (node.get('In_Degree') == 0 and node.get('Out_Degree') == 0):
                print('Detached biomaterial detected {}'.format(str(node)))
                test = False
        return test

    def test_last_two_protocol_types(self):
        end_of_graph_data_file_types = self.features.end_of_graph_data_file_types

        for match in self.features.end_graph_protocols:
            if match.get('no_final_protocols') != 2:
                return False
            end_file_type = match.get('data_file_specific_type')
            valid_protocols = end_of_graph_data_file_types.get(end_file_type)
            if match.get('protocol_specific_type') not in valid_protocols:
                return False
        return True

    def last_biomaterial_node_is_appropreate(self):
        ultimate_biomaterial_type_map_to_file = self.features.ultimate_biomaterial_type_map_to_file
        for match in self.features.end_graph_protocols:
            data_file_specific_type = match.get('data_file_specific_type')
            if match.get('biomaterial_specific_type') not in ultimate_biomaterial_type_map_to_file.get(data_file_specific_type):
                return False
        return True

    def seq_file_max_3_per_assay(self):
        for count in self.features.seq_files_per_assay:
            if count.get('no_seq_files') > 3:
                return False
        return True

    def min_assay_backbone_path_is_5(self):
        for long_path in self.features.longest_backbone_paths:
            if long_path.get('length') < 5:
                return False
        return True

    def test_backbone_is_acyclical(self):
        if self.features.cyclical_nodes:
            return False
        else:
            return True


