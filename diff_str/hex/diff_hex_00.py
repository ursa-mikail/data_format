import hashlib
from binascii import unhexlify, hexlify

# Define hexadecimal strings (no spaces or newlines)
m1_hex = 'd131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f8955ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70'
m2_hex = 'd131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70'

#m1_hex = '0e306561559aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef'
#m2_hex = '0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef'

# Convert hex strings to bytes
m1 = unhexlify(m1_hex)
m2 = unhexlify(m2_hex)

# Compare the two sequences and find differences
diffs = [i for i in range(len(m1)) if m1[i] != m2[i]]
print("Changes in hex at positions:", diffs)

# Visualizing differences
m_diff = list(m1_hex)  # Convert to list for mutable changes
for x in diffs:
    m_diff[x] = '-'  # Mark differences


print("Modified Hex String with Differences:")
print("".join(m_diff))
print(m1_hex)
print(m2_hex)

# Append a word and hash again
word = "hello".encode()

mm1 = hashlib.md5()
mm2 = hashlib.md5()

mm1.update(m1 + word)
mm2.update(m2 + word)

print("\nOriginal M1 + word:", hexlify(m1 + word), "\nMD5 Hash:", mm1.hexdigest())
print("\nOriginal M2 + word:", hexlify(m2 + word), "\nMD5 Hash:", mm2.hexdigest())

"""
Changes in hex at positions: [19, 45, 59, 83, 109, 123]
Modified Hex String with Differences:
d131dd02c5e6eec4693-9a0698aff95c2fcab58712467-ab4004583eb8f-7f8955ad340609f4b30283e-88832571415a085125e8f7cdc-9fd91dbdf2803-3c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70
d131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f8955ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70
d131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70

Original M1 + word: b'd131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f8955ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a7068656c6c6f' 
MD5 Hash: fd70c57bdd6dd7464f0d4bcc47d9a71c

Original M2 + word: b'd131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a7068656c6c6f' 
MD5 Hash: fd70c57bdd6dd7464f0d4bcc47d9a71c
"""