import pandas as pd
import numpy as np
from ipaddress import ip_address, IPv4Address
import os
import random
import string

def generate_random_hex(length=8):
    """
    Generate a random hexadecimal string
    
    Args:
        length (int): Length of the hex string (default: 8 characters)
    
    Returns:
        str: Random hex string
    """
    return ''.join(random.choices('0123456789ABCDEF', k=length))

def write_hex_to_row(sheet_number, row_number, number_of_columns_to_fill, excel_file_path, start_col=0):
    """
    Write random hex strings to a specific row across multiple columns
    
    Args:
        sheet_number (int): Sheet number (0-based index)
        row_number (int): Row number to write to (1-based index)
        number_of_columns_to_fill (int): Number of columns to fill with hex strings
        excel_file_path (str): Path to the Excel file
        start_col (int): Starting column index (0-based, default: 0 = column A)
    """
    try:
        # Read the Excel file
        xl_file = pd.ExcelFile(excel_file_path)
        sheet_names = xl_file.sheet_names
        
        if sheet_number >= len(sheet_names):
            print(f"❌ Sheet number {sheet_number} doesn't exist. Available sheets: {len(sheet_names)}")
            return False
        
        sheet_name = sheet_names[sheet_number]
        print(f"📝 Writing hex strings to Sheet {sheet_number} ('{sheet_name}'), Row {row_number}, {number_of_columns_to_fill} columns")
        
        # Read the entire sheet
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=None)
        
        # Ensure the DataFrame has enough rows
        while len(df) < row_number:
            df.loc[len(df)] = [None] * len(df.columns) if len(df.columns) > 0 else [None]
        
        # Ensure the DataFrame has enough columns
        required_cols = start_col + number_of_columns_to_fill
        if len(df.columns) < required_cols:
            for i in range(len(df.columns), required_cols):
                df[i] = None
        
        # Generate and write hex strings
        hex_strings = [generate_random_hex() for _ in range(number_of_columns_to_fill)]
        
        for i in range(number_of_columns_to_fill):
            df.iloc[row_number-1, start_col + i] = hex_strings[i]
        
        # Write back to Excel
        with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
        
        print(f"✅ Written hex strings: {hex_strings}")
        return True
        
    except Exception as e:
        print(f"❌ Error writing hex to row: {e}")
        return False

def write_hex_to_column(sheet_number, column_number, number_of_rows_to_fill, excel_file_path, start_row=0):
    """
    Write random hex strings to a specific column across multiple rows
    
    Args:
        sheet_number (int): Sheet number (0-based index)
        column_number (int): Column number to write to (0-based index)
        number_of_rows_to_fill (int): Number of rows to fill with hex strings
        excel_file_path (str): Path to the Excel file
        start_row (int): Starting row index (0-based, default: 0 = first row)
    """
    try:
        # Read the Excel file
        xl_file = pd.ExcelFile(excel_file_path)
        sheet_names = xl_file.sheet_names
        
        if sheet_number >= len(sheet_names):
            print(f"❌ Sheet number {sheet_number} doesn't exist. Available sheets: {len(sheet_names)}")
            return False
        
        sheet_name = sheet_names[sheet_number]
        print(f"📝 Writing hex strings to Sheet {sheet_number} ('{sheet_name}'), Column {column_number}, {number_of_rows_to_fill} rows")
        
        # Read the entire sheet
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=None)
        
        # Ensure the DataFrame has enough columns
        while len(df.columns) <= column_number:
            df[len(df.columns)] = None
        
        # Ensure the DataFrame has enough rows
        required_rows = start_row + number_of_rows_to_fill
        if len(df) < required_rows:
            for i in range(len(df), required_rows):
                df.loc[i] = [None] * len(df.columns)
        
        # Generate and write hex strings
        hex_strings = [generate_random_hex() for _ in range(number_of_rows_to_fill)]
        
        for i in range(number_of_rows_to_fill):
            df.iloc[start_row + i, column_number] = hex_strings[i]
        
        # Write back to Excel
        with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
        
        print(f"✅ Written {number_of_rows_to_fill} hex strings to column {column_number}")
        return True
        
    except Exception as e:
        print(f"❌ Error writing hex to column: {e}")
        return False

