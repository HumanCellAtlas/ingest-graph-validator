
def unpack_ignore_lists(in_dict): # Neo4J cannot take lists or dicts so they are unpacked or stringed

    def dict_loop(in_dict):

        # type rules for unpacking

        neo4j_safe = (str, int, float)
        neo4j_notsafe = (list)
        unpack = (dict)

        out_dict = {}
        for key, value in in_dict.items():
            if isinstance(value, unpack):
                for nested_key, nested_value in value.items():
                    new_key = key + '.' + nested_key
                    out_dict[new_key] = nested_value
            elif isinstance(value, neo4j_safe):
                out_dict[key] = value
            elif isinstance(value, neo4j_notsafe):
                out_dict[key] = str(value)
            else:
                print('WARNING: not caught data type while unpacking.')
        return out_dict

    out_dict = dict_loop(in_dict)
    type_list = [type(x) for x in out_dict.values()]
    if dict in type_list:
        out_dict = dict_loop(out_dict)
    elif list in type_list:
        out_dict = dict_loop(out_dict)

    return out_dict

