from helpers.cli_helpers import cli_json_override_property, cli_load_json_from_file, cli_json_print_errors, cli_choose_option, cli_json_get_value_by_type, cli_json_object_fix_errors

from helpers.json_helpers import load_json_from_file, json_find_items_by_key_generator
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
        special_keys = ['dependencies', 'anyOf', 'oneOf', 'allOf']
        pre_path = []
        if ns['type'] == 'array':
            pre_path.append('items')
        
        for sp_key in special_keys:
            path = pre_path + [sp_key]
            try:
                sp_value = dpath.get(ns, path)
            except KeyError:
                sp_value = None
            if sp_value:
                print('path', path)
                print('sp_value', sp_value)
                for dk in sp_value.keys():
                    d = sp_value[dk]
                    if 'if' in d.keys():
                        sub_schema = d.get('if')
                        v = Draft6Validator(sub_schema)
                        if v.is_valid(instance):
                            sp_value[dk] = d.get('then')
                        elif d.get('else'):
                            sp_value[dk] = d.get('else')
                dpath.set(ns, pre_path)
                ns[path] = sp_value
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
        

    def is_valid(self):
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
        
        #current_schema = self._get_updated_schema(self.instance, self.schema)
        print(10*"-")
        print('final current schema')
        print(current_schema)
        v = Draft6Validator(current_schema)
        if not v.is_valid(self.instance):
            return False
        return True
            

schema = load_json_from_file('tmp.schema.json')
instance = load_json_from_file('tmp.json')

ob = JsonObject(schema, instance)
ob.is_valid()
#cli_json_object_fix_errors(ob)

# conds = json_find_items_by_key_generator(schema, 'if')
#next(conds)
