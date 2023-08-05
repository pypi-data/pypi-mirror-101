import json


def to_json_file(json_data, file_path, encoder=None):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4, cls=encoder)


def of_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_json(j):
    print(json.dumps(j, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
