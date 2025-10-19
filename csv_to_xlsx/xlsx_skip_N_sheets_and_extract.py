import pandas as pd
import numpy as np
from ipaddress import ip_address, IPv4Address
import os

def create_sample_excel_file():
    """Create a sample Excel file with multiple sheets"""
    
    # Create sample data for multiple sheets
    with pd.ExcelWriter('sample_network_data.xlsx', engine='openpyxl') as writer:
        
        # First 4 sheets (will be skipped)
        cover_data = pd.DataFrame({
            'A': ['COVER PAGE', 'Company Confidential', 'IP Address Report'],
            'B': ['', '', ''],
            'C': ['', '', '']
        })
        cover_data.to_excel(writer, sheet_name='Cover', index=False)
        
        summary_data = pd.DataFrame({
            'A': ['SUMMARY', 'Total IPs: 150', 'IPv4: 120'],
            'B': ['', '', ''],
            'C': ['', '', '']
        })
        summary_data.to_excel(writer, sheet_name='Summary', index=False)
        
        toc_data = pd.DataFrame({
            'A': ['TABLE OF CONTENTS', 'Network A - Page 1', 'Network B - Page 2'],
            'B': ['', '', ''],
            'C': ['', '', '']
        })
        toc_data.to_excel(writer, sheet_name='TOC', index=False)
        
        instructions_data = pd.DataFrame({
            'A': ['INSTRUCTIONS', 'Step 1: Review', 'Step 2: Validate'],
            'B': ['', '', ''],
            'C': ['', '', '']
        })
        instructions_data.to_excel(writer, sheet_name='Instructions', index=False)
        
        # Sheets we actually want to process (starting from sheet 5)
        # Network A data starting at row 7
        network_a_data = [
            # Rows 1-6 (will be skipped)
            ['', '', '', ''],
            ['', '', '', ''],
            ['NETWORK A - SERVER IPS', '', '', ''],
            ['', '', '', ''],
            ['Date: 2024-01-15', 'Location: Data Center A', '', ''],
            ['Hostname', 'IP Address', 'Status', 'Description'],  # Column headers
            # Rows 7+ (actual data)
            ['router-dc1', '192.168.1.1', 'Active', 'Main router'],
            ['server-web1', '192.168.1.10', 'Active', 'Web server'],
            ['server-db1', '10.0.0.5', 'Active', 'Database server'],
            ['server-app1', '172.16.0.100', 'Maintenance', 'Application server'],
            ['server-backup1', '192.168.1.50', 'Active', 'Backup server'],
            ['', '', '', ''],
            ['router-ipv6', '2001:db8::1', 'Active', 'IPv6 router']  # This will be filtered out (IPv6)
        ]
        pd.DataFrame(network_a_data).to_excel(writer, sheet_name='Network_A', index=False, header=False)
        
        # Network B data
        network_b_data = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['NETWORK B - OFFICE IPS', '', '', ''],
            ['', '', '', ''],
            ['Date: 2024-01-15', 'Location: Office B', '', ''],
            ['Hostname', 'IP Address', 'Status', 'Description'],
            ['router-office1', '192.168.2.1', 'Active', 'Office router'],
            ['pc-user1', '192.168.2.100', 'Active', 'User workstation'],
            ['pc-user2', '192.168.2.101', 'Inactive', 'Old workstation'],
            ['printer1', '192.168.2.200', 'Active', 'Network printer'],
            ['server-files', '10.1.1.5', 'Active', 'File server']
        ]
        pd.DataFrame(network_b_data).to_excel(writer, sheet_name='Network_B', index=False, header=False)
        
        # Network C data
        network_c_data = [
            ['', '', '', ''],
            ['', '', '', ''],
            ['NETWORK C - DMZ IPS', '', '', ''],
            ['', '', '', ''],
            ['Date: 2024-01-15', 'Location: DMZ', '', ''],
            ['Hostname', 'IP Address', 'Status', 'Description'],
            ['web-external1', '203.0.113.10', 'Active', 'Public web server'],
            ['web-external2', '203.0.113.11', 'Active', 'Public web server'],
            ['mail-server', '198.51.100.5', 'Active', 'Mail server'],
            ['vpn-gateway', '192.0.2.100', 'Active', 'VPN gateway']
        ]
        pd.DataFrame(network_c_data).to_excel(writer, sheet_name='Network_C', index=False, header=False)
    
    print("✅ Sample Excel file created: 'sample_network_data.xlsx'")
    return 'sample_network_data.xlsx'

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

