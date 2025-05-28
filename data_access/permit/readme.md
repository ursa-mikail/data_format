# Permit Management System
This project generates a Python class to handle permit data from a JSON file, including timestamps. It allows reading, modifying, and displaying permit information in a user-friendly format.

## Overview
Generate JSON Data: Creates a sample permit.json file with random data using the faker library.

Generate Python Class: Creates a Python class (Permit) based on the structure of the JSON file.

Read and Process Permit Data: Reads the modified_permit.json file, converts timestamps into a human-readable format, and displays the status (whether the permit is expired or how much time is left).

There is also an expiration check:
```
Time Start: 2024-12-02T15:30:00
Time End: 2024-12-05T15:30:00
Time left: 2 days, 3 hours, 15 minutes
```

If the permit is expired:
```
Time Start: 2024-12-02T15:30:00
Time End: 2024-11-28T15:30:00
Expired
```