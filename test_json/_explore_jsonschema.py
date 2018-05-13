from jsonschema import validate, Draft3Validator, Draft4Validator, Draft6Validator, FormatChecker, ErrorTree

schema = {"type" : "object", "properties" : {"price" : {"type" : "number"},"name" : {"type" : "string"},},}
validate({"name" : "Eggs", "price" : 34.99}, schema)
validate({"name" : "Eggs", "price" : "Invalid"}, schema)                                   
#################
schema = {"maxItems" : 2}
Draft3Validator(schema).is_valid([2, 3, 4])
###################3
schema = {"type" : "array", "items" : {"enum" : [1, 2, 3]}, "maxItems" : 2}
v = Draft3Validator(schema)
for error in sorted(v.iter_errors([2, 3, 4]), key=str):
    print(error.message)
################333333
schema = {"maxItems" : 2}
Draft3Validator(schema).validate([2, 3, 4])
#############3
schema = {
    "$schema": "http://json-schema.org/schema#",

    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"},
    },
    "required": ["email"]
}
Draft4Validator.check_schema(schema)
#########################
validate("localhost", {"format" : "hostname"})
validate("localhost", {"format" : "email"})
validate("localhost", {"format" : "email"}, format_checker=FormatChecker(),)
validate("m@j.com", {"format" : "email"}, format_checker=FormatChecker(),)
validate("-12", {"format" : "hostname"}, format_checker=FormatChecker(),)
################################
schema = {
    "items": {
        "anyOf": [
            {"type": "string", "maxLength": 2},
            {"type": "integer", "minimum": 5}
        ]
    }
}
instance = [{}, 3, "foo","1234"]
v = Draft6Validator(schema)
errors = sorted(v.iter_errors(instance), key=lambda e: e.path)
for error in errors:
    print(error.message)
tree = ErrorTree(v.iter_errors(instance))
##################################
from helpers.json_helpers import load_json_from_file

schema = load_json_from_file('if-exists-and-condiftion.schema.json')
v = Draft6Validator(schema)
instance = {"x": "r"}
errors = sorted(v.iter_errors(instance), key=lambda e: e.path)
for error in errors:
    print(error.message)

ns = schema
dependencies = ns.get('dependencies', {})
if dependencies:
    for dk in dependencies.keys():
        d = dependencies[dk]
        if 'if' in d.keys():
            # check condition is True
            if True:
                dependencies[dk] = d.get('then')

dependencies