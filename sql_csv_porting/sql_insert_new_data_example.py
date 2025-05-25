# Create the new_data DataFrame with the specified data
data_dict = {
    'longitude': [-123.92],
    'latitude': [41.54],
    'housing_median_age': [22.0],
    'total_rooms': [2920.0],
    'total_bedrooms': [636.0],
    'population': [1382.0],
    'households': [499.0],
    'median_income': [2.0202],
    'median_house_value': [71100.0]
}
new_data = pd.DataFrame(data_dict)

# Show the new_data DataFrame
print("New DataFrame:")
print(new_data)

# Connect to an SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(database_name)

# Load the new_data DataFrame into a SQL table
new_data.to_sql('housing', conn, if_exists='replace', index=False)

# Create a cursor object
cur = conn.cursor()

# Define and execute an SQL query to retrieve the data
sql_query = "SELECT * FROM housing"
cur.execute(sql_query)

# Fetch all results from the executed query
results = cur.fetchall()

# Print the results
print("\nResults from SQL query:")
for row in results:
    print(row)

###
# Define and execute an SQL query to retrieve data from new_housing
sql_query_new = "SELECT * FROM new_housing"
cur.execute(sql_query_new)
new_results = cur.fetchall()

print("\nResults from new_housing table:")
for row in new_results:
    print(row)

# Close the connection
conn.close()

"""
New DataFrame:
   longitude  latitude  housing_median_age  total_rooms  total_bedrooms  \
0    -123.92     41.54                22.0       2920.0           636.0   

   population  households  median_income  median_house_value  
0      1382.0       499.0         2.0202             71100.0  

Results from SQL query:
(-123.92, 41.54, 22.0, 2920.0, 636.0, 1382.0, 499.0, 2.0202, 71100.0)

Results from new_housing table:
(1, 636.0, 'New data with 636 total bedrooms')
(2, 166.0, 'New data with 166 total bedrooms')
"""