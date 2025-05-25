import sqlite3

source_db = './sample_data/example.db'
# Connect to SQLite (it will create the database file if it doesn't exist)
conn = sqlite3.connect(source_db)

# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    email TEXT UNIQUE
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

# Connect to the database
conn = sqlite3.connect(source_db)
cursor = conn.cursor()

# Insert data into the table
cursor.execute('''
INSERT INTO users (name, age, email)
VALUES ('Alice', 30, 'alice@example.com')
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

# Connect to the database
conn = sqlite3.connect(source_db)
cursor = conn.cursor()

# Query the data
cursor.execute('SELECT * FROM users')

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the connection
conn.close()

"""
(1, 'Alice', 30, 'alice@example.com')
"""