import csv

# Input and output file paths
input_file = 'data.csv'
output_file = 'formatted_data.csv'

# Function to find the maximum number of columns in the CSV
def find_max_columns(input_file):
    max_columns = 0
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        for row in reader:
            max_columns = max(max_columns, len(row))
    return max_columns

# Function to ensure proper formatting and quote sentences in 'Notes' column
def format_csv(input_file, output_file, max_number_of_columns):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    # Format the data: Ensure all cells in the Notes column are quoted if they meet the criteria
    for i, row in enumerate(rows):
        # Ensure proper number of columns by checking and adding empty values if necessary
        while len(row) < max_number_of_columns:
            row.append('')
        
        # If the Notes column has a sentence, ensure it's enclosed in quotes
        if row[3]:
            note = row[3]
            # Only quote if it's not already quoted and has more than 2 words
            if not note.startswith('"') and not note.endswith('"') and len(note.split()) > 2:
                row[3] = f'"{note}"'
    
    # Write the formatted data to a new CSV file
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)

# Find the maximum number of columns in the CSV
max_number_of_columns = find_max_columns(input_file)

# Call the function to process the input CSV file with the dynamic max column value
format_csv(input_file, output_file, max_number_of_columns)

print(f"CSV formatted and saved to {output_file}")


"""
1. Reading the CSV: The code reads the CSV data into a list of rows.

2. Ensuring consistent columns: If a row has fewer than max_number_of_columns columns, the code appends empty strings to ensure all rows have 5 columns (matching the header).
* find_max_columns is found by find_max_columns()

3. Formatting the 'Notes' column: For each row, if there is text in the "Notes" column that isn't already wrapped in quotes, it adds quotes around the text.

4. Writing the output: It writes the formatted rows back to a new CSV file, ensuring proper formatting.

Quote condition: It checks if the column is already quoted. If it isn't quoted and has more than 2 words (i.e., length of the word list > 2), it will add quotes.

Skipping short notes: If the note has fewer than 2 words or is already quoted, it won't add quotes.

"""