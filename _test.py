from helpers.json_object import JsonObject
from helpers.json_helpers import load_json_from_file, json_schme_path_generator
from helpers.cli_helpers import cli_json_object_fix_errors, cli_choose_option, cli_confirm, cli_json_get_value_by_type, cli_json_get_value_by_schema, cli_json_object_modify_instance
import dpath
from jsonschema import Draft6Validator

schema = load_json_from_file('app_json/session.schema.json')
instance = load_json_from_file('app_json/session.json')

ob = JsonObject(schema, instance)
cli_json_object_modify_instance(ob)