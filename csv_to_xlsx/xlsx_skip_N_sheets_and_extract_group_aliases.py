import pandas as pd
from ipaddress import IPv4Address, AddressValueError
from collections import defaultdict

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
        ip_records = defaultdict(list)  # Track all records by IP
        
        for sheet_name in sheets_to_process:
            print(f"\n📄 Processing sheet: {sheet_name}")
            
            # Read the entire sheet to see what we're working with
            df_full = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=None)
            print(f"   Full sheet dimensions: {df_full.shape[0]} rows x {df_full.shape[1]} columns")
            
            # Read the sheet starting from specified row, using only columns A and B
            df = pd.read_excel(
                excel_file_path, 
                sheet_name=sheet_name, 
                header=None, 
                skiprows=start_row-1,
                usecols='A,B'  # Only read columns A and B
            )
            
            print(f"   Data after skipping rows: {df.shape[0]} rows x {df.shape[1]} columns")
            
            # Process each row
            row_count = 0
            for row_idx, row in df.iterrows():
                actual_row_number = row_idx + start_row  # Calculate actual row number
                row_data = process_row(row, sheet_name, actual_row_number)
                
                if row_data:  # Only add if we found valid data
                    ip_records[row_data['ip_address']].append(row_data)
                    row_count += 1
            
            print(f"   ✅ Found {row_count} valid records in this sheet")
        
        # Consolidate IP records - one entry per IP with aliases combined
        consolidated_data = []
        for ip, records in ip_records.items():
            if records:
                # Use the first record as the main entry
                main_record = records[0].copy()
                
                # Collect aliases from subsequent records
                aliases = []
                for record in records[1:]:
                    aliases.append(record['hostname'])
                
                # Add aliases column
                main_record['aliases'] = ', '.join(aliases) if aliases else ''
                
                consolidated_data.append(main_record)
        
        # Convert to DataFrame for easier handling
        if consolidated_data:
            result_df = pd.DataFrame(consolidated_data)
            
            # Save to CSV if output file specified
            if output_file:
                result_df.to_csv(output_file, index=False)
                print(f"\n💾 Extracted data saved to: {output_file}")
            
            print(f"\n🎉 Total unique IP addresses: {len(consolidated_data)}")
            return result_df
        else:
            print("❌ No valid data found in the specified sheets")
            return pd.DataFrame()
        
    except Exception as e:
        print(f"❌ Error processing Excel file: {e}")
        return pd.DataFrame()

def process_row(row, sheet_name, row_number):
    """
    Process a single row to extract hostname and IP data from columns A and B
    """
    
    # Extract data from columns A (hostname) and B (IP address)
    hostname = str(row[0]).strip() if pd.notna(row[0]) and str(row[0]).strip() != '' else None
    ip_address = str(row[1]).strip() if pd.notna(row[1]) and str(row[1]).strip() != '' else None
    
    # Check if we have both hostname and valid IPv4 address
    if hostname and ip_address and is_valid_ipv4(ip_address):
        return {
            'sheet_name': sheet_name,
            'row_number': row_number,
            'hostname': hostname,
            'ip_address': ip_address
        }
    
    return None

def is_valid_ipv4(ip_string):
    """
    Check if a string is a valid IPv4 address and not a network address
    """
    try:
        ip_obj = IPv4Address(ip_string)
        # Filter out network addresses (like 10.0.0.0, 10.0.1.0) and broadcast addresses
        if ip_string.endswith('.0') or ip_string.endswith('.255'):
            return False
        return True
    except (AddressValueError, ValueError):
        return False

def display_extracted_data(df):
    """
    Display the extracted data in a nice format
    """
    if df.empty:
        print("No data to display")
        return
    
    print("\n" + "="*80)
    print("EXTRACTED DATA SUMMARY")
    print("="*80)
    
    for idx, row in df.iterrows():
        print(f"Record {idx + 1}:")
        print(f"  Sheet: {row['sheet_name']}")
        print(f"  Row: {row['row_number']}")
        print(f"  Hostname: {row['hostname']}")
        print(f"  IP Address: {row['ip_address']}")
        if row['aliases']:
            print(f"  Aliases: {row['aliases']}")
        print()

def analyze_duplicates(df):
    """
    Analyze and display IP addresses with aliases
    """
    if df.empty:
        return
    
    # Find IPs with aliases
    ips_with_aliases = df[df['aliases'] != '']
    
    if not ips_with_aliases.empty:
        print("\n🔍 IP ADDRESSES WITH ALIASES:")
        print("="*50)
        
        for idx, row in ips_with_aliases.iterrows():
            print(f"\nIP Address: {row['ip_address']}")
            print(f"Main Hostname: {row['hostname']}")
            print(f"Aliases: {row['aliases']}")
    else:
        print("\n✅ No IP addresses have aliases")

