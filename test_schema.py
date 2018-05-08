from helpers.cli_helpers import cli_json_override_property, cli_load_json_from_file
from helpers.json_helpers import load_json_from_file
        
session_schema = load_json_from_file('session.schema.json')    
# Prepopulate with another session? Y
if input('start from previous session? [y/N]: ') == 'y':
    session = cli_load_json_from_file()

new_session = cli_json_override_property(session, session_schema, confirm_prompt=True)
new_session
# What field do you want to override?