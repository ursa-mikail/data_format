import yaml
import pandas as pd
import sqlite3
import json
import random
import string
import hashlib
import re

# Step 1: Randomly generate YAML data
def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_metadata():
    return {
        "type": generate_random_string(5),
        "description": generate_random_string(20)
    }

def generate_random_item():
    return {
        "key": generate_random_string(),
        "value": generate_random_string(),
        "metadata": generate_random_metadata(),
        "chunk": "0x" + ''.join(random.choices(string.hexdigits, k=6))
    }

# Create random YAML data
num_items = 5  # Change this to generate more items
yaml_data = {"Item": [generate_random_item() for _ in range(num_items)]}

# Convert to YAML
yaml_str = yaml.dump(yaml_data, default_flow_style=False)
print("Generated YAML:")
print(yaml_str)

# Step 2: Convert YAML data to CSV format
data = yaml.safe_load(yaml_str)
df = pd.DataFrame(data['Item'])

# Convert metadata dictionary to JSON string for CSV export
def clean_meta(meta):
    try:
        # Remove any extraneous characters from the start and end of the string
        meta = meta.strip()
        
        # Use a regex to replace double double-quotes with single double-quotes
        meta = re.sub(r'""', '"', meta)
        
        # Ensure all escape sequences are handled properly
        meta = meta.encode().decode('unicode_escape')
        
        # Load and re-encode to ensure valid JSON format
        cleaned_meta = json.dumps(json.loads(meta))
        return cleaned_meta
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error during cleaning: {e}")
        # If cleaning fails, return an empty JSON object or handle it accordingly
        return '{}'

df['meta'] = df['metadata'].apply(lambda x: clean_meta(json.dumps(x)))

# Convert hex string to a plain string (no array)
def hex_to_str(hex_str):
    # Remove '0x' prefix and join hex characters
    return hex_str[2:].upper()

df['hex'] = df['chunk'].apply(hex_to_str)

# Step 2.5: Add SHA-256 hash column
def generate_sha256_hash(row):
    # Generate SHA-256 hash of 'key' + 'value' + 'metadata'
    hash_input = f"{row['key']} {row['value']} {json.dumps(row['metadata'])}"
    return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()

df['sha256'] = df.apply(generate_sha256_hash, axis=1)

# Reorder columns to match the desired format
df = df[['sha256', 'key', 'value', 'meta', 'hex']]

# Save DataFrame to CSV
dir_start = './sample_data/'
csv_file = dir_start + 'items.csv'
df.to_csv(csv_file, index=False, sep=',', quotechar='"')
print(f"\nCSV data saved to {csv_file}")

# Step 3: Import the CSV data into an SQL database
conn = sqlite3.connect(':memory:')  # Using in-memory SQLite database
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE items (
    sha256 TEXT,
    key TEXT,
    value TEXT,
    meta TEXT,
    hex TEXT
)
""")

# Read the CSV file and insert into the SQL table
df.to_sql('items', conn, if_exists='append', index=False)

# Commit changes
conn.commit()

# Step 4: Function to get 'meta' by 'sha256'
def get_meta_by_sha256(sha256_value):
    cursor.execute("SELECT meta FROM items WHERE sha256 = ?", (sha256_value,))
    result = cursor.fetchone()
    if result:
        raw_meta = result[0]  # Extract the 'meta' string from the tuple
        print(f"Raw meta data: {raw_meta}")  # Print the raw meta data
        try:
            # Clean the raw data before attempting to decode
            cleaned_meta = clean_meta(raw_meta)
            return json.loads(cleaned_meta)  # Return the meta as a dictionary
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error for {sha256_value}: {e}")
            return None
    else:
        return None

# Step 5: Query all sha256 values and display associated meta
cursor.execute("SELECT sha256 FROM items")
sha256_values = cursor.fetchall()

# Display the meta for each sha256 value
for sha256_value in sha256_values:
    sha256_value = sha256_value[0]  # Extract sha256 value from tuple
    meta = get_meta_by_sha256(sha256_value)
    print(f"\nSHA-256: {sha256_value}")
    if meta:
        print(f"Meta: {json.dumps(meta, indent=2)}")
    else:
        print("No meta found.")


sha256_value = 'nfPeTJDwInIKk96iOK0x'
meta = get_meta_by_sha256(sha256_value)
print(f"\nSHA-256: {sha256_value}")
if meta:
    print(f"Meta: {json.dumps(meta, indent=2)}")
else:
    print("No meta found.")

# Close the database connection
# conn.close()

# Step 4: Export data back to CSV
exported_csv_file = dir_start + 'items_exported.csv'

# Retrieve all rows
cursor.execute("SELECT sha256, key, value, meta, hex FROM items")
rows = cursor.fetchall()

# Prepare data for export
export_df = pd.DataFrame(rows, columns=["sha256", "key", "value", "meta", "hex"])

# Export to CSV
export_df.to_csv(exported_csv_file, index=False, sep=',', quotechar='"')
print(f"\nExported CSV data saved to {exported_csv_file}")

# Close the database connection
conn.close()

"""
Generated YAML:
Item:
- chunk: '0xa7CfDc'
  key: r0MGEJpTob
  metadata:
    description: IB2xHXeudn28IekX1qst
    type: NeSvK
  value: XPY17yle14
