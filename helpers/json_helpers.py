import json

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
            return None
    return value

def json_get_errors(obj, schema):
    errors = {}
    # Check required
    required_props = schema.get('required', [])
    
    for rp in required_props:
        if not obj.get(rp):
            if rp not in errors.keys():
                errors[rp] = []
            errors[rp].append('This property is required.')
            
    return errors




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

