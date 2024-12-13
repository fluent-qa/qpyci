import json
# import yaml
# import toml

def load_config(file_path:str):
    if file_path.endswith('.json'):
        with open(file_path) as f:
            return json.load(f)
    # elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
    #     with open(file_path) as f:
    #         return yaml.safe_load(f)
    # elif file_path.endswith('.toml'):
    #     with open(file_path) as f:
    #         return toml.load(f)
    else:
        raise ValueError("Unsupported file format")