def write_hex_to_cell(sheet_number, row_number, column_number, excel_file_path, hex_length=8):
    """
    Write a random hex string to a specific cell
    
    Args:
        sheet_number (int): Sheet number (0-based index)
        row_number (int): Row number (1-based index)
        column_number (int): Column number (0-based index)
        excel_file_path (str): Path to the Excel file
        hex_length (int): Length of hex string (default: 8)
    """
    try:
        # Read the Excel file
        xl_file = pd.ExcelFile(excel_file_path)
        sheet_names = xl_file.sheet_names
        
        if sheet_number >= len(sheet_names):
            print(f"❌ Sheet number {sheet_number} doesn't exist. Available sheets: {len(sheet_names)}")
            return False
        
        sheet_name = sheet_names[sheet_number]
        print(f"📝 Writing hex string to Sheet {sheet_number} ('{sheet_name}'), Cell ({row_number}, {column_number})")
        
        # Read the entire sheet
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=None)
        
        # Ensure the DataFrame has enough rows and columns
        while len(df) < row_number:
            df.loc[len(df)] = [None] * len(df.columns) if len(df.columns) > 0 else [None]
        
        while len(df.columns) <= column_number:
            df[len(df.columns)] = None
        
        # Generate and write hex string
        hex_string = generate_random_hex(hex_length)
        df.iloc[row_number-1, column_number] = hex_string
        
        # Write back to Excel
        with pd.ExcelWriter(excel_file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
        
        print(f"✅ Written hex string '{hex_string}' to cell ({row_number}, {column_number})")
        return True
        
    except Exception as e:
        print(f"❌ Error writing hex to cell: {e}")
        return False

def read_hex_from_row(sheet_number, row_number, number_of_columns_to_read, excel_file_path, start_col=0):
    """
    Read hex strings from a specific row across multiple columns
    
    Args:
        sheet_number (int): Sheet number (0-based index)
        row_number (int): Row number to read from (1-based index)
        number_of_columns_to_read (int): Number of columns to read
        excel_file_path (str): Path to the Excel file
        start_col (int): Starting column index (0-based, default: 0 = column A)
    
    Returns:
        list: List of hex strings found in the specified range
    """
    try:
        # Read the Excel file
        xl_file = pd.ExcelFile(excel_file_path)
        sheet_names = xl_file.sheet_names
        
        if sheet_number >= len(sheet_names):
            print(f"❌ Sheet number {sheet_number} doesn't exist. Available sheets: {len(sheet_names)}")
            return []
        
        sheet_name = sheet_names[sheet_number]
        print(f"📖 Reading hex strings from Sheet {sheet_number} ('{sheet_name}'), Row {row_number}, {number_of_columns_to_read} columns")
        
        # Read the sheet
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=None)
        
        # Check if row exists
        if len(df) < row_number:
            print(f"❌ Row {row_number} doesn't exist in sheet '{sheet_name}'")
            return []
        
        # Check if enough columns exist
        if len(df.columns) < (start_col + number_of_columns_to_read):
            print(f"❌ Not enough columns in sheet '{sheet_name}'")
            return []
        
        # Extract hex strings
        hex_strings = []
        for i in range(number_of_columns_to_read):
            cell_value = df.iloc[row_number-1, start_col + i]
            if pd.notna(cell_value):
                hex_strings.append(str(cell_value))
            else:
                hex_strings.append(None)
        
        print(f"✅ Read hex strings: {hex_strings}")
        return hex_strings
        
    except Exception as e:
        print(f"❌ Error reading hex from row: {e}")
        return []

def read_hex_from_row(sheet_number, row_number, number_of_columns_to_read, excel_file_path, start_col=0):
    """
    Read hex strings from a specific row across multiple columns
    
    Args:
        sheet_number (int): Sheet number (0-based index)
        row_number (int): Row number to read from (1-based index)
        number_of_columns_to_read (int): Number of columns to read
        excel_file_path (str): Path to the Excel file
        start_col (int): Starting column index (0-based, default: 0 = column A)
    
    Returns:
        list: List of hex strings found in the specified range
    """
    try:
        # Read the Excel file
        xl_file = pd.ExcelFile(excel_file_path)
        sheet_names = xl_file.sheet_names
        
        if sheet_number >= len(sheet_names):
            print(f"❌ Sheet number {sheet_number} doesn't exist. Available sheets: {len(sheet_names)}")
            return []
        
        sheet_name = sheet_names[sheet_number]
        print(f"📖 Reading hex strings from Sheet {sheet_number} ('{sheet_name}'), Row {row_number}, {number_of_columns_to_read} columns starting from column {start_col}")
        
        # Read the sheet
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=None)
        
        # Check if row exists
        if len(df) < row_number:
            print(f"❌ Row {row_number} doesn't exist in sheet '{sheet_name}'")
            return []
        
        # Check if enough columns exist
        if len(df.columns) < (start_col + number_of_columns_to_read):
            print(f"❌ Not enough columns in sheet '{sheet_name}'. Available: {len(df.columns)}, Required: {start_col + number_of_columns_to_read}")
            return []
        
        # Extract hex strings
        hex_strings = []
        for i in range(number_of_columns_to_read):
            cell_value = df.iloc[row_number-1, start_col + i]
            if pd.notna(cell_value):
                hex_strings.append(str(cell_value).strip())
            else:
                hex_strings.append(None)
        
        print(f"✅ Read {len([x for x in hex_strings if x is not None])} hex strings: {hex_strings}")
        return hex_strings
        
    except Exception as e:
        print(f"❌ Error reading hex from row: {e}")
        return []

