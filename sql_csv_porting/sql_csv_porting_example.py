#!pip install pandasql
import pandas as pd
import pandasql as ps
import sqlite3

"""
1. Getting csv file
2. Filtering data
3. Load to sql as table
4. Export sql table to csv
"""

# Load the CSV file into a DataFrame
data = pd.read_csv('./sample_data/california_housing_test.csv')
database_name = './sample_data/housing_data.db'

#data = data.set_index('id')
#print(data.query('latitude > 41'))

# Define an SQL query to filter data
sql_query = """
SELECT * 
FROM data 
WHERE latitude > 41.5 
AND total_rooms > 2800
"""

# Execute the SQL query and store the result in a new DataFrame
filtered_data = ps.sqldf(sql_query, locals())
print("Filtered Data:")
print(filtered_data)

# Add context to the filtered_data DataFrame
filtered_data['context'] = 'Filtered data: latitude > 41.5 and total_rooms > 2800'

# Create the new_data DataFrame with context
new_data_dict = {
    'id': [1, 2],
    'total_bedrooms': [636.0, 166.0],
    'context': ['New data with 636 total bedrooms', 'New data with 166 total bedrooms']
}
new_data = pd.DataFrame(new_data_dict)
print("\nNew Data:")
print(new_data)

# Connect to an SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(database_name)

# Load the filtered data into a SQL table
filtered_data.to_sql('filtered_housing', conn, if_exists='replace', index=False)

# Load the new_data DataFrame into a SQL table
new_data.to_sql('new_housing', conn, if_exists='replace', index=False)

# Create a cursor object
cur = conn.cursor()

# Define and execute an SQL query to retrieve data from filtered_housing
sql_query_filtered = "SELECT * FROM filtered_housing"
cur.execute(sql_query_filtered)
filtered_results = cur.fetchall()

print("\nResults from filtered_housing table:")
for row in filtered_results:
    print(row)

# Define and execute an SQL query to retrieve data from new_housing
sql_query_new = "SELECT * FROM new_housing"
cur.execute(sql_query_new)
new_results = cur.fetchall()

print("\nResults from new_housing table:")
for row in new_results:
    print(row)

# Load the filtered data into a new SQL table
filtered_data.to_sql('filtered_housing_beyond_41.5', conn, if_exists='replace', index=False)

# Export the filtered DataFrame to a CSV file
csv_filename = './sample_data/latitude_beyond_41.5_and_total_rooms_more_than_2800.csv'
filtered_data.to_csv(csv_filename, index=False)

# Close the connection
conn.close()

print(f"\nData has been exported to {csv_filename}")

"""
Filtered Data:
   longitude  latitude  housing_median_age  total_rooms  total_bedrooms  \
0    -123.92     41.54                22.0       2920.0           636.0   

   population  households  median_income  median_house_value  
0      1382.0       499.0         2.0202             71100.0  

New Data:
   id  total_bedrooms                           context
0   1           636.0  New data with 636 total bedrooms
1   2           166.0  New data with 166 total bedrooms

Results from filtered_housing table:
(-123.92, 41.54, 22.0, 2920.0, 636.0, 1382.0, 499.0, 2.0202, 71100.0, 'Filtered data: latitude > 41.5 and total_rooms > 2800')

Results from new_housing table:
(1, 636.0, 'New data with 636 total bedrooms')
(2, 166.0, 'New data with 166 total bedrooms')

Data has been exported to ./sample_data/latitude_beyond_41.5_and_total_rooms_more_than_2800.csv

"""