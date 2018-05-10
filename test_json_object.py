from helpers.cli_helpers import cli_json_override_property, cli_load_json_from_file, cli_json_print_errors
from helpers.json_helpers import load_json_from_file
from jsonschema import validate, Draft3Validator, Draft4Validator, Draft6Validator, FormatChecker, ErrorTree
import copy

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
            
    def get_errors(self):
        current_schema = self._get_updated_schema(self.instance, self.schema)
        v = Draft6Validator(current_schema)
        return v.iter_errors(self.instance)
        # errors = sorted(v.iter_errors(instance), key=lambda e: e.path)
        # for error in errors:
        #     print(error.message)

schema2 = load_json_from_file('if-exists-and-condiftion.schema.json')
instance = {"x": "v"}

#schema = copy.deepcopy(schema2)
schema = schema2

ob = JsonObject(schema, instance)
if not ob.is_valid():
    errors = sorted(ob.get_errors(), key=lambda e: e.path)
    for error in errors:
        print(error.message)