def read_hex_from_column(sheet_number, column_number, number_of_rows_to_read, excel_file_path, start_row=0):
    """
    Read hex strings from a specific column across multiple rows
    
    Args:
        sheet_number (int): Sheet number (0-based index)
        column_number (int): Column number to read from (0-based index)
        number_of_rows_to_read (int): Number of rows to read
        excel_file_path (str): Path to the Excel file
        start_row (int): Starting row index (0-based, default: 0 = first row)
    
    Returns:
        list: List of hex strings found in the specified range
    """
    try:
        # Read the Excel file
        xl_file = pd.ExcelFile(excel_file_path)
        sheet_names = xl_file.sheet_names
        
        if sheet_number >= len(sheet_names):
            print(f"❌ Sheet number {sheet_number} doesn't exist. Available sheets: {len(sheet_names)}")
            return []
        
        sheet_name = sheet_names[sheet_number]
        print(f"📖 Reading hex strings from Sheet {sheet_number} ('{sheet_name}'), Column {column_number}, {number_of_rows_to_read} rows starting from row {start_row}")
        
        # Read the sheet
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=None)
        
        # Check if column exists
        if len(df.columns) <= column_number:
            print(f"❌ Column {column_number} doesn't exist in sheet '{sheet_name}'")
            return []
        
        # Check if enough rows exist
        if len(df) < (start_row + number_of_rows_to_read):
            print(f"❌ Not enough rows in sheet '{sheet_name}'. Available: {len(df)}, Required: {start_row + number_of_rows_to_read}")
            return []
        
        # Extract hex strings
        hex_strings = []
        for i in range(number_of_rows_to_read):
            cell_value = df.iloc[start_row + i, column_number]
            if pd.notna(cell_value):
                hex_strings.append(str(cell_value).strip())
            else:
                hex_strings.append(None)
        
        print(f"✅ Read {len([x for x in hex_strings if x is not None])} hex strings: {hex_strings}")
        return hex_strings
        
    except Exception as e:
        print(f"❌ Error reading hex from column: {e}")
        return []

def read_hex_from_cell(sheet_number, row_number, column_number, excel_file_path):
    """
    Read a hex string from a specific cell
    
    Args:
        sheet_number (int): Sheet number (0-based index)
        row_number (int): Row number to read from (1-based index)
        column_number (int): Column number to read from (0-based index)
        excel_file_path (str): Path to the Excel file
    
    Returns:
        str or None: Hex string if found, None otherwise
    """
    try:
        # Read the Excel file
        xl_file = pd.ExcelFile(excel_file_path)
        sheet_names = xl_file.sheet_names
        
        if sheet_number >= len(sheet_names):
            print(f"❌ Sheet number {sheet_number} doesn't exist. Available sheets: {len(sheet_names)}")
            return None
        
        sheet_name = sheet_names[sheet_number]
        print(f"📖 Reading hex string from Sheet {sheet_number} ('{sheet_name}'), Cell ({row_number}, {column_number})")
        
        # Read the sheet
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=None)
        
        # Check if row exists
        if len(df) < row_number:
            print(f"❌ Row {row_number} doesn't exist in sheet '{sheet_name}'")
            return None
        
        # Check if column exists
        if len(df.columns) <= column_number:
            print(f"❌ Column {column_number} doesn't exist in sheet '{sheet_name}'")
            return None
        
        # Extract hex string
        cell_value = df.iloc[row_number-1, column_number]
        if pd.notna(cell_value):
            hex_string = str(cell_value).strip()
            print(f"✅ Read hex string: '{hex_string}'")
            return hex_string
        else:
            print(f"ℹ️  Cell ({row_number}, {column_number}) is empty")
            return None
        
    except Exception as e:
        print(f"❌ Error reading hex from cell: {e}")
        return None

