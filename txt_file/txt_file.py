import os
import random
import time
from datetime import datetime

def generate_random_hex(length=32):
    """Generate random hexadecimal string"""
    return ''.join(random.choices('0123456789abcdef', k=length))

def read_file_lines(filename):
    """Read all lines from a file"""
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        return f.readlines()

def write_file_lines(filename, lines):
    """Write lines to a file"""
    with open(filename, 'w') as f:
        f.writelines(lines)

def initialize_random_file():
    """Initialize random.txt with some random hex lines"""
    lines = [generate_random_hex() + '\n' for _ in range(10)]
    write_file_lines('random.txt', lines)
    print("Initialized random.txt with 10 random hex lines")

def delete_lines(input_file, line_numbers, output_file=None):
    """
    Delete lines from file given a list of line numbers
    Line numbers are 1-indexed
    """
    lines = read_file_lines(input_file)
    
    # Convert to set for faster lookup and remove duplicates
    line_numbers = set(line_numbers)
    
    # Check if all line numbers exist
    max_line = len(lines)
    invalid_lines = [ln for ln in line_numbers if ln < 1 or ln > max_line]
    
    if invalid_lines:
        print(f"Error: Line numbers {invalid_lines} do not exist. File has {max_line} lines.")
        return None
    
    # Delete lines (convert to 0-indexed and sort in reverse to avoid index issues)
    lines_to_delete = sorted(line_numbers, reverse=True)
    for line_num in lines_to_delete:
        del lines[line_num - 1]
    
    # Create output filename with timestamp if not provided
    if output_file is None:
        timestamp = int(time.time() * 1000)
        output_file = f'random.{timestamp}.txt'
    
    write_file_lines(output_file, lines)
    print(f"Deleted lines {sorted(line_numbers)}. Output: {output_file}")
    return output_file

def insert_lines(input_file, line_numbers, output_file=None):
    """
    Insert random hex lines at specified line numbers
    Line numbers are 1-indexed (inserts before the specified line)
    """
    lines = read_file_lines(input_file)
    
    # Check if all line numbers exist
    max_line = len(lines) + 1  # Can insert after last line
    invalid_lines = [ln for ln in line_numbers if ln < 1 or ln > max_line]
    
    if invalid_lines:
        print(f"Error: Line numbers {invalid_lines} are invalid. Can only insert between 1 and {max_line}.")
        return None
    
    # Sort line numbers in reverse order to maintain correct indices during insertion
    lines_to_insert = sorted(line_numbers, reverse=True)
    
    for line_num in lines_to_insert:
        new_line = generate_random_hex() + '\n'
        lines.insert(line_num - 1, new_line)
    
    # Create output filename with timestamp if not provided
    if output_file is None:
        timestamp = int(time.time() * 1000)
        output_file = f'random.{timestamp}.txt'
    
    write_file_lines(output_file, lines)
    print(f"Inserted random hex at lines {sorted(line_numbers)}. Output: {output_file}")
    return output_file

def update_lines(input_file, line_numbers, output_file=None):
    """
    Update (replace) lines with random hex at specified line numbers
    Line numbers are 1-indexed
    """
    lines = read_file_lines(input_file)
    
    # Check if all line numbers exist
    max_line = len(lines)
    invalid_lines = [ln for ln in line_numbers if ln < 1 or ln > max_line]
    
    if invalid_lines:
        print(f"Error: Line numbers {invalid_lines} do not exist. File has {max_line} lines.")
        return None
    
    # Update lines
    for line_num in line_numbers:
        new_line = generate_random_hex() + '\n'
        lines[line_num - 1] = new_line
    
    # Create output filename with timestamp if not provided
    if output_file is None:
        timestamp = int(time.time() * 1000)
        output_file = f'random.{timestamp}.txt'
    
    write_file_lines(output_file, lines)
    print(f"Updated lines {sorted(line_numbers)} with random hex. Output: {output_file}")
    return output_file

def display_file(filename):
    """Display file contents with line numbers"""
    if not os.path.exists(filename):
        print(f"File {filename} does not exist")
        return
    
    lines = read_file_lines(filename)
    print(f"\nContents of {filename}:")
    for i, line in enumerate(lines, 1):
        print(f"{i:3}: {line.strip()}")

