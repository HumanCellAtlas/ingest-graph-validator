from pprint import pprint

"""
Neo4J cannot take lists or dictionaries. In order to be used, json schemas ("content" in EntityMap object) need to be flattened.

@:param[in] in_dict     Dictionary whose values are going to be unpacked
@:param[in] out_dict    Used for recursivity if there is a dictionary as a value to unpack
@:param[in] nested_key  Used for recursivity. Key represents fully qualified key (e.g. project.title.description)

@:returns   out_dict    Dictionary with unpacked values
"""
def unpack_dictionary(in_dict, out_dict={}, nested_key = ""):
    for key, value in in_dict.items():
        if isinstance(value, dict):
            out_dict = unpack_dictionary(value, out_dict, "{}{}{}".format(nested_key, "." if nested_key else "", key))
        elif isinstance(value, list):
            if isinstance(value[0], dict):
                for dictionary in value:
                    out_dict = unpack_dictionary(dictionary, out_dict, "{}{}{}".format(nested_key, "." if nested_key else "", key))
            else:
                out_dict["{}{}{}".format(nested_key, "." if nested_key else "", key)] = str(value)
        else:
            out_dict[nested_key + ("." if nested_key else "") + key] = value
    #pprint(out_dict)
    return out_dict

def unpack_ignore_lists(in_dict): # Neo4J cannot take lists or dicts so they are unpacked or stringed

    def dict_loop(in_dict):

        # type rules for unpacking

        neo4j_safe = (str, int, float)
        neo4j_notsafe = list
        unpack = dict

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