def read_hex_from_row_range(sheet_number, row_number, start_col, end_col, excel_file_path):
    """
    Read hex strings from a specific row within a column range
    
    Args:
        sheet_number (int): Sheet number (0-based index)
        row_number (int): Row number to read from (1-based index)
        start_col (int): Starting column index (0-based)
        end_col (int): Ending column index (0-based, inclusive)
        excel_file_path (str): Path to the Excel file
    
    Returns:
        list: List of hex strings found in the specified range
    """
    number_of_columns = end_col - start_col + 1
    return read_hex_from_row(sheet_number, row_number, number_of_columns, excel_file_path, start_col)

def read_hex_from_column_range(sheet_number, column_number, start_row, end_row, excel_file_path):
    """
    Read hex strings from a specific column within a row range
    
    Args:
        sheet_number (int): Sheet number (0-based index)
        column_number (int): Column number to read from (0-based index)
        start_row (int): Starting row index (0-based)
        end_row (int): Ending row index (0-based, inclusive)
        excel_file_path (str): Path to the Excel file
    
    Returns:
        list: List of hex strings found in the specified range
    """
    number_of_rows = end_row - start_row + 1
    return read_hex_from_column(sheet_number, column_number, number_of_rows, excel_file_path, start_row)

def extract_ip_data(excel_file_path, skip_sheets=4, start_row=7, output_file=None):
    """
    Extract IP data from Excel file, skipping first N worksheets and starting from specific row
    
    Args:
        excel_file_path (str): Path to the Excel file
        skip_sheets (int): Number of worksheets to skip from beginning
        start_row (int): Row number to start processing from (1-based)
        output_file (str): Path to save extracted data
    """
    
    try:
        # Read the Excel file
        xl_file = pd.ExcelFile(excel_file_path)
        sheet_names = xl_file.sheet_names
        
        print(f"📊 Found {len(sheet_names)} sheets: {sheet_names}")
        
        # Skip first N worksheets
        sheets_to_process = sheet_names[skip_sheets:]
        
        print(f"🔧 Skipping first {skip_sheets} sheets: {sheet_names[:skip_sheets]}")
        print(f"🔧 Processing {len(sheets_to_process)} sheets: {sheets_to_process}")
        print(f"🔧 Starting from row {start_row} in each sheet")
        print(f"🔧 Using columns: A=Hostname, B=IP Address")
        
        all_ip_data = []
        
        for sheet_name in sheets_to_process:
            print(f"\n📄 Processing sheet: {sheet_name}")
            
            # Read the sheet, skipping rows (start_row-1 because skiprows is 0-based)
            # Use only columns A and B
            df = pd.read_excel(
                excel_file_path, 
                sheet_name=sheet_name, 
                header=None, 
                skiprows=start_row-1,
                usecols='A,B'  # Only read columns A and B
            )
            
            print(f"   Sheet dimensions: {df.shape[0]} rows x {df.shape[1]} columns")
            
            # Process each row
            row_count = 0
            for row_idx, row in df.iterrows():
                actual_row_number = row_idx + start_row  # Calculate actual row number
                row_data = process_row(row, sheet_name, actual_row_number)
                
                if row_data:  # Only add if we found valid IPv4 data
                    all_ip_data.append(row_data)
                    row_count += 1
            
            print(f"   ✅ Found {row_count} IPv4 records in this sheet")
        
        # Convert to DataFrame for easier handling
        if all_ip_data:
            result_df = pd.DataFrame(all_ip_data)
            
            # Save to CSV if output file specified
            if output_file:
                result_df.to_csv(output_file, index=False)
                print(f"\n💾 Extracted data saved to: {output_file}")
            
            print(f"\n🎉 Total IPv4 records extracted: {len(all_ip_data)}")
            return result_df
        else:
            print("❌ No IPv4 data found in the specified sheets")
            return pd.DataFrame()
        
    except Exception as e:
        print(f"❌ Error processing Excel file: {e}")
        return pd.DataFrame()

def process_row(row, sheet_name, row_number):
    """
    Process a single row to extract hostname and IPv4 data from columns A and B
    """
    
    # Extract data from columns A (hostname) and B (IP address)
    hostname = str(row[0]).strip() if pd.notna(row[0]) else ''
    ip_address = str(row[1]).strip() if pd.notna(row[1]) else ''
    
    # Check if we have valid IPv4 address
    if ip_address and is_valid_ipv4(ip_address):
        return {
            'sheet_name': sheet_name,
            'row_number': row_number,
            'hostname': hostname,
            'ip_address': ip_address
        }
    
    return None

def is_valid_ipv4(ip_string):
    """
    Check if a string is a valid IPv4 address
    """
    try:
        ip_obj = ip_address(ip_string)
        return isinstance(ip_obj, IPv4Address)
    except ValueError:
        return False

