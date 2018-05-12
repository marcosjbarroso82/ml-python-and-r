from helpers.cli_helpers import cli_json_override_property, cli_load_json_from_file, cli_json_print_errors
from helpers.json_helpers import load_json_from_file, json_get_errors
        
session_schema = load_json_from_file('session.schema.json')    
# Prepopulate with another session? Y
if input('start from previous session? [y/N]: ') == 'y':
    session = cli_load_json_from_file()

# new_session = cli_json_override_property(session, session_schema, confirm_prompt=True)
s = session
sch = session_schema

# Correct Errors
if json_get_errors(s, sch):
    cli_json_print_errors(s, sch)
    s = cli_json_override_property(s, sch)
    
"""
cargar el modelo si existe (es un json)
sino, crearlo en base al schema especificado

"""