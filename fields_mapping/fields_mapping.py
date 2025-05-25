#!pip install faker
import json
import random
from faker import Faker
from datetime import datetime

fake = Faker()

# Generate fake source.json
def generate_fake_data(n=5):
    data = []
    for _ in range(n):
        item = {
            "timestamp": fake.iso8601(),
            "log": fake.sentence(),
            "score": round(random.uniform(0, 100), 2),
            "reference": fake.uuid4(),
            "tags": fake.words(nb=random.randint(2, 5))
        }
        data.append(item)
    return data

with open("source.json", "w") as f:
    json.dump(generate_fake_data(), f, indent=2)

# Mapping specification
mapping = {
    "timestamp": {
        "target": "event.time",
        "type": "string"
    },
    "log": {
        "target": "event.message"
    },
    "score": {
        "target": "event.metrics.score",
        "type": "float"
    },
    "reference": {
        "target": "event.meta.id"
    },
    "tags": {
        "target": "event.labels[]"
    }
}

with open("mapping.json", "w") as f:
    json.dump(mapping, f, indent=2)

# ---- Transformer ---- #

def get_value(data, path):
    keys = path.split('.')
    for key in keys:
        if isinstance(data, list) and key.endswith("[]"):
            return [get_value(item, key[:-2]) for item in data]
        elif isinstance(data, dict):
            data = data.get(key)
        else:
            return None
    return data

def set_value(data, path, value):
    keys = path.split('.')
    for i, key in enumerate(keys):
        if key.endswith("[]"):
            key = key[:-2] # -2 to omit `[]`
            if key not in data:
                data[key] = []
            if isinstance(value, list):
                for val in value:
                    data[key].append(val)
            return
        if i == len(keys) - 1:
            data[key] = value
        else:
            data = data.setdefault(key, {})

def apply_type(val, target_type):
    try:
        if target_type == "int":
            return int(val)
        elif target_type == "float":
            return float(val)
        elif target_type == "string":
            return str(val)
        elif target_type == "bool":
            return bool(val)
    except:
        return val
    return val

def transform(source_list, mapping):
    result = []
    for source in source_list:
        item = {}
        for src, rule in mapping.items():
            tgt = rule["target"]
            val = source.get(src)
            if val is not None and "type" in rule:
                val = apply_type(val, rule["type"])
            set_value(item, tgt, val)
        result.append(item)
    return result

# Read source and mapping
with open("source.json") as f:
    source_data = json.load(f)

with open("mapping.json") as f:
    mapping_rules = json.load(f)

# Apply transform
transformed = transform(source_data, mapping_rules)

with open("target.json", "w") as f:
    json.dump(transformed, f, indent=2)

