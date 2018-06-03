import json
import copy
import dpath
from IPython.core.debugger import Pdb

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
    elif value_type in ['array', 'object']:
        value = json.loads(value)
    
    return value

from IPython.core.debugger import Pdb
def deprecated_json_find_items_by_key_generator(json_input, lookup_key, path=[], skip_keys=[]):
    print('json_find_items_by_key_generator')
    print('json_input: ', json_input)
    print('path: ', path)
    
    #if lookup_key == 'if':
    Pdb().set_trace()
    
    #json_input = copy.deepcopy(json_input)
    if isinstance(json_input, dict):
        
        index = 0
        for k, v in json_input.items():
            if k == lookup_key and k not in skip_keys:
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

def json_pop_nested_item(instance, path=[]):
    if len(path) == 0:
        return instance
    if len(path) == 1:
        instance.pop(path[0])
    else:
        item = instance
        for k in path[:-1]:
            item = item.get(k)
        item.pop(path[-1])
    return instance


def json_set_nested_value(instance, path, value):
    """
    It works with nested unexistent arrays.
    it fails if something is preciously set where an array should be
    """
    x = copy.deepcopy(instance)
    tp = []
    
    for idx, p in enumerate(path[:-1]):
        tp.append(p)
        try:
            dpath.get(x, tp)
            continue
        except KeyError:
            next_p =  path[idx + 1]
            if type(next_p) == int:
                dpath.new(x, tp, [])
            else:
                dpath.new(x, tp, {})
    
    old_x = copy.deepcopy(x)
    #Pdb().set_trace()
    
    try:
        dpath.get(x, path)
        
        if path:
            sx = dpath.get(x, path)
            dpath.merge(sx, value)
            dpath.set(x, path, sx)
        else:
            dpath.merge(x, value)
    except:
        if path:
        
            dpath.new(x, path, value)
        else:
            dpath.merge(x, value)
    """
    try:
        dpath.new(x, path, value)
    except Exception as e:
        print(e)
        #Pdb().set_trace()
        if path:
            sx = dpath.get(x, path)
            dpath.merge(sx, value)
            #dpath.set(x, path, sx)
        else:
            sx = x
        dpath.merge(sx, value)
        x =sx
       """
            
    
    return x
        
        
        
        