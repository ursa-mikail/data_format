# Read YAML and JSON files back to CSV
# Function to write data to CSV
def write_data_to_csv(file_path, data):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

# Read YAML data
with open(yaml_file_path, 'r') as file:
    yaml_data = yaml.safe_load(file)

# Write YAML data back to CSV 
yaml_data_ordered = [[item[header] for header in headers] for item in yaml_data]
write_data_to_csv(yaml_to_csv_file_path, yaml_data_ordered)
print(f"YAML data written back to CSV at {yaml_to_csv_file_path}")

# Read JSON data
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Write JSON data back to CSV
json_to_csv_file_path = os.path.join(output_dir, 'json_to_csv.csv')
write_data_to_csv(json_to_csv_file_path, [list(item.values()) for item in json_data])
print(f"JSON data written back to CSV at {json_to_csv_file_path}")

"""
YAML data written back to CSV at ./sample_data/data/yaml_to_csv.csv
JSON data written back to CSV at ./sample_data/data/json_to_csv.csv
"""