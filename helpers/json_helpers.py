import json
import copy
def load_json_from_file(path):
    with open(path, 'r') as file:
        obj = json.loads(file.read())
    return obj

def json_cast_value(value, value_type):
    # TODO: Implement all types
    if value_type == 'integer':
        try:
            value = int(value)
        except ValueError:
            raise
    return value

def json_find_items_by_key_generator(json_input, lookup_key, path=[]):
    if isinstance(json_input, dict):
        index = 0
        for k, v in json_input.items():
            if k == lookup_key:
                path = path + [k]
                yield v, k, path
            else:
                tmp_path = path + [k]
                yield from json_find_items_by_key_generator(v, lookup_key, tmp_path)
            index += 1
    elif isinstance(json_input, list):
        index = 0
        for item in json_input:
            path = path + [index]
            yield from json_find_items_by_key_generator(item, lookup_key, path)



def json_schme_path_generator(ob, path=[], schema_path=[]):
    print(20*"=")
    print(ob)
    
    path = copy.deepcopy(path)
    schema_path = copy.deepcopy(schema_path)
    
    if ob.get('type') == 'object':
        schema_path.append('properties')
        yield from json_schme_path_generator(ob.get('properties', {}), path=path, schema_path=schema_path)
    elif ob.get('type') == 'list':
        schema_path.append('items')
        schema_path.append('properties')
        yield from json_schme_path_generator(ob['items'].get('properties', {}), path=path, schema_path=schema_path)
    else:
        for key, value in ob.items():
            if value.get('type') in ['list', 'object']:
                yield from json_schme_path_generator(value, path=path+[key], schema_path=schema_path + [key])
            else:
                yield (path + [key], schema_path + [key])
