import os
import json
import dpath
from .json_helpers import load_json_from_file, json_cast_value, json_schme_path_generator


def cli_json_override_property(obj, schema, confirm_prompt=False):
    if confirm_prompt and not cli_confirm('Do you want to override a property?[y/n]: '):
            return
    props = set(list(obj.keys()) + schema.get('required', []))
    prop = cli_choose_option(props)
    obj = cli_json_schema_update_prop(prop, obj, schema)
    return obj

def cli_json_schema_update_prop(prop, obj, schema):
    value_type = schema['properties'][prop].get('type')
    while True:
        value = input('enter %s: ' % prop)
        if value: # TODO: Handle not required properties
            value = json_cast_value(value, value_type)
            if value == None:
                continue
            # TODO: Check other validations
            break
    obj[prop] = value
    return obj

def cli_confirm(msg):
    while True:
        answer = input(msg + '[y/n]: ')
        if answer == 'n':
            return False
        elif answer == 'y':
            return True

def cli_choose_option(options, msg=None):
    # TODO: Remove patch
    # PATCH for arrays
    list_flag = False
    if type(options[0]) == list:
        list_flag = True
        new_options = []
        for op in options:
            new_options.append(".".join(op))
        options = new_options
    if msg:
        print(msg)
    print('Options:')
    for option in options:
        print(option, end=', ')
    while True:
        choice = input('Choose an option: ')
        if choice in options:
            break
        print('Wrong choice')
    if list_flag:
        return choice.split(".")
    return choice

def cli_get_file_path(msg=None):
    if not msg:
        msg = 'enter file path: '
    while True:
        path = input(msg)
        if os.path.isfile(path):
            break
    return path

def cli_get_column(dataset, msg=None):
    if not msg:
        msg = 'Enter Column name'
    while True:
        print(10*"=")
        print('Columns:', dataset.columns)

        target_column = input(msg + ':  ')
        if target_column in dataset.columns:
            break
        else:
            print('Wrong answer!')
    return target_column

def cli_load_json_from_file():
    path = cli_get_file_path()
    return load_json_from_file(path)



def cli_json_get_value_by_type(type, msg=None):
    # TODO: Implement all types
    if not msg:
        msg = 'Enter %s value: ' % type
        
        while True:
            value = input(msg)
            try:
                if type == 'string':
                    pass
                elif type == 'integer':
                    value = int(value)
                elif type == 'number':
                    value = float(value)
                elif type == 'dict':
                    value = dict(json.loads(value))
                elif type == 'json':
                    value = json.loads(value)
                return value
            except ValueError:
                pass

def ask_json_value(instance, path, msg='Enter value for path', type=None):
    # TODO: path doesn't have a functionality here
    # TODO: instance doesn't have a functionality here
    
    # types = ["null[NOT-IMPLMENTED]", "boolean[NOT-IMPLEMENTED]", "object[NOT-IMPLEMENTED", "array[NOT-IMPLEMENTED]", "number", "integer", "string"]
    types = ["number", "integer", "string", "dict", "json"]
    print(msg)
    print('path: %s' % path)
    if not type:
        type = cli_choose_option(types, 'Choose a data type')
    return cli_json_get_value_by_type(type)
            
def cli_json_object_fix_errors(ob):
    while True:
        if ob.is_valid(): break
        error = next(ob.get_errors())
        
        for e in ob.get_errors():
            print(e.message)
        
        print(20*"=")
        print('FIX ERROR')
        print(20*"=")
        print('instance: ', ob.instance)
        #print('schema: ', ob._get_updated_schema(ob.instance, ob.schema))
        print('message: ',error.message)
        
        path = list(error.absolute_path)
        
        print('current path: %s' % path)
        #if cli_confirm('Append something to the path?'):
        extra_path = input('Enter extra path separated by ".": ')
        
        if extra_path != '':
            extra_path = int(extra_path)
            extra_path_array = []
            for p in extra_path.split('.'):
                if p.isnumeric(): # TODO: Ask if it's actually a number
                    extra_path_array.append(int(p))
                else:
                    extra_path_array.append(p)
            
            path = path + extra_path.split('.')
        
        value = ask_json_value(ob.instance, error.absolute_path, error.message)
        
        ob.set_value(path, value)
        

def cli_json_object_set_value(ob):
    tmp_path = input('Enter path separated by ".": ')
    path = tmp_path.split('.')
    value = ask_json_value(ob.instance, path)
    merge_policy = cli_choose_option(['replace', 'add', 'safe'], 'Chosse a merge poicy')
    ob.set_value(path, value, merge_policy)
    
def cli_json_get_value_by_schema(schema):
    print(20*"=")
    print("cli_json_get_value_by_schema")
    type = schema.get('type', 'string')
    
    while True:
        value = input('Enter value: ')
        try:
            value = json_cast_value(value, type)
            break
        except:
            pass
    return value

def cli_json_object_modify_instance(ob):
    while True:
        if not ob.is_valid():
            cli_json_object_fix_errors(ob)
    
        if not cli_confirm('ingresar valor?'):
            break
            
        paths = json_schme_path_generator(ob.get_updated_schema())
        instance_paths = []
        schema_paths = []
        for p in paths:
            instance_paths.append(p[0])
            schema_paths.append(p[1])
        path = cli_choose_option(instance_paths)
        path_index = instance_paths.index(path)
        schema_path = schema_paths[path_index]
        
        value = cli_json_get_value_by_schema(dpath.get(ob.schema, schema_path))
        
        merge_policy = 'replace'
        if type(value) in [list, dict]:
            merge_policy = cli_choose_option(['replace', 'add', 'safe'], msg='Choose merge policy')
        ob.set_value(path, value, merge_policy)
    
    