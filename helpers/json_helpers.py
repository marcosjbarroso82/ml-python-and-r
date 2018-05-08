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