- chunk: '0x59bf22'
  key: MCAMr5mbgZ
  metadata:
    description: ERsG4WLdtuMnrF0FWU0g
    type: Osnb2
  value: eJd5PD1wvw
- chunk: '0xaAC5Be'
  key: TD2LN0mr8W
  metadata:
    description: R4HMhzwVBfbHiNIA29lE
    type: fW68Q
  value: yqrxI6fwRO
- chunk: '0xdAeb90'
  key: R116Do3RWN
  metadata:
    description: IQTuFD6vFErwsDOc8HGO
    type: wqD7I
  value: SwMIrJipTN
- chunk: '0x0d478B'
  key: 30WKDFdFfz
  metadata:
    description: WkBOG6ZtI2oX7XRKLqdI
    type: BUNb6
  value: ZwcP9zu3Nw


CSV data saved to ./sample_data/items.csv
Raw meta data: {"description": "IB2xHXeudn28IekX1qst", "type": "NeSvK"}

SHA-256: 2cee1b70308d4cda2b40ec87f82461ec6165f104435f1edca4265637a348d7ec
Meta: {
  "description": "IB2xHXeudn28IekX1qst",
  "type": "NeSvK"
}
Raw meta data: {"description": "ERsG4WLdtuMnrF0FWU0g", "type": "Osnb2"}

SHA-256: 25ca9d580f9d3f8e31fd3ce87c73de411a4053601386156c8c2c14d534f1f6af
Meta: {
  "description": "ERsG4WLdtuMnrF0FWU0g",
  "type": "Osnb2"
}
Raw meta data: {"description": "R4HMhzwVBfbHiNIA29lE", "type": "fW68Q"}

SHA-256: 286b5f4a385f9fb42d38d6aa2224ae29e2a67eea584a5e94ffb2678028d1553c
Meta: {
  "description": "R4HMhzwVBfbHiNIA29lE",
  "type": "fW68Q"
}
Raw meta data: {"description": "IQTuFD6vFErwsDOc8HGO", "type": "wqD7I"}

SHA-256: 1d5692968a90b9e1f6125034ae23eb1bae64df6c5d665ef35a1b1306e3e1f055
Meta: {
  "description": "IQTuFD6vFErwsDOc8HGO",
  "type": "wqD7I"
}
Raw meta data: {"description": "WkBOG6ZtI2oX7XRKLqdI", "type": "BUNb6"}

SHA-256: 1182f2922b63eb07efbe8b3148396716c5cdcf3caaa9a95e05ab5b5fc711c669
Meta: {
  "description": "WkBOG6ZtI2oX7XRKLqdI",
  "type": "BUNb6"
}

SHA-256: nfPeTJDwInIKk96iOK0x
No meta found.

Exported CSV data saved to ./sample_data/items_exported.csv

"""