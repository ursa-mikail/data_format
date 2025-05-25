def write_data_to_tdml_file(filename, data):
    with open(filename, "w") as f:
        f.write(data)

files_tdml = ["f1.tdml", "f2.tdml", "f3.tdml"]

data_01 = """
'''
Type
'''
'''
Procedure
'''
'''
Adversary control(s)
'''
'''
Objective
'''
"""

data_02 = """
'''
IND-CPA
'''
'''
Challenger: KE, KD = KG(security parameter)
Adversary: m0, m1 = choose 2 messages of the same length. Send m0, m1 to challenger. Perform additional operations in polynomial time including calls to the encryption oracle.
Challenger: b = randomly choose between 0 and 1
Challenger: C := E(KE, mb). Send C to adversary.
Adversary: perform additional operations in polynomial time including calls to the encryption oracle. Output guess.
If guess = b, the adversary wins.
Restriction: Messages to be of the same length aim to prevent adversary from trivially winning the game by just comparing the length of ciphertexts. However, this requirement is weak, especially because it assumes only a single interaction between adversary and challenger.
'''
'''
Plaintext messages.
Ciphertext messages.
e.g. adversary has Mark’s public key.
'''
'''
Adversary tries to guess which of the messages was encrypted.
'''
"""

data_03 = """
'''
IND-CPA1
'''
'''
Challenger: KE,KD = KG(security parameter)
Adversary (a polynomially-bounded number of times): call the encryption or decryption oracle for arbitrary plaintexts or ciphertexts, respectively
Adversary: m0,m1= choose 2 messages of the same length
Challenger: b= randomly choose between 0 and 1
Challenger: C:=E(KE,mb)Send C to adversary.
Adversary: perform additional operations in polynomial time. Output guess
If guess=b, the adversary wins
'''
'''
Use / abuse service as decryption oracle (but cannot depend on the challenge y).
Adversary tries to guess which of the messages was encrypted.
'''
"""

data_list = [data_01, data_02, data_03]

for file, data in zip(files_tdml, data_list):
    write_data_to_tdml_file(file, data)


# converts a Tabulated Data Markup Language (TDML) file into a CSV file, stitching data column by column. This assumes TDML is structured as tabular data in a clear text format, rather than an XML-based format.
import csv
import argparse
import glob
import re

def read_tdml(file_path):
    """
    Reads a TDML file and returns the parsed data as a list of lists.
    Handles sections separated by triple quotes (''').
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add a sentinel ''' at the end if not present to handle last section
    if not content.endswith("'''"):
        content += "'''"
        
    # Split keeping empty sections between triple quotes
    sections = []
    current = ""
    i = 0
    while i < len(content):
        if content[i:i+3] == "'''":
            sections.append(current.strip())
            current = ""
            i += 3
        else:
            current += content[i]
            i += 1
    return sections[:-1]  # Remove last empty section from sentinel

def write_csv(headers, data, output_file):
    """
    Writes the given tabulated data to a CSV file.
    Handles multi-line content within cells.
    """
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Write headers only if they exist
        if headers:
            writer.writerow(headers)
        
        # Process data if it exists
        if data:
            # Clean the data by replacing newlines with spaces in each cell
            cleaned_data = []
            for column in data:
                cleaned_column = []
                for cell in column:
                    # Preserve empty cells but clean non-empty ones
                    cleaned_cell = ' '.join(cell.split()) if cell.strip() else ''
                    cleaned_column.append(cleaned_cell)
                cleaned_data.append(cleaned_column)
            writer.writerows(zip(*cleaned_data))

def tdml_to_csv(tdml_files, output_file):
    """
    Converts multiple TDML files into a single CSV by extracting headers and columns.
    Each file's content is split by triple quotes.
    """
    all_data = []
    headers = []

    for tdml_file in tdml_files:
        try:
            tdml_data = read_tdml(tdml_file)
            if tdml_data:
                # First section is treated as header
                headers.append(tdml_data[0])
                # Rest of the sections form the column data
                all_data.append(tdml_data[1:])
        except Exception as e:
            print(f"Error processing {tdml_file}: {str(e)}")
            continue

    if not all_data:
        print("No valid data found in any of the input files.")
        return

    write_csv(headers, all_data, output_file)

def main():
    parser = argparse.ArgumentParser(description="Convert TDML files to CSV format.")
    parser.add_argument('-o', '--output', default='output.csv', 
                       help="Output CSV file (default: output.csv)")
    parser.add_argument('-p', '--pattern', default='f*.tdml',
                       help="File pattern to match TDML files (default: f*.tdml)")
    args, unknown = parser.parse_known_args()

    tdml_files = sorted(glob.glob(args.pattern))
    if not tdml_files:
        print(f"No TDML files found matching pattern: {args.pattern}")
        return

    tdml_to_csv(tdml_files, args.output)
    print(f"Processed {len(tdml_files)} files")
    print(f"CSV saved as {args.output}")

if __name__ == "__main__":
    main()

