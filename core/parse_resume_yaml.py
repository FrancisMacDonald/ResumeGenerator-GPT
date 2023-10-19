import yaml
from pydantic import ValidationError

from core.schema import Resume


def parse_yaml(path):
    with open(path, 'r') as stream:
        try:
            parsed_data = yaml.safe_load(stream)
            resume = Resume(**parsed_data)
        except yaml.YAMLError as exc:
            print(exc)
        except ValidationError as e:
            print(e.errors())

    return resume
