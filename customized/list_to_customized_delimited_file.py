# list_to_customized_delimited_file.py
# Custom Delimiter File Write/Read
filename = "example.txt"
mode = 'w'
delimiter = "<--break-->"

# Sample data
data = [
    ["apple", "banana", "cherry"],
    ["dog", "cat", "mouse"],
    ["sun", "moon", "stars"]
]

# Write to the file using the arbitrary delimiter
with open(filename, mode, newline='') as file:
    for row in data:
        file.write(delimiter.join(row) + '\n')

# Read the data back
read_data = []
with open(filename, 'r', newline='') as file:
    for line in file:
        # Strip the newline and split by the custom delimiter
        read_data.append(line.strip().split(delimiter))

# Output read data
for row in read_data:
    print(row)

"""
['apple', 'banana', 'cherry']
['dog', 'cat', 'mouse']
['sun', 'moon', 'stars']
"""    