# test data file creation
def create_sample_excel_file(filename=None, sheet_configs=None, num_dummy_sheets=4):
    """
    Create a sample Excel file with configurable sheets and data
    
    Args:
        filename (str): Output filename (default: 'sample_network_data.xlsx')
        sheet_configs (list): List of dictionaries defining sheet configurations
        num_dummy_sheets (int): Number of dummy sheets to create before data sheets
    
    Returns:
        str: Path to the created Excel file
    """
    
    # Default filename
    if filename is None:
        filename = 'sample_network_data.xlsx'
    
    # Default sheet configurations for network data
    if sheet_configs is None:
        sheet_configs = [
            {
                'name': 'Network_A',
                'title': 'NETWORK A - SERVER IPS',
                'date': '2024-01-15',
                'location': 'Data Center A',
                'headers': ['Hostname', 'IP Address', 'Status', 'Description'],
                'data': [
                    ['router-dc1', '192.168.1.1', 'Active', 'Main router'],
                    ['server-web1', '192.168.1.10', 'Active', 'Web server'],
                    ['server-db1', '10.0.0.5', 'Active', 'Database server'],
                    ['server-app1', '172.16.0.100', 'Maintenance', 'Application server'],
                    ['server-backup1', '192.168.1.50', 'Active', 'Backup server'],
                    ['router-ipv6', '2001:db8::1', 'Active', 'IPv6 router']
                ],
                'empty_rows_before': 2,
                'empty_rows_after': 1
            },
            {
                'name': 'Network_B',
                'title': 'NETWORK B - OFFICE IPS',
                'date': '2024-01-15',
                'location': 'Office B',
                'headers': ['Hostname', 'IP Address', 'Status', 'Description'],
                'data': [
                    ['router-office1', '192.168.2.1', 'Active', 'Office router'],
                    ['pc-user1', '192.168.2.100', 'Active', 'User workstation'],
                    ['pc-user2', '192.168.2.101', 'Inactive', 'Old workstation'],
                    ['printer1', '192.168.2.200', 'Active', 'Network printer'],
                    ['server-files', '10.1.1.5', 'Active', 'File server']
                ],
                'empty_rows_before': 2,
                'empty_rows_after': 0
            },
            {
                'name': 'Network_C',
                'title': 'NETWORK C - DMZ IPS',
                'date': '2024-01-15',
                'location': 'DMZ',
                'headers': ['Hostname', 'IP Address', 'Status', 'Description'],
                'data': [
                    ['web-external1', '203.0.113.10', 'Active', 'Public web server'],
                    ['web-external2', '203.0.113.11', 'Active', 'Public web server'],
                    ['mail-server', '198.51.100.5', 'Active', 'Mail server'],
                    ['vpn-gateway', '192.0.2.100', 'Active', 'VPN gateway']
                ],
                'empty_rows_before': 2,
                'empty_rows_after': 0
            }
        ]
    
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            
            # Create dummy sheets (Cover, Summary, TOC, Instructions, etc.)
            dummy_sheets = [
                {
                    'name': 'Cover',
                    'data': [
                        ['COVER PAGE', '', ''],
                        ['Company Confidential', '', ''],
                        ['IP Address Report', '', ''],
                        ['', '', ''],
                        ['Created: 2024-01-15', 'Version: 1.0', 'Author: System']
                    ]
                },
                {
                    'name': 'Summary',
                    'data': [
                        ['SUMMARY', '', ''],
                        ['Total IPs: 150', 'IPv4: 120', 'IPv6: 30'],
                        ['Active: 100', 'Inactive: 20', 'Maintenance: 30'],
                        ['', '', ''],
                        ['Networks: 3', 'Sheets: 7', 'Last Updated: 2024-01-15']
                    ]
                },
                {
                    'name': 'TOC',
                    'data': [
                        ['TABLE OF CONTENTS', '', ''],
                        ['Cover Page - Page 1', 'Summary - Page 2', 'TOC - Page 3'],
                        ['Instructions - Page 4', 'Network A - Page 5', 'Network B - Page 6'],
                        ['Network C - Page 7', '', '']
                    ]
                },
                {
                    'name': 'Instructions',
                    'data': [
                        ['INSTRUCTIONS', '', ''],
                        ['Step 1: Review all network data', 'Step 2: Validate IP addresses', ''],
                        ['Step 3: Update as needed', 'Step 4: Save changes', ''],
                        ['', '', ''],
                        ['Notes:', '', ''],
                        ['- IPv4 addresses only', '- Report any discrepancies', '']
                    ]
                }
            ]
            
            # Create only the requested number of dummy sheets
            for i in range(min(num_dummy_sheets, len(dummy_sheets))):
                sheet_data = dummy_sheets[i]
                df = pd.DataFrame(sheet_data['data'])
                df.to_excel(writer, sheet_name=sheet_data['name'], index=False, header=False)
                print(f"✅ Created dummy sheet: {sheet_data['name']}")
            
            # Create data sheets based on configurations
            for config in sheet_configs:
                sheet_data = create_sheet_data(config)
                df = pd.DataFrame(sheet_data)
                df.to_excel(writer, sheet_name=config['name'], index=False, header=False)
                print(f"✅ Created data sheet: {config['name']} with {len(config['data'])} records")
        
        print(f"✅ Sample Excel file created: '{filename}'")
        print(f"✅ Total sheets: {num_dummy_sheets + len(sheet_configs)}")
        return filename
        
    except Exception as e:
        print(f"❌ Error creating sample Excel file: {e}")
        return None

