from helpers.cli_helpers import cli_json_override_property, cli_load_json_from_file, cli_json_print_errors, cli_choose_option, cli_json_get_value_by_type

from helpers.json_helpers import load_json_from_file
from jsonschema import validate, Draft3Validator, Draft4Validator, Draft6Validator, FormatChecker, ErrorTree
import copy
import dpath

class JsonObject():
        
    def __init__(self, schema, instance={}):
       # self.init(schema, instance)
        self.schema = copy.deepcopy(schema)
        self.instance = copy.deepcopy(instance)
    
    def _convertDraft7to6(self, instance, shema):
        ns = copy.deepcopy(schema)
        dependencies = ns.get('dependencies', {})
        if dependencies:
            for dk in dependencies.keys():
                d = dependencies[dk]
                if 'if' in d.keys():
                    sub_schema = d.get('if')
                    v = Draft6Validator(sub_schema)
                    if v.is_valid(instance):
                        dependencies[dk] = d.get('then')
                    elif d.get('else'):
                        dependencies[dk] = d.get('else')
                            
            ns['dependencies'] = dependencies
        return ns
        
    def _get_updated_schema(self, instance, schema):
        current_schema = copy.deepcopy(schema)
        
        while True:
            v = Draft6Validator(current_schema)
            if not v.is_valid(instance):
                return current_schema
            temp_schema = self._convertDraft7to6(self.instance, current_schema)
            if temp_schema != current_schema:
                current_schema = temp_schema
            else:
                break
        return current_schema
    
    def is_valid(self):
        current_schema = self._get_updated_schema(self.instance, self.schema)
        v = Draft6Validator(current_schema)
        if not v.is_valid(self.instance):
            return False
        return True
            
    def get_errors_orig(self):
        current_schema = self._get_updated_schema(self.instance, self.schema)
        v = Draft6Validator(current_schema)
        return v.iter_errors(self.instance)
        # errors = sorted(v.iter_errors(instance), key=lambda e: e.path)
        # for error in errors:
        #     print(error.message)
        
    def get_errors(self):
        current_schema = self._get_updated_schema(self.instance, self.schema)
        v = Draft6Validator(current_schema)
        
        errors = []
        for error in v.iter_errors(self.instance):
            error.set_path = list(copy.deepcopy(error.absolute_path))
            if error.validator == 'required':
                error.set_path = error.set_path + error.validator_value
            
            errors.append(error)
        
        return errors
        
    
    def set_value(self, path, value):
        pass
        

schema2 = load_json_from_file('if-exists-and-condiftion.schema.json')
instance = {
        "x": "v",
        "v": "v",
        "l": {"l1": "ss", "l4": 3, "l32": "sd"},
        "l3": "l3_base"
        }

#schema = copy.deepcopy(schema2)
schema = schema2

error_attrs = ['validator', 'validator_value', 'absolute_path', 'set_path']


def ask_json_value(instance, path, msg='Enter value for path', type=None):
    types = ["null[NOT-IMPLMENTED]", "boolean[NOT-IMPLEMENTED]", "object[NOT-IMPLEMENTED", "array[NOT-IMPLEMENTED]", "number", "integer", "string"]
    print(msg)
    print('path: %s' % path)
    if not type:
        type = cli_choose_option(types, 'Choose a data type')
    return cli_json_get_value_by_type(type)


ob = JsonObject(schema, instance)
last_error = None

while True:
    if ob.is_valid(): break
    
    errors = ob.get_errors()
    for error in errors:
        print(10*"=")
        #for e_attr in error_attrs:
        #    print('%s: %s' % (e_attr, getattr(error, e_attr)))
        value = ask_json_value(ob.instance, error.set_path, error.message)
        new_sub_instance = dict()
        dpath.util.new(new_sub_instance, list(error.set_path), value)
        dpath.util.merge(ob.instance, new_sub_instance)
