import yaml


def of_yaml(path_yaml: str):
    with open(path_yaml, 'r', encoding='utf-8') as f:
        return yaml.load(f.read(), Loader=yaml.FullLoader)