def create_sheet_data(config):
    """
    Create sheet data based on configuration
    
    Args:
        config (dict): Sheet configuration
        
    Returns:
        list: 2D list representing sheet data
    """
    sheet_data = []
    
    # Add empty rows at the beginning
    for _ in range(config.get('empty_rows_before', 2)):
        sheet_data.append([''] * 4)
    
    # Add title row
    sheet_data.append([config.get('title', 'NETWORK DATA'), '', '', ''])
    
    # Add empty row after title
    sheet_data.append([''] * 4)
    
    # Add date and location
    sheet_data.append([
        f"Date: {config.get('date', '2024-01-15')}",
        f"Location: {config.get('location', 'Unknown')}",
        '', ''
    ])
    
    # Add headers
    sheet_data.append(config.get('headers', ['Hostname', 'IP Address', 'Status', 'Description']))
    
    # Add data rows
    for row in config.get('data', []):
        sheet_data.append(row)
    
    # Add empty rows at the end
    for _ in range(config.get('empty_rows_after', 0)):
        sheet_data.append([''] * 4)
    
    return sheet_data

# Example usage with different configurations
def create_custom_sample_files():
    """Demonstrate different ways to use the generic create_sample_excel_file()"""
    
    print("🚀 Creating Custom Sample Files")
    print("="*50)
    
    # Example 1: Default network data (same as original)
    print("\n1. Creating default network data file...")
    create_sample_excel_file()
    
    # Example 2: Custom filename and fewer dummy sheets
    print("\n2. Creating custom file with 2 dummy sheets...")
    create_sample_excel_file(
        filename='custom_network_data.xlsx',
        num_dummy_sheets=2
    )
    
    # Example 3: Completely custom sheet configuration
    print("\n3. Creating file with custom sheet configuration...")
    
    custom_config = [
        {
            'name': 'Devices',
            'title': 'DEVICE INVENTORY',
            'date': '2024-01-20',
            'location': 'Headquarters',
            'headers': ['Device Name', 'MAC Address', 'Type', 'Location', 'Owner'],
            'data': [
                ['laptop-john', '00:1B:44:11:3A:B7', 'Laptop', 'Floor 3', 'John Doe'],
                ['desktop-sara', '00:1B:44:11:3A:B8', 'Desktop', 'Floor 2', 'Sara Smith'],
                ['phone-conf', '00:1B:44:11:3A:B9', 'VOIP Phone', 'Conference Room', 'IT Dept'],
                ['printer-mkt', '00:1B:44:11:3A:BA', 'Printer', 'Marketing', 'Team MKT']
            ],
            'empty_rows_before': 1,
            'empty_rows_after': 2
        },
        {
            'name': 'Servers',
            'title': 'SERVER FARM',
            'date': '2024-01-20',
            'location': 'Data Center West',
            'headers': ['Hostname', 'IP Address', 'CPU', 'RAM', 'Storage'],
            'data': [
                ['web-srv-01', '10.10.1.10', '8 cores', '32GB', '500GB SSD'],
                ['db-srv-01', '10.10.1.20', '16 cores', '64GB', '1TB SSD'],
                ['app-srv-01', '10.10.1.30', '12 cores', '48GB', '750GB SSD'],
                ['file-srv-01', '10.10.1.40', '8 cores', '32GB', '2TB HDD']
            ],
            'empty_rows_before': 1,
            'empty_rows_after': 1
        }
    ]
    
    create_sample_excel_file(
        filename='device_inventory.xlsx',
        sheet_configs=custom_config,
        num_dummy_sheets=3
    )
    
    # Example 4: Minimal configuration
    print("\n4. Creating minimal file...")
    minimal_config = [
        {
            'name': 'SimpleData',
            'data': [
                ['Item1', 'Value1'],
                ['Item2', 'Value2'],
                ['Item3', 'Value3']
            ]
        }
    ]
    
    create_sample_excel_file(
        filename='minimal_data.xlsx',
        sheet_configs=minimal_config,
        num_dummy_sheets=0
    )

