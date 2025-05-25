import csv

# Example lists
Kismet = [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]
Pneuma = [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]
Psyche = [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]
Opus = [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]
Soma = [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]

# Function to convert list to dictionary
def lists_to_dict(keys, *lists):
    return {key: value for key, value in zip(keys, lists)}

# Function to convert dictionary to list of lists
def dict_to_lists(dictionary):
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    return keys, values

# Function to convert list to CSV
def list_to_csv(filename, headers, *lists):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for row in zip(*lists):
            writer.writerow(row)

# Function to convert CSV to dictionary with variable names
def csv_to_dict(filename):
    variables = {}
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        lists = {header: [] for header in headers}
        for row in reader:
            for header, value in zip(headers, row):
                lists[header].append(int(value))
        variables.update(lists)
    return variables

# Example usage:
keys = ["Kismet", "Pneuma", "Psyche", "Opus", "Soma"]
lists = [Kismet, Pneuma, Psyche, Opus, Soma]

# Convert lists to dictionary
data_dict = lists_to_dict(keys, *lists)
print("Dictionary:", data_dict)

# Convert dictionary back to lists
keys, values = dict_to_lists(data_dict)
print("Keys:", keys)
print("Values:", values)

# Convert lists to CSV
list_to_csv('output.csv', keys, *lists)

# Convert CSV back to dictionary with variable names
csv_data_dict = csv_to_dict('output.csv')
print("CSV to Dictionary with Variables:", csv_data_dict)

# Dynamically create variables
locals().update(csv_data_dict)

# Accessing the variables created
print("Kismet:", Kismet)
print("Pneuma:", Pneuma)
print("Psyche:", Psyche)
print("Opus:", Opus)
print("Soma:", Soma)

print(f"\n[csv_data_dict]:")
# Print csv_data_dict keys and values
for key, value in csv_data_dict.items():
    print(f"{key}: {value}")

"""
Dictionary: {'Kismet': [50, 50, 50, 0, 0, 0, 0, 0, 50, 75], 'Pneuma': [50, 50, 50, 0, 0, 0, 0, 0, 50, 75], 'Psyche': [50, 50, 50, 0, 0, 0, 0, 0, 50, 75], 'Opus': [50, 50, 50, 0, 0, 0, 0, 0, 50, 75], 'Soma': [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]}
Keys: ['Kismet', 'Pneuma', 'Psyche', 'Opus', 'Soma']
Values: [[50, 50, 50, 0, 0, 0, 0, 0, 50, 75], [50, 50, 50, 0, 0, 0, 0, 0, 50, 75], [50, 50, 50, 0, 0, 0, 0, 0, 50, 75], [50, 50, 50, 0, 0, 0, 0, 0, 50, 75], [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]]
CSV to Dictionary with Variables: {'Kismet': [50, 50, 50, 0, 0, 0, 0, 0, 50, 75], 'Pneuma': [50, 50, 50, 0, 0, 0, 0, 0, 50, 75], 'Psyche': [50, 50, 50, 0, 0, 0, 0, 0, 50, 75], 'Opus': [50, 50, 50, 0, 0, 0, 0, 0, 50, 75], 'Soma': [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]}
Kismet: [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]
Pneuma: [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]
Psyche: [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]
Opus: [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]
Soma: [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]

[csv_data_dict]:
Kismet: [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]
Pneuma: [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]
Psyche: [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]
Opus: [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]
Soma: [50, 50, 50, 0, 0, 0, 0, 0, 50, 75]
"""