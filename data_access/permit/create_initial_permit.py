#!pip install faker
from faker import Faker
import json
import time

faker = Faker()

# Generate JSON data
permit = {
    "name": faker.name(),
    "ids": [faker.uuid4() for _ in range(3)],
    "accounts": [faker.iban() for _ in range(3)],
    "keys": [faker.sha256() for _ in range(3)],
    "contact_trusted": [faker.uuid4() for _ in range(3)],
    "time_start": int(time.time()),  # current time in Linux format
    "time_end": int(time.time()) + 100000  # arbitrary future time in Linux format
}

# Write JSON data to a file
with open('permit.json', 'w') as f:
    json.dump(permit, f, indent=4)

