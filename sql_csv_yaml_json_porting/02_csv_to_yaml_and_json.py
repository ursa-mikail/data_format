# Convert CSV to YAML and JSON
import yaml
import json

# File paths
yaml_file_path = os.path.join(output_dir, 'data.yaml')
json_file_path = os.path.join(output_dir, 'data.json')

# Read CSV data
with open(csv_file_path, 'r') as file:
    reader = csv.DictReader(file)
    csv_data = [row for row in reader]

# Write to YAML
with open(yaml_file_path, 'w') as file:
    yaml.dump(csv_data, file, default_flow_style=False)

# Write to JSON
with open(json_file_path, 'w') as file:
    json.dump(csv_data, file, indent=4)

print(f"YAML data written to {yaml_file_path}")
print(f"JSON data written to {json_file_path}")

"""
YAML data written to ./sample_data/data/data.yaml
JSON data written to ./sample_data/data/data.json
"""