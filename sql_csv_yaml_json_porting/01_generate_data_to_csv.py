# Generate Random CSV Data
import csv
import random
import os
import hashlib

# Create directory if not exists
output_dir = './sample_data/data/'
os.makedirs(output_dir, exist_ok=True)

# File paths
csv_file_path = os.path.join(output_dir, 'data.csv')

# Headers
headers = ['service', 'user', 'time_stamp', 'hash_of_all_data']

# Generate random data
def generate_random_data(num_rows):
    data = []
    for _ in range(num_rows):
        service = f"service_{random.getrandbits(40):010x}"
        user = f"user_{random.getrandbits(40):010x}"
        time_stamp = random.randint(1000000000, 2000000000)
        combined_data = f"{service},{user},{time_stamp}"
        hash_of_all_data = hashlib.sha256(combined_data.encode()).hexdigest()
        data.append([service, user, time_stamp, hash_of_all_data])
    return data

# Write to CSV
num_rows = 3
data = generate_random_data(num_rows)
with open(csv_file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(data)

print(f"CSV data written to {csv_file_path}")

"""
CSV data written to ./sample_data/data/data.csv
"""