import os
import json
from .json_helpers import load_json_from_file, json_cast_value
"""
def cli_json_print_errors(obj, schema):
    errors = json_get_errors(obj, schema)
    if errors:
        print('You have to correct this errors:')
        for prop in errors.keys():
            for error in errors[prop]:
                print('%s: %s' % (prop, error))
"""
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

def cli_get_integer(default=None, min=0, max=10, msg='Enter degree', *args, **kwargs):
    while True:
        value = input('{msg}(min:{min}, max:{max}, default:{default}: '.format(msg=msg, min=min, max=max, default=default))
        if value == '' and default:
            value = default
        try:
            int_value = int(value)
            if int_value >= min and int_value <= max:
                break
        except ValueError:
            print(ValueError)
            pass
    return int_value

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
        error = ob.get_errors()[0]
        
        print(10*"=")
        print(error.instance)
        print(error.message)
        
        path = list(error.absolute_path)
        
        print('current path: %s' % path)
        #if cli_confirm('Append something to the path?'):
        extra_path = input('Enter extra path separated by ".": ')
        path = path + extra_path.split('.')
        
        value = ask_json_value(ob.instance, error.absolute_path, error.message)
        
        print(error.set_path, value)
        
        ob.set_value(path, value)
        

def cli_json_object_set_value(ob):
    tmp_path = input('Enter path separated by ".": ')
    path = tmp_path.split('.')
    value = ask_json_value(ob.instance, path)
    ob.set_value(path, value)
    
        