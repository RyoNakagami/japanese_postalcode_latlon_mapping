import yaml
import json


def read_yaml(yaml_path: str) -> dict:
    with open(yaml_path) as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise (exc)


def read_json(json_path: str) -> dict:
    with open(json_path, 'r') as json_data:
        data = json.load(json_data)
    return data
