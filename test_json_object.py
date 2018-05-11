from helpers.cli_helpers import cli_json_override_property, cli_load_json_from_file, cli_json_print_errors, cli_choose_option, cli_json_get_value_by_type, cli_json_object_fix_errors

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
        new_sub_instance = dict()
        dpath.util.new(new_sub_instance, path, value)
        dpath.util.merge(self.instance, new_sub_instance)
        

schema = load_json_from_file('if-exists-and-condiftion.schema.json')
instance = {
        "x": "v",
        "v": "v",
        "l": {"l1": "ss", "l4": "3", "l32": "sd"},
        "l3": "l3_base"
        }


ob = JsonObject(schema, instance)

cli_json_object_fix_errors(ob)