def display_extracted_data(df):
    """
    Display the extracted data in a nice format
    """
    if df.empty:
        print("No data to display")
        return
    
    print("\n" + "="*80)
    print("EXTRACTED IP DATA SUMMARY")
    print("="*80)
    
    for idx, row in df.iterrows():
        print(f"Record {idx + 1}:")
        print(f"  Sheet: {row['sheet_name']}")
        print(f"  Row: {row['row_number']}")
        print(f"  Hostname: {row['hostname']}")
        print(f"  IP Address: {row['ip_address']}")
        print()
        
# Enhanced main execution to demonstrate all read functions
if __name__ == "__main__":
    print("🚀 Excel Hex String Operations Demo")
    print("="*50)
    
    # Step 1: Create sample Excel file
    excel_file = create_sample_excel_file()
    
    # Step 2: Demonstrate hex writing functions first
    print("\n" + "="*50)
    print("Testing Hex Writing Functions")
    print("="*50)
    
    # Write some test data to read later
    write_hex_to_row(4, 15, 4, excel_file)  # Sheet 4, Row 15, 4 columns
    write_hex_to_column(4, 4, 5, excel_file)  # Sheet 4, Column 4, 5 rows
    write_hex_to_cell(4, 20, 3, excel_file)  # Sheet 4, Row 20, Column 3
    
    # Step 3: Demonstrate all hex reading functions
    print("\n" + "="*50)
    print("Testing Hex Reading Functions")
    print("="*50)
    
    # Read from row
    print("\n1. Reading from row:")
    row_data = read_hex_from_row(4, 15, 4, excel_file)
    
    # Read from column
    print("\n2. Reading from column:")
    col_data = read_hex_from_column(4, 4, 5, excel_file)
    
    # Read from specific cell
    print("\n3. Reading from specific cell:")
    cell_data = read_hex_from_cell(4, 20, 3, excel_file)
    
    # Read from row range
    print("\n4. Reading from row range:")
    row_range_data = read_hex_from_row_range(4, 15, 0, 2, excel_file)  # Columns 0-2
    
    # Read from column range
    print("\n5. Reading from column range:")
    col_range_data = read_hex_from_column_range(4, 4, 0, 2, excel_file)  # Rows 0-2
    
    # Step 4: Test error cases
    print("\n" + "="*50)
    print("Testing Error Cases")
    print("="*50)
    
    # Non-existent sheet
    print("\n6. Reading from non-existent sheet:")
    invalid_sheet = read_hex_from_row(9, 1, 3, excel_file)
    
    # Non-existent row
    print("\n7. Reading from non-existent row:")
    invalid_row = read_hex_from_row(4, 99, 3, excel_file)
    
    # Non-existent column
    print("\n8. Reading from non-existent column:")
    invalid_col = read_hex_from_column(4, 9, 3, excel_file)
    
    # Step 5: Original IP extraction (for reference)
    print("\n" + "="*50)
    print("Original IP Data Extraction")
    print("="*50)
    
    extracted_data = extract_ip_data(
        excel_file_path=excel_file,
        skip_sheets=4,
        start_row=7,
        output_file="extracted_ips.csv"
    )
    
    if not extracted_data.empty:
        display_extracted_data(extracted_data)


