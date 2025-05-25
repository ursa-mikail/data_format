# Tabulated Data Markup Language (TDML) file into a CSV 

## [Method 01]
✅ Text File Format (Before CSV)
Instead of spaces (which can appear inside data), we'll use a custom delimiter such as | or ; or any character `[delimiter]` stored in a variable delimiter.

🧪 Example Usage: ![method_01](method_01/tdml_file_into_csv.py)

<img src="method_01/data.txt.png" alt="data.txt" style="width:320px;height:110px;"> ➡️➡️➡️ <img src="method_01/data.csv.png" alt="data.csv" style="width:320px;height:110px;">

<hr>

## [Method 02]
Converts a Tabulated Data Markup Language (TDML) file into a CSV file, stitching data column by column. This assumes TDML is structured as tabular data in a clear text format, rather than an XML-based format.

The script processes multiple TDML files (f1.tdml, f2.tdml, f3.tdml, etc.), automatically detecting them and converting them into a single CSV file. 🚀

![tabulated_data_markup_language_tdml_file_into_a_csv](method_02/tabulated_data_markup_language_tdml_file_into_a_csv.png)

