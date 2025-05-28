import json

class Permit:
    def __init__(self, name="", ids=None, accounts=None, keys=None, contact_trusted=None, time_start=0, time_end=0):
        self.name = name
        self.ids = ids if ids is not None else []
        self.accounts = accounts if accounts is not None else []
        self.keys = keys if keys is not None else []
        self.contact_trusted = contact_trusted if contact_trusted is not None else []
        self.time_start = time_start
        self.time_end = time_end

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_ids(self):
        return self.ids

    def set_ids(self, ids):
        self.ids = ids

    def get_accounts(self):
        return self.accounts

    def set_accounts(self, accounts):
        self.accounts = accounts

    def get_keys(self):
        return self.keys

    def set_keys(self, keys):
        self.keys = keys

    def get_contact_trusted(self):
        return self.contact_trusted

    def set_contact_trusted(self, contact_trusted):
        self.contact_trusted = contact_trusted

    def get_time_start(self):
        return self.time_start

    def set_time_start(self, time_start):
        self.time_start = time_start

    def get_time_end(self):
        return self.time_end

    def set_time_end(self, time_end):
        self.time_end = time_end

    @staticmethod
    def from_json(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return Permit(
            name=data.get('name', ''),
            ids=data.get('ids', []),
            accounts=data.get('accounts', []),
            keys=data.get('keys', []),
            contact_trusted=data.get('contact_trusted', []),
            time_start=data.get('time_start', 0),
            time_end=data.get('time_end', 0)
        )

    def to_json(self, file_path):
        data = {
            "name": self.name,
            "ids": self.ids,
            "accounts": self.accounts,
            "keys": self.keys,
            "contact_trusted": self.contact_trusted,
            "time_start": self.time_start,
            "time_end": self.time_end
        }
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

# Usage example
if __name__ == "__main__":
    permit = Permit.from_json('permit.json')
    print("Name:", permit.get_name())
    print("IDs:", permit.get_ids())
    print("Accounts:", permit.get_accounts())
    print("Keys:", permit.get_keys())
    print("Contact Trusted:", permit.get_contact_trusted())
    print("Time Start:", permit.get_time_start())
    print("Time End:", permit.get_time_end())

    # Modify and save back to JSON
    permit.set_name("New Name")
    permit.to_json('modified_permit.json')

"""
Name: Kristin Schmidt
IDs: ['6a3f4f63-8f80-4f60-8ec2-9e0eecd5a852', '4b220783-0e37-4584-8054-5cef7b2b392a', '425e7515-7b62-453c-a891-c9df49adf9f6']
Accounts: ['GB30EXPX68376823955355', 'GB59ZEQL21608061534586', 'GB79KPOD93387630360772']
Keys: ['74b3d985b04c62aab698d38e6c680fe3e58058e32ffef30c6c1e1232d37ca3c2', '3ea620c682c0b89c7073854a960f11ff87c98f46e6f3a5012726c4599f29db8b', 'd298d29e74a7700f75b4400fc441eba43b0c06aee38ea87e04cbbce7ba54b90d']
Contact Trusted: ['54913a43-04e4-4c19-bdf3-952ab5f8c0c7', '8e1bebed-2d86-40d3-b4bc-cef7531c0ccc', 'fb447bc7-791a-489f-81fd-9186f5776dc9']
Time Start: 1748459164
Time End: 1748559164
"""