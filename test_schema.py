"""

"""
session = {
        "name": "session", "ds_path": "ds_path", "model_path": "model_path"
        }

session_schema = {  
  "type": "object",  
  "required": ["name"],
  "properties": {
    "name": {      
      "type": "string"
    },
    "ds_path": {
      "type": "string"      
    },    
    "model_path": {
      "type": "string"      
    }
  }
}
    
from cli_helpers import cli_confirm, cli_choose_option, cli_json_schema_update_prop
        
# Prepopulate with another session? Y
def cli_json_override_property(obj, schema, confirm_prompt=False):
    if confirm_prompt and not cli_confirm('Do you want to override a property?[y/n]: '):
            return

    # Choose property
    prop = cli_choose_option(session.keys())

    obj = cli_json_schema_update_prop(prop, obj, schema)
    return session

new_session = cli_json_override_property(session, session_schema, confirm_prompt=True)
new_session
# What field do you want to override?