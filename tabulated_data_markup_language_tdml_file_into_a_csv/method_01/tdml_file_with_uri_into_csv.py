import csv
import re
import requests

def txt_to_csv(txt_file_path, csv_file_path, delimiter='[delimiter]'):
    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
        lines = txt_file.readlines()

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for line in lines:
            row = line.strip().split(delimiter)
            writer.writerow(row)

def extract_url_from_cell(cell, uri_start='[uri_start]', uri_end='[uri_end]'):
    pattern = re.escape(uri_start) + r'(.*?)' + re.escape(uri_end)
    match = re.search(pattern, cell)
    return match.group(1).strip() if match else None

def find_urls_in_csv(csv_file_path):
    found_urls = []
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row_idx, row in enumerate(reader):
            for col_idx, cell in enumerate(row):
                url = extract_url_from_cell(cell)
                if url:
                    found_urls.append((url, row_idx, col_idx))
    return found_urls

def fetch_text_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print("Error fetching URL:", e)
        return None

def extract_from_csv(csv_file_path, mode='row', index=0):
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        reader = list(csv.reader(file))
        if mode == 'row':
            return reader[index] if index < len(reader) else None
        elif mode == 'col':
            return [row[index] for row in reader if index < len(row)]
    return None

def csv_dimensions(csv_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        rows = list(csv.reader(file))
        return len(rows), len(rows[0]) if rows else 0

def get_element(csv_file_path, row_idx, col_idx):
    with open(csv_file_path, 'r', encoding='utf-8') as file:
        rows = list(csv.reader(file))
        return rows[row_idx][col_idx] if row_idx < len(rows) and col_idx < len(rows[row_idx]) else None


# === USAGE ===
delimiter = '[delimiter]'

# Step 1: Convert data.txt to data.csv
txt_to_csv('./sample_data/data.txt', './sample_data/data.csv', delimiter)

# Step 2: Find URLs in any cell of data.csv
found_urls = find_urls_in_csv('./sample_data/data.csv')

if found_urls:
    for idx, (url, r, c) in enumerate(found_urls, 1):
        print(f"======== [cout url {idx}: {url} found at row {r}, column {c}] ========")
    # Optionally, you can fetch the URL contents if needed
    for url, _, _ in found_urls:
        fetched_txt = fetch_text_from_url(url)
        if fetched_txt:
            print(f"Fetched content from {url}")
            print(fetched_txt)
else:
    print("No URLs found in any cell.")

"""
======== [cout url 1: https://raw.githubusercontent.com/ursa-mikail/tabulated_data_markup_language_tdml_file_into_a_csv/refs/heads/main/method_01/tdml_file_into_csv.py found at row 2, column 3] ========
======== [cout url 2: https://raw.githubusercontent.com/ursa-mikail/toolings/refs/heads/main/python/utilities/readme.md found at row 4, column 3] ========
Fetched content from https://raw.githubusercontent.com/ursa-mikail/tabulated_data_markup_language_tdml_file_into_a_csv/refs/heads/main/method_01/tdml_file_into_csv.py
:
Fetched content from https://raw.githubusercontent.com/ursa-mikail/toolings/refs/heads/main/python/utilities/readme.md
:


"""