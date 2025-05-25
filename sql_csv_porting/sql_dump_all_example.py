import pandas as pd
import pandasql as ps
import sqlite3

# Connect to an SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(database_name)
# Create a cursor object
cur = conn.cursor()

# Function to list all tables
def list_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    return [table[0] for table in tables]

# Function to dump all data from all tables
def dump_all_data(cursor, tables):
    for table in tables:
        print(f"\nData from {table} table:")
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        col_names = [col[1] for col in columns]
        print(f"Columns: {col_names}")
        
        cursor.execute(f"SELECT * FROM {table};")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

# List all tables
tables = list_tables(cur)

# Dump all data from all tables
dump_all_data(cur, tables)

# Close the connection
conn.close()

"""
Data from filtered_housing table:
Columns: ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income', 'median_house_value', 'context']
(-123.92, 41.54, 22.0, 2920.0, 636.0, 1382.0, 499.0, 2.0202, 71100.0, 'Filtered data: latitude > 41.5 and total_rooms > 2800')

Data from new_housing table:
Columns: ['id', 'total_bedrooms', 'context']
(1, 636.0, 'New data with 636 total bedrooms')
(2, 166.0, 'New data with 166 total bedrooms')

Data from housing table:
Columns: ['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population', 'households', 'median_income', 'median_house_value']
(-123.92, 41.54, 22.0, 2920.0, 636.0, 1382.0, 499.0, 2.0202, 71100.0)
"""