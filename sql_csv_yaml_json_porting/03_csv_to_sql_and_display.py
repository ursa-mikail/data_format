# Create an SQLite Database and Insert Data
import sqlite3

# File path
db_file_path = os.path.join(output_dir, 'data.db')

# Create SQLite database and table
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS data (
    service TEXT,
    user TEXT,
    time_stamp INTEGER,
    hash_of_all_data TEXT
)''')

# Insert CSV data into SQLite
for row in csv_data:
    cursor.execute('''INSERT INTO data (service, user, time_stamp, hash_of_all_data)
                      VALUES (:service, :user, :time_stamp, :hash_of_all_data)''', row)

conn.commit()

# Query to display all data including headers
cursor.execute("SELECT * FROM data")
rows = cursor.fetchall()

# Display data
print(headers)
for row in rows:
    print(row)

conn.close()
print(f"SQLite data written to {db_file_path}")

"""
['service', 'user', 'time_stamp', 'hash_of_all_data']
('service_d75acdd53b', 'user_31cb608905', 1853093073, 'a6c474dff647eb511feb68b4c8a4cf8e862bc5e4598eb03370cbad8de23fe09e')
('service_130a560357', 'user_5382952a4a', 1651703894, 'cfd2ba2cd3b3022a8a0779bc4951bae1ac489a60449a2b91b71c52a9a576f7f8')
('service_6fdd6891b1', 'user_b6b3705c70', 1206747340, '19b063b0e1ed5bfba587f1e3b709babd9d7fb6cc8f44eeb007a4c00f0262bf34')
SQLite data written to ./sample_data/data/data.db
"""