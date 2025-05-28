import json
from datetime import datetime

# Function to read JSON data
def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Function to convert Unix timestamp to YYYY-MM-DDTHH:MM:SS format
def format_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S')

# Function to calculate the time difference
def calculate_time_difference(time_start, time_end):
    now = datetime.utcnow()
    start = datetime.utcfromtimestamp(time_start)
    end = datetime.utcfromtimestamp(time_end)
    time_left = end - now
    
    if time_left.total_seconds() > 0:
        return f"Time left: {time_left}"
    else:
        return "Expired"

# Read JSON data from the file
data = read_json('modified_permit.json')

# Extract timestamps
time_start = data.get('time_start')
time_end = data.get('time_end')

# Convert timestamps to formatted strings
time_start_str = format_timestamp(time_start)
time_end_str = format_timestamp(time_end)

# Calculate time difference
status = calculate_time_difference(time_start, time_end)

# Print the results
print(f"Time Start: {time_start_str}")
print(f"Time End: {time_end_str}")
print(status)

"""
Time Start: 2025-05-28T19:06:04
Time End: 2025-05-29T22:52:44
Time left: 1 day, 3:42:15.882214
"""