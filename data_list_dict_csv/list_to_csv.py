import csv

# sample data
data = [["Name", "Age", "Gender"],
        ["John", "25", "Male"],
        ["Jane", "30", "Female"],
        ["Bob", "40", "Male"]]

# specify file name and mode ('w' for write)
filename = "example.csv"
mode = 'w'

# open the file with the specified mode and create a CSV writer object
with open(filename, mode, newline='') as file:
    writer = csv.writer(file, delimiter=',')
    
    # write the data to the file
    for row in data:
        writer.writerow(row)

# Read the data back
read_data = []
with open(filename, 'r', newline='') as file:
    for row in csv.reader(file):
        read_data.append(row)

# Output read data
print("Read Data (from csv):")
for row in read_data:
    print(row)

"""
Read Data (from csv):
['Name', 'Age', 'Gender']
['John', '25', 'Male']
['Jane', '30', 'Female']
['Bob', '40', 'Male']
"""    