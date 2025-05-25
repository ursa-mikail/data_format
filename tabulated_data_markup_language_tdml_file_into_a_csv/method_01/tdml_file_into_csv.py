import csv

def txt_to_csv(txt_file_path, csv_file_path, delimiter='|'):
    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for line in lines:
            row = line.strip().split(delimiter)
            writer.writerow(row)        # csv writer may not close the cell with ',', hence, we may require a formatter later.

def extract_from_csv(csv_file_path, mode='row', index=0):
    data = []
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = list(csv.reader(file))
        if mode == 'row':
            return reader[index] if index < len(reader) else None
        elif mode == 'col':
            if reader:
                return [row[index] for row in reader if index < len(row)]
    return None

def csv_dimensions(csv_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        rows = list(csv.reader(file))
        num_rows = len(rows)
        num_cols = len(rows[0]) if rows else 0
        return num_rows, num_cols

def get_element(csv_file_path, row_idx, col_idx):
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        rows = list(csv.reader(file))
        if row_idx < len(rows) and col_idx < len(rows[row_idx]):
            return rows[row_idx][col_idx]
        return None


# Usage
delimiter = '[delimiter]'
txt_to_csv('./sample_data/data.txt', 'data.csv', delimiter)

print("Row 1:", extract_from_csv('data.csv', 'row', 1))
print("Col 2:", extract_from_csv('data.csv', 'col', 2))

rows, cols = csv_dimensions('data.csv')
print("Dimensions:", rows, "rows x", cols, "columns")

print("Element at (1,2):", get_element('data.csv', 1, 2))

"""
Row 1: ['John Gray', '25', 'Engineer', '']
Col 2: ['Occupation', 'Engineer', 'Designer', 'Data Scientist']
Dimensions: 4 rows x 4 columns
Element at (1,2): Engineer
"""