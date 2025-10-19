import pandas as pd
import os

def create_sample_csv():
    """Create a sample CSV file for testing"""
    sample_data = """id,name,department,salary,join_date,is_active
1,John Smith,Engineering,75000,2020-03-15,true
2,Jane Doe,Marketing,65000,2019-07-22,true
3,Bob Johnson,Sales,55000,2021-01-10,true
4,Alice Brown,Engineering,80000,2018-11-05,true
5,Charlie Wilson,HR,60000,2022-06-30,false
6,Diana Lee,Marketing,70000,2020-09-14,true
7,Frank Miller,Sales,58000,2021-12-03,true
8,Grace Davis,Engineering,85000,2017-05-18,true"""
    
    with open('sample_data.csv', 'w') as f:
        f.write(sample_data)
    print("✅ Sample CSV file created: sample_data.csv")

def csv_to_xlsx_to_csv():
    """Convert CSV to XLSX and back to CSV"""
    
    # Step 1: Read CSV
    print("\n📖 Reading CSV file...")
    df_csv = pd.read_csv('sample_data.csv')
    print("Original CSV data:")
    print(df_csv)
    print(f"Shape: {df_csv.shape}")
    
    # Step 2: Convert CSV to XLSX
    print("\n🔄 Converting CSV to XLSX...")
    df_csv.to_excel('converted_data.xlsx', index=False, sheet_name='EmployeeData')
    print("✅ CSV converted to XLSX: converted_data.xlsx")
    
    # Step 3: Read XLSX
    print("\n📖 Reading XLSX file...")
    df_xlsx = pd.read_excel('converted_data.xlsx')
    print("XLSX data:")
    print(df_xlsx)
    print(f"Shape: {df_xlsx.shape}")
    
    # Step 4: Convert XLSX back to CSV
    print("\n🔄 Converting XLSX back to CSV...")
    df_xlsx.to_csv('final_data.csv', index=False)
    print("✅ XLSX converted back to CSV: final_data.csv")
    
    # Step 5: Verify data integrity
    print("\n🔍 Verifying data integrity...")
    df_final = pd.read_csv('final_data.csv')
    
    # Check if data is the same
    if df_csv.equals(df_final):
        print("✅ SUCCESS: Data integrity maintained! All conversions worked perfectly.")
    else:
        print("❌ WARNING: Data mismatch detected!")
        
    # Display file sizes
    print(f"\n📊 File sizes:")
    print(f"Original CSV: {os.path.getsize('sample_data.csv')} bytes")
    print(f"XLSX file: {os.path.getsize('converted_data.xlsx')} bytes")
    print(f"Final CSV: {os.path.getsize('final_data.csv')} bytes")

def cleanup():
    """Clean up created files"""
    files_to_remove = ['sample_data.csv', 'converted_data.xlsx', 'final_data.csv']
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"🧹 Cleaned up: {file}")

# Run the complete test
if __name__ == "__main__":
    print("🚀 Starting CSV ↔ XLSX Conversion Test")
    print("=" * 50)
    
    try:
        # Create sample CSV
        create_sample_csv()
        
        # Perform conversions
        csv_to_xlsx_to_csv()
        
        print("\n" + "=" * 50)
        print("🎉 Test completed successfully!")
        
        # Optional: Uncomment the line below to clean up files
        # cleanup()
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")

"""
🚀 Starting CSV ↔ XLSX Conversion Test
==================================================
✅ Sample CSV file created: sample_data.csv

📖 Reading CSV file...
Original CSV data:
   id            name   department  salary   join_date  is_active
0   1      John Smith  Engineering   75000  2020-03-15       True
1   2        Jane Doe    Marketing   65000  2019-07-22       True
2   3     Bob Johnson        Sales   55000  2021-01-10       True
3   4     Alice Brown  Engineering   80000  2018-11-05       True
4   5  Charlie Wilson           HR   60000  2022-06-30      False
5   6       Diana Lee    Marketing   70000  2020-09-14       True
6   7    Frank Miller        Sales   58000  2021-12-03       True
7   8     Grace Davis  Engineering   85000  2017-05-18       True
Shape: (8, 6)

🔄 Converting CSV to XLSX...
✅ CSV converted to XLSX: converted_data.xlsx

📖 Reading XLSX file...
XLSX data:
   id            name   department  salary   join_date  is_active
0   1      John Smith  Engineering   75000  2020-03-15       True
1   2        Jane Doe    Marketing   65000  2019-07-22       True
2   3     Bob Johnson        Sales   55000  2021-01-10       True
3   4     Alice Brown  Engineering   80000  2018-11-05       True
4   5  Charlie Wilson           HR   60000  2022-06-30      False
5   6       Diana Lee    Marketing   70000  2020-09-14       True
6   7    Frank Miller        Sales   58000  2021-12-03       True
7   8     Grace Davis  Engineering   85000  2017-05-18       True
Shape: (8, 6)

🔄 Converting XLSX back to CSV...
✅ XLSX converted back to CSV: final_data.csv

🔍 Verifying data integrity...
✅ SUCCESS: Data integrity maintained! All conversions worked perfectly.

📊 File sizes:
Original CSV: 403 bytes
XLSX file: 5376 bytes
Final CSV: 404 bytes

==================================================
🎉 Test completed successfully!
"""