<pre>
As we extend the porting of CSV to SQL and back (refer: <a href="https://github.com/ursa-mikail/sql_csv_porting">sql_csv_porting</a>), we illustrate data porting with CSV, YAML, and JSON as well.

Starting from a CSV file, we generate random data with field headers:
[service, user, time_stamp, hash_of_all_data].

We demonstrate this by generating 3 rows of random data (all fields random), such as service_hex_5_bytes, etc.

The versatility of the data porting package is shown as:
CSV <--> YAML <--> JSON (for YAML and JSON, output the formatted files).

Output to: ./sample_data/data/

From the SQL, all data including field headers is displayed.

For YAML and JSON, read from ./sample_data/data/ and convert back to CSV.

.
├── 01_generate_data_to_csv.py
├── 02_csv_to_yaml_and_json.py
├── 03_csv_to_sql_and_display.py
├── 04_yaml_and_json_to_csv.py
└── sample_data
    └── data
        ├── data.csv
        ├── data.db
        ├── data.json
        ├── data.yaml
        ├── json_to_csv.csv
        └── yaml_to_csv.csv

</pre>
