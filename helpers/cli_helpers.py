import os
from .json_helpers import load_json_from_file, json_cast_value, json_get_errors

def cli_json_print_errors(obj, schema):
    errors = json_get_errors(obj, schema)
    if errors:
        print('You have to correct this errors:')
        for prop in errors.keys():
            for error in errors[prop]:
                print('%s: %s' % (prop, error))

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
        answer = input(msg)
        if answer == 'n':
            return False
        elif answer == 'y':
            return True

def cli_choose_option(options, msg=None):
    if msg:
        print(msg)
    print('Options:')
    for option in options:
        print(option)
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
            pass
    return int_value

def cli_load_json_from_file():
    path = cli_get_file_path()
    return load_json_from_file(path)