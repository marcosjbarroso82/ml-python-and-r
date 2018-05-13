from helpers.cli_helpers import cli_json_object_fix_errors
from helpers.json_helpers import load_json_from_file, json_find_items_by_key_generator
from jsonschema import Draft6Validator
import copy
import dpath


class JsonObject():
        
    def __init__(self, schema, instance={}):
        self.schema = copy.deepcopy(schema)
        self.instance = copy.deepcopy(instance)
        
    def _get_updated_schema(self, instance, schema):
        current_schema = copy.deepcopy(schema)
        for sub_schema_cond, _, sub_schema_path in json_find_items_by_key_generator(schema, 'if'):
            v_sub = Draft6Validator(sub_schema_cond)
            repl_path = sub_schema_path[:-1]
            if v_sub.is_valid(self.instance):
                then_path = sub_schema_path[:-1] + ['then']
                sub_schema = dpath.get(current_schema, then_path)
            else:
                try:
                    else_path = sub_schema_path[:-1] + ['else']
                    sub_schema = dpath.get(current_schema, else_path)
                except KeyError:
                    sub_schema = dict()
            dpath.set(current_schema, repl_path, sub_schema)
        return current_schema
    
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
    
    def set_single_value(self, path, value):
        #new_sub_instance = dict()
        # dpath.util.new(new_sub_instance, path, value)
        # dpath.util.merge(self.instance, new_sub_instance)
        dpath.util.new(self.instance, path, value)
        
    def is_valid(self):
        current_schema = self._get_updated_schema(self.instance, self.schema)
        v = Draft6Validator(current_schema)
        return v.is_valid(self.instance)
            

schema = load_json_from_file('if-exists-and-condiftion.schema.json')
instance = load_json_from_file('if-exists-and-condiftion.json')

ob = JsonObject(schema, instance)
ob.is_valid()
cli_json_object_fix_errors(ob)
#e = ob.get_errors()[0]

# conds = json_find_items_by_key_generator(schema, 'if')
#next(conds)
