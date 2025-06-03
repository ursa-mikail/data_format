#!pip install jsonschema
#!pip install deepdiff

import sys
import yaml
from deepdiff import DeepDiff
from jsonschema import validate, ValidationError


def load_yaml(file_path):
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)


def validate_yaml(data, schema):
    try:
        validate(instance=data, schema=schema)
        print("[✓] YAML is valid according to the schema.")
    except ValidationError as e:
        print("[!] YAML validation error:", e.message)
        #sys.exit(1)


def diff_yaml(old_yaml, new_yaml):
    diff = DeepDiff(old_yaml, new_yaml, ignore_order=True)
    if diff:
        print("🔍 Differences found:")
        print(diff.pretty())
    else:
        print("✅ No differences found.")


if __name__ == "__main__":
    """
    import argparse

    parser = argparse.ArgumentParser(description="YAML Diff and Validator")
    parser.add_argument("old", help="Path to old YAML file")
    parser.add_argument("new", help="Path to new YAML file")
    parser.add_argument("--schema", help="Optional JSON Schema file for validation", required=False)

    args = parser.parse_args()

    old_yaml = load_yaml(args.old)
    new_yaml = load_yaml(args.new)

    if args.schema:
        schema = load_yaml(args.schema)
        print(f"\nValidating {args.old}...")
        validate_yaml(old_yaml, schema)
        print(f"\nValidating {args.new}...")
        validate_yaml(new_yaml, schema)

    import os

    if args.schema and not os.path.exists(args.schema):
        print(f"[!] Schema file not found: {args.schema}")        
    """
    print("\nComparing files...")
    # Define file paths
    old_file = 'old.yaml'
    new_file = 'new.yaml'
    #schema_file = 'schema.json'  # optional, comment out if not used
    schema_file = 'schema.yaml'  # optional, comment out if not used


    # Load YAML files
    old_yaml_data = load_yaml(old_file)
    new_yaml_data = load_yaml(new_file)

    # Optionally load and validate against schema
    try:
        schema = load_yaml(schema_file)
        print(f"\nValidating {old_file}...")
        validate_yaml(old_yaml_data, schema)

        print(f"\nValidating {new_file}...")
        validate_yaml(new_yaml_data, schema)
    except FileNotFoundError:
        print("Schema file not found. Skipping validation...")

    # Show diff
    print("\nComparing files...")
    diff_yaml(old_yaml_data, new_yaml_data)
   

"""
Comparing files...

Validating old.yaml...
[✓] YAML is valid according to the schema.

Validating new.yaml...
[✓] YAML is valid according to the schema.

Comparing files...
🔍 Differences found:
Item root['location'] added to dictionary.
Value of root['age'] changed from 30 to 31.
Value of root['role'] changed from "admin" to "user".
"""    