# Main execution
if __name__ == "__main__":
    print("🚀 Excel IP Data Extraction Demo")
    print("="*50)
    
    # Step 1: Create sample Excel file
    excel_file = create_sample_excel_file()
    
    # Step 2: Extract IP data with default configuration
    print("\n" + "="*50)
    print("Starting IP Data Extraction...")
    print("="*50)
    
    extracted_data = extract_ip_data(
        excel_file_path=excel_file,
        skip_sheets=4,      # Skip first 4 worksheets
        start_row=7,        # Start from row 7
        output_file="extracted_ips.csv"
    )
    
    # Step 3: Display results
    if not extracted_data.empty:
        display_extracted_data(extracted_data)
        
        # Show summary by sheet
        print("\n📈 SUMMARY BY SHEET:")
        print(extracted_data['sheet_name'].value_counts())
    else:
        print("No data was extracted.")

    # Demo with different configurations
    print("\n" + "="*50)
    print("DEMO: Different Configuration")
    print("="*50)
    
    # Example: Skip only 2 sheets and start from row 5
    demo_data = extract_ip_data(
        excel_file_path=excel_file,
        skip_sheets=2,      # Skip first 2 worksheets
        start_row=5,        # Start from row 5
        output_file="demo_extracted_ips.csv"
    )

"""
Multiple Sheets in One Excel File: Processes a single .xlsx file with multiple worksheets
Configurable Skip: skip_sheets=4 skips the first 4 worksheets
Configurable Start Row: start_row=7 starts processing from row 7 in each sheet
Specific Columns: Uses only columns A (hostname) and B (IP address)
IPv4 Only: Filters only valid IPv4 addresses
Flexible Output: Saves results to CSV

🚀 Excel IP Data Extraction Demo
==================================================
✅ Sample Excel file created: 'sample_network_data.xlsx'

==================================================
Starting IP Data Extraction...
==================================================
📊 Found 7 sheets: ['Cover', 'Summary', 'TOC', 'Instructions', 'Network_A', 'Network_B', 'Network_C']
🔧 Skipping first 4 sheets: ['Cover', 'Summary', 'TOC', 'Instructions']
🔧 Processing 3 sheets: ['Network_A', 'Network_B', 'Network_C']
🔧 Starting from row 7 in each sheet
🔧 Using columns: A=Hostname, B=IP Address

📄 Processing sheet: Network_A
   Sheet dimensions: 7 rows x 2 columns
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


📈 SUMMARY BY SHEET:
sheet_name
Network_A    5
Network_B    5
Network_C    4
Name: count, dtype: int64

==================================================
DEMO: Different Configuration
==================================================
📊 Found 7 sheets: ['Cover', 'Summary', 'TOC', 'Instructions', 'Network_A', 'Network_B', 'Network_C']
🔧 Skipping first 2 sheets: ['Cover', 'Summary']
🔧 Processing 5 sheets: ['TOC', 'Instructions', 'Network_A', 'Network_B', 'Network_C']
🔧 Starting from row 5 in each sheet
🔧 Using columns: A=Hostname, B=IP Address

📄 Processing sheet: TOC
   Sheet dimensions: 0 rows x 0 columns
   ✅ Found 0 IPv4 records in this sheet

📄 Processing sheet: Instructions
   Sheet dimensions: 0 rows x 0 columns
   ✅ Found 0 IPv4 records in this sheet

📄 Processing sheet: Network_A
   Sheet dimensions: 9 rows x 2 columns
   ✅ Found 5 IPv4 records in this sheet

📄 Processing sheet: Network_B
   Sheet dimensions: 7 rows x 2 columns
   ✅ Found 5 IPv4 records in this sheet

📄 Processing sheet: Network_C
   Sheet dimensions: 6 rows x 2 columns
   ✅ Found 4 IPv4 records in this sheet

💾 Extracted data saved to: demo_extracted_ips.csv
"""