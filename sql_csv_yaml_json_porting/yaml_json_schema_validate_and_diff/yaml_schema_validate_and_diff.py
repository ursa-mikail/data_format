#!pip install jsonschema
#!pip install deepdiff

import yaml
import json
import os
import sys
import argparse
from jsonschema import validate, ValidationError
from deepdiff import DeepDiff

def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)

def load_json(path):
    with open(path) as f:
        return json.load(f)

def save_yaml(data, path):
    with open(path, 'w') as f:
        yaml.safe_dump(data, f, sort_keys=False)

def save_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def convert_file(input_file, output_file):
    if input_file.endswith('.yaml') or input_file.endswith('.yml'):
        data = load_yaml(input_file)
        save_json(data, output_file)
    elif input_file.endswith('.json'):
        data = load_json(input_file)
        save_yaml(data, output_file)
    else:
        print(f"[!] Unsupported file format: {input_file}")
        #sys.exit(1)
    print(f"[✓] Converted: {input_file} → {output_file}")

def validate_yaml(yaml_file, schema_file):
    schema = load_yaml(schema_file)
    data = load_yaml(yaml_file)

    try:
        validate(instance=data, schema=schema)
        print(f"[✓] VALID: {yaml_file}")
        return data
    except ValidationError as e:
        print(f"[✗] INVALID: {yaml_file}\n    {e.message}")
        return None

def diff_yaml(old_file, new_file):
    old_data = load_yaml(old_file)
    new_data = load_yaml(new_file)

    diff = DeepDiff(old_data, new_data, verbose_level=2)
    if not diff:
        print("[✓] No differences found.")
    else:
        print("[🔁] Differences:")
        print(json.dumps(diff, indent=2))

def main():
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("old", help="Old YAML file")
    parser.add_argument("new", help="New YAML file")
    parser.add_argument("--schema", required=True, help="Path to YAML schema file")
    parser.add_argument("--convert", action="store_true", help="Convert YAML ↔ JSON")
    args = parser.parse_args()
    """
    args = argparse.Namespace()
    args.old = "old.yaml"
    args.new = "new.yaml"
    args.schema = "schema.yaml"
    args.convert = False

    if args.convert:
        convert_file(args.old, args.old.replace('.yaml', '.json'))
        convert_file(args.new, args.new.replace('.yaml', '.json'))
    else:
        print("🔍 Validating...")
        old_data = validate_yaml(args.old, args.schema)
        new_data = validate_yaml(args.new, args.schema)

        if old_data and new_data:
            print("\n🔍 Running Diff...")
            diff_yaml(args.old, args.new)

if __name__ == "__main__":
    main()

"""
🔍 Validating...
[✓] VALID: old.yaml
[✓] VALID: new.yaml

🔍 Running Diff...
[🔁] Differences:
{
  "iterable_item_added": {
    "root['bindings'][0]['members'][1]": "user:bob@example.com",
    "root['bindings'][1]": {
      "role": "roles/cloudkms.admin",
      "members": [
        "group:admin-team@example.com"
      ]
    }
  }
}
"""