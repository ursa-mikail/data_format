import yaml
import json
import os
from jsonschema import validate, ValidationError

def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)

def save_json(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def validate_and_render(policy_path, schema_path, output_path):
    data = load_yaml(policy_path)
    schema = load_yaml(schema_path)

    try:
        validate(instance=data, schema=schema)
        print(f"[✓] Valid: {policy_path}")
    except ValidationError as e:
        print(f"[!] Validation error in {policy_path}:\n{e.message}")
        return

    save_json(data, output_path)

if __name__ == "__main__":
    schema_file = "policies/schema.yaml"
    for filename in os.listdir("policies"):
        if filename.endswith(".yaml") and filename != "schema.yaml":
            input_path = f"policies/{filename}"
            output_path = f"policies/rendered/{filename.replace('.yaml', '.json')}"
            os.makedirs("policies/rendered", exist_ok=True)
            validate_and_render(input_path, schema_file, output_path)

"""
🔁 Reusable Terraform module for keysets
🔄 Environment separation using tfvars or for_each
🛡 Policy YAML validation and auto-render to JSON
🚫 No more raw hand-coded JSON policies
📉 Reduced changes needing approval: only policy YAML and vars
"""