# Example usage and demonstration
if __name__ == "__main__":
    # Initialize the random file if it doesn't exist
    if not os.path.exists('random.txt'):
        initialize_random_file()
    
    # Display original file
    print("=" * 50)
    display_file('random.txt')
    
    # Test operations in sequence, passing the output of one as input to the next
    current_file = 'random.txt'
    
    # Test delete function
    print("\n" + "=" * 50)
    print("Testing DELETE function...")
    current_file = delete_lines(current_file, [2, 5, 8])
    if current_file:
        display_file(current_file)
    
    # Test insert function on the result of delete
    print("\n" + "=" * 50)
    print("Testing INSERT function...")
    current_file = insert_lines(current_file, [1, 3, 6])  # Now using correct line numbers for the current file
    if current_file:
        display_file(current_file)
    
    # Test update function on the result of insert
    print("\n" + "=" * 50)
    print("Testing UPDATE function...")
    current_file = update_lines(current_file, [1, 4, 7])  # Using correct line numbers for the current file
    if current_file:
        display_file(current_file)
"""
Features:
delete_lines(line_numbers): Deletes specified lines (1-indexed) and validates they exist
insert_lines(line_numbers): Inserts random hex lines at specified positions (1-indexed)
update_lines(line_numbers): Replaces specified lines with random hex and validates they exist

==================================================

Contents of random.txt:
  1: 9f952356a0e2d196237f6846a0c06f10
  2: 7c7ea104f5bf86e0228bc8245a363fe4
  3: 4bddf33d0107fa96af23558aff2e1102
  4: 39aa09d5d24499ecfd8e87ca986f9854
  5: a37b9e14f864ac145d4aca4e0bb7dd4a
  6: 9ee6368b7fa02ff97da8085c1ca1c821
  7: 4e72dc3f4bdd4d47e52e1edbb9693c47
  8: 7ca9e7e07c359aa7a60b25a603f159ce
  9: 0dcd4befcac2f28ea20f67e402ec8d24
 10: ac398a76c819642c8feaa6f3ccb9acce

==================================================
Testing DELETE function...
Deleted lines [2, 5, 8]. Output: random.1763927829402.txt

Contents of random.1763927829402.txt:
  1: 9f952356a0e2d196237f6846a0c06f10
  2: 4bddf33d0107fa96af23558aff2e1102
  3: 39aa09d5d24499ecfd8e87ca986f9854
  4: 9ee6368b7fa02ff97da8085c1ca1c821
  5: 4e72dc3f4bdd4d47e52e1edbb9693c47
  6: 0dcd4befcac2f28ea20f67e402ec8d24
  7: ac398a76c819642c8feaa6f3ccb9acce

==================================================
Testing INSERT function...
Inserted random hex at lines [1, 3, 6]. Output: random.1763927829403.txt

Contents of random.1763927829403.txt:
  1: 9a8c19faff0fa7b8529ff0e236b470bc
  2: 9f952356a0e2d196237f6846a0c06f10
  3: 4bddf33d0107fa96af23558aff2e1102
  4: 56ff80d8e7573e5931133b2af5f6d286
  5: 39aa09d5d24499ecfd8e87ca986f9854
  6: 9ee6368b7fa02ff97da8085c1ca1c821
  7: 4e72dc3f4bdd4d47e52e1edbb9693c47
  8: 07be073d0fd16248f512ea3db3fdfdda
  9: 0dcd4befcac2f28ea20f67e402ec8d24
 10: ac398a76c819642c8feaa6f3ccb9acce

==================================================
Testing UPDATE function...
Updated lines [1, 4, 7] with random hex. Output: random.1763927829405.txt

Contents of random.1763927829405.txt:
  1: 84f3e49ff3065e11376e6782df67f773
  2: 9f952356a0e2d196237f6846a0c06f10
  3: 4bddf33d0107fa96af23558aff2e1102
  4: d6b0549c30ccec130749304aa3568267
  5: 39aa09d5d24499ecfd8e87ca986f9854
  6: 9ee6368b7fa02ff97da8085c1ca1c821
  7: e860f0e3e87c2919482c7bf7cd7c48e3
  8: 07be073d0fd16248f512ea3db3fdfdda
  9: 0dcd4befcac2f28ea20f67e402ec8d24
 10: ac398a76c819642c8feaa6f3ccb9acce

"""