from .cli_helpers import cli_json_object_fix_errors, cli_confirm, cli_json_object_set_value
from .json_helpers import load_json_from_file, json_find_items_by_key_generator, json_pop_nested_item
from jsonschema import Draft6Validator
import copy
import dpath
from urllib.request import urlopen
import json

from dpath.util import MERGE_REPLACE, MERGE_ADDITIVE, MERGE_TYPESAFE

from .constants import SCHEMA_RESERVED_WORDS

MERGE_POLICIES = {
        'replace': MERGE_REPLACE,
        'add': MERGE_ADDITIVE,
        'safe': MERGE_TYPESAFE
        }


class JsonObject():
        
    def __init__(self, schema, instance={}):
        self.schema = copy.deepcopy(schema)
        self.instance = copy.deepcopy(instance)
        
    def get_updated_schema(self, schema=None):
        if schema == None:
            schema = copy.deepcopy(self.schema)
        modified_flag = False
        
        current_schema = copy.deepcopy(schema)
        try:
            ref_value, _, ref_path = next(json_find_items_by_key_generator(schema, '$ref'))
            ref = urlopen("file:app_json/ds_preprocess_step.schema.json")
            ref_content = json.loads(ref.file.read())
            ref.file.close()
            ref.close()
            # remove $ref
            json_pop_nested_item(current_schema, ref_path)
            
            print('ref_content: ', ref_content)
            print('ref_path: ', ref_path)
            
            # instert referenced schema
            tmp_instance = dict()
            dpath.new(tmp_instance, ref_path[:-1], ref_content)
            dpath.merge(schema, tmp_instance)
            modified_flag = True
            print('REF MODIFIED', 10*"*")
        except StopIteration:
            pass
    
        try:
            sub_schema_cond, _, sub_schema_path = next(json_find_items_by_key_generator(schema, 'if'))
            v_sub = Draft6Validator(sub_schema_cond)
            
            path = [x for x in sub_schema_path if x not in SCHEMA_RESERVED_WORDS]
            repl_path = sub_schema_path[:-1]
            try:
                sub_instance = dpath.get(self.instance, path)                
                if v_sub.is_valid(sub_instance):
                    then_path = sub_schema_path[:-1] + ['then']
                    sub_schema = dpath.get(current_schema, then_path)
                else:
                    try:
                        else_path = sub_schema_path[:-1] + ['else']
                        sub_schema = dpath.get(current_schema, else_path)
                    except KeyError:
                        sub_schema = dict()
            except KeyError:
                sub_schema = dict()
            dpath.set(current_schema, repl_path, sub_schema)
            modified_flag = True
            print('REF MODIFIED', 10*"*")
        except StopIteration:
            pass
        if modified_flag:
            return self.get_updated_schema(current_schema)
        current_schema.pop('definitions')
        return current_schema
    
    def get_errors(self):
        current_schema = self.get_updated_schema()
        v = Draft6Validator(current_schema)
        return v.iter_errors(self.instance)
        """
            errors = []
            for error in v.iter_errors(self.instance):
                error.set_path = list(copy.deepcopy(error.absolute_path))
                if error.validator == 'required':
                    error.set_path = error.set_path + error.validator_value
                errors.append(error)
            return errors
        """
    def set_value(self, path, value, merge_policy='replace'):
        merge_flags = MERGE_POLICIES.get(merge_policy)
        tmp_instance = copy.deepcopy(self.instance)
        tmp_path = []
        for p in path:
            print(tmp_path)
            print(tmp_instance)
            try:
                dpath.get(tmp_instance, tmp_path)
            except KeyError:
                if type(p) == int:
                    print('create array')
                    dpath.util.new(tmp_instance, tmp_path, [])
            tmp_path.append(p)
        print('tmp_instance:  ', tmp_instance)
        print('path: ', path)
        print('value: ', value)
        dpath.util.new(tmp_instance, path, value)
        print("MERGE")
        print('tmp_instance:  ', tmp_instance)
        print('self.instance: ', self.instance)
        print('merge_flags: ', merge_flags)
        #dpath.util.merge(self.instance, tmp_instance, flags=merge_policy)    
        dpath.util.merge(self.instance, tmp_instance, flags=merge_flags)
        
    def is_valid(self):
        current_schema = self.get_updated_schema()
        
        v = Draft6Validator(current_schema)
        return v.is_valid(self.instance)
            
"""
#schema = load_json_from_file('ob_with_if_and_array.schema.json')
schema = load_json_from_file('session.schema.json')
instance = load_json_from_file('session.json')

ob = JsonObject(schema, instance)

ob.is_valid()
cli_json_object_fix_errors(ob)

while False:
    if not cli_confirm('Do you want to enter a new value?'):
        break
    cli_json_object_set_value(ob)    

"""