"""
🚀 Excel Hex String Operations Demo
==================================================
✅ Created dummy sheet: Cover
✅ Created dummy sheet: Summary
✅ Created dummy sheet: TOC
✅ Created dummy sheet: Instructions
✅ Created data sheet: Network_A with 6 records
✅ Created data sheet: Network_B with 5 records
✅ Created data sheet: Network_C with 4 records
✅ Sample Excel file created: 'sample_network_data.xlsx'
✅ Total sheets: 7

==================================================
Testing Hex Writing Functions
==================================================
📝 Writing hex strings to Sheet 4 ('Network_A'), Row 15, 4 columns
✅ Written hex strings: ['DC045926', '4D9DC046', '3140EFD8', '3EEC7095']
📝 Writing hex strings to Sheet 4 ('Network_A'), Column 4, 5 rows
✅ Written 5 hex strings to column 4
📝 Writing hex string to Sheet 4 ('Network_A'), Cell (20, 3)
✅ Written hex string '5D23CA80' to cell (20, 3)

==================================================
Testing Hex Reading Functions
==================================================

1. Reading from row:
📖 Reading hex strings from Sheet 4 ('Network_A'), Row 15, 4 columns starting from column 0
✅ Read 4 hex strings: ['DC045926', '4D9DC046', '3140EFD8', '3EEC7095']

2. Reading from column:
📖 Reading hex strings from Sheet 4 ('Network_A'), Column 4, 5 rows starting from row 0
✅ Read 5 hex strings: ['6B72D9C5', '38C227B5', '7C40BD86', '3405F561', '4C77C413']

3. Reading from specific cell:
📖 Reading hex string from Sheet 4 ('Network_A'), Cell (20, 3)
✅ Read hex string: '5D23CA80'

4. Reading from row range:
📖 Reading hex strings from Sheet 4 ('Network_A'), Row 15, 3 columns starting from column 0
✅ Read 3 hex strings: ['DC045926', '4D9DC046', '3140EFD8']

5. Reading from column range:
📖 Reading hex strings from Sheet 4 ('Network_A'), Column 4, 3 rows starting from row 0
✅ Read 3 hex strings: ['6B72D9C5', '38C227B5', '7C40BD86']

==================================================
Testing Error Cases
==================================================

6. Reading from non-existent sheet:
❌ Sheet number 9 doesn't exist. Available sheets: 7

7. Reading from non-existent row:
📖 Reading hex strings from Sheet 4 ('Network_A'), Row 99, 3 columns starting from column 0
❌ Row 99 doesn't exist in sheet 'Network_A'

8. Reading from non-existent column:
📖 Reading hex strings from Sheet 4 ('Network_A'), Column 9, 3 rows starting from row 0
❌ Column 9 doesn't exist in sheet 'Network_A'

==================================================
Original IP Data Extraction
==================================================
📊 Found 7 sheets: ['Cover', 'Summary', 'TOC', 'Instructions', 'Network_A', 'Network_B', 'Network_C']
🔧 Skipping first 4 sheets: ['Cover', 'Summary', 'TOC', 'Instructions']
🔧 Processing 3 sheets: ['Network_A', 'Network_B', 'Network_C']
🔧 Starting from row 7 in each sheet
🔧 Using columns: A=Hostname, B=IP Address

📄 Processing sheet: Network_A
   Sheet dimensions: 14 rows x 2 columns
   ✅ Found 5 IPv4 records in this sheet

📄 Processing sheet: Network_B
   Sheet dimensions: 5 rows x 2 columns
   ✅ Found 5 IPv4 records in this sheet

📄 Processing sheet: Network_C
   Sheet dimensions: 4 rows x 2 columns
   ✅ Found 4 IPv4 records in this sheet

💾 Extracted data saved to: extracted_ips.csv

🎉 Total IPv4 records extracted: 14

================================================================================
EXTRACTED IP DATA SUMMARY
================================================================================
Record 1:
  Sheet: Network_A
  Row: 7
  Hostname: router-dc1
  IP Address: 192.168.1.1

Record 2:
  Sheet: Network_A
  Row: 8
  Hostname: server-web1
  IP Address: 192.168.1.10

Record 3:
  Sheet: Network_A
  Row: 9
  Hostname: server-db1
  IP Address: 10.0.0.5

Record 4:
  Sheet: Network_A
  Row: 10
  Hostname: server-app1
  IP Address: 172.16.0.100

Record 5:
  Sheet: Network_A
  Row: 11
  Hostname: server-backup1
  IP Address: 192.168.1.50

Record 6:
  Sheet: Network_B
  Row: 7
  Hostname: router-office1
  IP Address: 192.168.2.1

Record 7:
  Sheet: Network_B
  Row: 8
  Hostname: pc-user1
  IP Address: 192.168.2.100

Record 8:
  Sheet: Network_B
  Row: 9
  Hostname: pc-user2
  IP Address: 192.168.2.101

Record 9:
  Sheet: Network_B
  Row: 10
  Hostname: printer1
  IP Address: 192.168.2.200

Record 10:
  Sheet: Network_B
  Row: 11
  Hostname: server-files
  IP Address: 10.1.1.5

Record 11:
  Sheet: Network_C
  Row: 7
  Hostname: web-external1
  IP Address: 203.0.113.10

Record 12:
  Sheet: Network_C
  Row: 8
  Hostname: web-external2
  IP Address: 203.0.113.11

Record 13:
  Sheet: Network_C
  Row: 9
  Hostname: mail-server
  IP Address: 198.51.100.5

Record 14:
  Sheet: Network_C
  Row: 10
  Hostname: vpn-gateway
  IP Address: 192.0.2.100


"""