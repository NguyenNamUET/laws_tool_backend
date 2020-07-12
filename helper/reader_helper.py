import gzip
import json


def load_jsonl_from_gz(file_gz_path):
    try:
        with gzip.open(file_gz_path, 'rt') as f:
            file_content = f.read()
            obj = json.loads(file_content)
            return obj
    except Exception as e:
        print(e)