# Main execution for your specific file
if __name__ == "__main__":
    print("🚀 Excel IP Data Extraction for dummy-.xlsx")
    print("="*50)
    
    # Process your specific file
    excel_file = "dummy-.xlsx"
    
    extracted_data = extract_ip_data(
        excel_file_path=excel_file,
        skip_sheets=4,      # Skip first 4 worksheets (donotuse1, donotuse2, donotuse3, donotuse4)
        start_row=7,        # Start from row 7 (where the actual data begins)
        output_file="extracted_ips.csv"
    )
    
    # Display results
    if not extracted_data.empty:
        display_extracted_data(extracted_data)
        
        # Show summary by sheet
        print("\n📈 SUMMARY BY UNIQUE IP ADDRESSES:")
        summary = extracted_data['sheet_name'].value_counts()
        for sheet, count in summary.items():
            print(f"  {sheet}: {count} unique IPs")
        
        # Analyze aliases
        analyze_duplicates(extracted_data)
        
        # Show total statistics
        total_aliases = extracted_data['aliases'].str.count(',').fillna(0).astype(int) + extracted_data['aliases'].astype(bool).astype(int)
        total_aliases = total_aliases.sum() - len(extracted_data)  # Subtract main hostnames
        print(f"\n📊 TOTAL STATISTICS:")
        print(f"  Unique IP addresses: {len(extracted_data)}")
        print(f"  Total aliases: {total_aliases}")
    else:
        print("No data was extracted.")

    # Let's also show what the raw data looks like for debugging
    print("\n" + "="*50)
    print("DEBUG: RAW DATA INSPECTION")
    print("="*50)
    
    xl_file = pd.ExcelFile(excel_file)
    sheets_to_check = xl_file.sheet_names[4:]  # Skip first 4
    
    for sheet_name in sheets_to_check:
        print(f"\n🔍 Checking raw data in: {sheet_name}")
        df_raw = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
        
        # Show rows 6-15 (around our target area)
        print(f"Rows 6-15 in {sheet_name}:")
        for i in range(5, min(15, len(df_raw))):
            row_data = []
            for j in range(min(6, len(df_raw.columns))):  # First 6 columns
                cell_val = df_raw.iloc[i, j] if pd.notna(df_raw.iloc[i, j]) else ""
                row_data.append(str(cell_val).strip())
            print(f"  Row {i+1}: {row_data}")

"""
🚀 Excel IP Data Extraction for dummy-.xlsx
==================================================
📊 Found 6 sheets: ['donotuse1', 'donotuse2', 'donotuse3', 'donotuse4', 'use1', 'use2']
🔧 Skipping first 4 sheets: ['donotuse1', 'donotuse2', 'donotuse3', 'donotuse4']
🔧 Processing 2 sheets: ['use1', 'use2']
🔧 Starting from row 7 in each sheet
🔧 Using columns: A=Hostname, B=IP Address

📄 Processing sheet: use1
   Full sheet dimensions: 10 rows x 7 columns
   Data after skipping rows: 4 rows x 2 columns
   ✅ Found 2 valid records in this sheet

📄 Processing sheet: use2
   Full sheet dimensions: 12 rows x 7 columns
   Data after skipping rows: 6 rows x 2 columns
   ✅ Found 4 valid records in this sheet

💾 Extracted data saved to: extracted_ips.csv

🎉 Total unique IP addresses: 4

================================================================================
EXTRACTED DATA SUMMARY
================================================================================
Record 1:
  Sheet: use1
  Row: 9
  Hostname: test-server1
  IP Address: 10.0.0.26

Record 2:
  Sheet: use1
  Row: 10
  Hostname: test-server2
  IP Address: 10.0.0.30

Record 3:
  Sheet: use2
  Row: 9
  Hostname: visu1
  IP Address: 10.0.1.2

Record 4:
  Sheet: use2
  Row: 10
  Hostname: gpu1
  IP Address: 10.0.1.3
  Aliases: t1-gpu1, t1-gpu-weak


📈 SUMMARY BY UNIQUE IP ADDRESSES:
  use1: 2 unique IPs
  use2: 2 unique IPs

🔍 IP ADDRESSES WITH ALIASES:
==================================================

IP Address: 10.0.1.3
Main Hostname: gpu1
Aliases: t1-gpu1, t1-gpu-weak

📊 TOTAL STATISTICS:
  Unique IP addresses: 4
  Total aliases: -2

==================================================
DEBUG: RAW DATA INSPECTION
==================================================

🔍 Checking raw data in: use1
Rows 6-15 in use1:
  Row 6: ['Virtual machine name', 'IP', 'Type', 'Cores', 'GRAM', 'GDISK']
  Row 7: ['', '10.0.0.0', '', 'ID', '', '']
  Row 8: ['', '10.0.0.1', 'cisco', 'DEFAULT GATEWAY', '', '']
  Row 9: ['test-server1', '10.0.0.26', 'server', '', '', '']
  Row 10: ['test-server2', '10.0.0.30', 'server', '', '', '']

🔍 Checking raw data in: use2
Rows 6-15 in use2:
  Row 6: ['Virtual machine name', 'IP', 'Type', 'Cores', 'GRAM', 'GDISK']
  Row 7: ['', '10.0.1.0', '', 'ID', '', '']
  Row 8: ['', '10.0.1.1', '', 'DEFAULT GATEWAY', '', '']
  Row 9: ['visu1', '10.0.1.2', 'vm', '', '', '']
  Row 10: ['gpu1', '10.0.1.3', 'vm', '', '', '']
  Row 11: ['t1-gpu1', '10.0.1.3', 'vm', '', '', '']
  Row 12: ['t1-gpu-weak', '10.0.1.3', 'vm', '', '', '']
"""