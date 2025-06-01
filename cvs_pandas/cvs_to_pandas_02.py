
"""
┌────┐
│    │
└────┘
"""
import os
import pandas as pd
import requests

# Directory to save the file
directory = './sample_data/'

# Create directory if it doesn't exist
if not os.path.exists(directory):
    os.makedirs(directory)

# URL of the CSV file
url = 'https://cve.mitre.org/data/downloads/allitems.csv'

# Path to save the CSV file
csv_path = os.path.join(directory, 'allitems.csv')

# Download the CSV file using requests to handle encoding
response = requests.get(url)
response.encoding = 'ISO-8859-1'  # Specify the encoding

# Write the content to a local file
with open(csv_path, 'w', encoding='ISO-8859-1') as file:
    file.write(response.text)

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_path, skiprows=10, encoding='ISO-8859-1')  # Adjust the encoding if necessary

# Print all field tags (column names)
print("Field tags (column names):")
print(df.columns.tolist())

# Print all field tags (column names) with their index
field_tags = df.columns.tolist()
for i in range(len(field_tags)):
    print(f"{i}: {field_tags[i]}")

"""
Field tags (column names):
['CVE-1999-0001', 'Candidate', 'ip_input.c in BSD-derived TCP/IP implementations allows remote attackers to cause a denial of service (crash or hang) via crafted packets.', 'BUGTRAQ:19981223 Re: CERT Advisory CA-98.13 - TCP/IP Denial of Service   |   CERT:CA-98-13-tcp-denial-of-service   |   CONFIRM:http://www.openbsd.org/errata23.html#tcpfix   |   OSVDB:5707   |   URL:http://www.osvdb.org/5707', 'Modified (20051217)', '   MODIFY(1) Frech  |     NOOP(2) Northcutt, Wall  |     REVIEWING(1) Christey', 'Christey> A Bugtraq posting indicates that the bug has to do with  |    "short packets with certain options set," so the description  |    should be modified accordingly.  |      |    But is this the same as CVE-1999-0052?  That one is related  |    to nestea (CVE-1999-0257) and probably the one described in  |    BUGTRAQ:19981023 nestea v2 against freebsd 3.0-Release  |    The patch for nestea is in ip_input.c around line 750.  |    The patches for CVE-1999-0001 are in lines 388&446.  So,   |    CVE-1999-0001 is different from CVE-1999-0257 and CVE-1999-0052.  |    The FreeBSD patch for CVE-1999-0052 is in line 750.  |    So, CVE-1999-0257 and CVE-1999-0052 may be the same, though  |    CVE-1999-0052 should be RECAST since this bug affects Linux  |    and other OSes besides FreeBSD.  |    Frech> XF:teardrop(338)  |    This assignment was based solely on references to the CERT advisory.  |    Christey> The description for BID:190, which links to CVE-1999-0052 (a  |    FreeBSD advisory), notes that the patches provided by FreeBSD in  |    CERT:CA-1998-13 suggest a connection between CVE-1999-0001 and  |    CVE-1999-0052.  CERT:CA-1998-13 is too vague to be sure without  |    further analysis.']
0: CVE-1999-0001
1: Candidate
2: ip_input.c in BSD-derived TCP/IP implementations allows remote attackers to cause a denial of service (crash or hang) via crafted packets.
3: BUGTRAQ:19981223 Re: CERT Advisory CA-98.13 - TCP/IP Denial of Service   |   CERT:CA-98-13-tcp-denial-of-service   |   CONFIRM:http://www.openbsd.org/errata23.html#tcpfix   |   OSVDB:5707   |   URL:http://www.osvdb.org/5707
4: Modified (20051217)
5:    MODIFY(1) Frech  |     NOOP(2) Northcutt, Wall  |     REVIEWING(1) Christey
6: Christey> A Bugtraq posting indicates that the bug has to do with  |    "short packets with certain options set," so the description  |    should be modified accordingly.  |      |    But is this the same as CVE-1999-0052?  That one is related  |    to nestea (CVE-1999-0257) and probably the one described in  |    BUGTRAQ:19981023 nestea v2 against freebsd 3.0-Release  |    The patch for nestea is in ip_input.c around line 750.  |    The patches for CVE-1999-0001 are in lines 388&446.  So,   |    CVE-1999-0001 is different from CVE-1999-0257 and CVE-1999-0052.  |    The FreeBSD patch for CVE-1999-0052 is in line 750.  |    So, CVE-1999-0257 and CVE-1999-0052 may be the same, though  |    CVE-1999-0052 should be RECAST since this bug affects Linux  |    and other OSes besides FreeBSD.  |    Frech> XF:teardrop(338)  |    This assignment was based solely on references to the CERT advisory.  |    Christey> The description for BID:190, which links to CVE-1999-0052 (a  |    FreeBSD advisory), notes that the patches provided by FreeBSD in  |    CERT:CA-1998-13 suggest a connection between CVE-1999-0001 and  |    CVE-1999-0052.  CERT:CA-1998-13 is too vague to be sure without  |    further analysis.
<ipython-input-4-0a88ec152794>:27: DtypeWarning: Columns (6) have mixed types. Specify dtype option on import or set low_memory=False.
  df = pd.read_csv(csv_path, skiprows=10, encoding='ISO-8859-1')  # Adjust the encoding if necessary
"""