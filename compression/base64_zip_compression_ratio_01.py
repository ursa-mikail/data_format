import base64
import zlib

# === Input: Replace this with your actual data ===
#data = """
#
#"""

#or
#%%writefile test.txt
#:

# read file test.txt
with open("test.txt", "r") as f:
    data = f.read()

# === Encode string to bytes ===
original_bytes = data.encode('utf-8')
original_size = len(original_bytes)

def size_info(name, compressed_bytes):
    size = len(compressed_bytes)
    saved = original_size - size
    percent = (saved / original_size) * 100 if original_size > 0 else 0
    return {
        'method': name,
        'compressed_size': size,
        'bytes_saved': saved,
        'percent_saved': round(percent, 2)
    }

results = []

# Base64 only
b64_encoded = base64.b64encode(original_bytes)
results.append(size_info("Base64 Only", b64_encoded))

# Zip only
zipped = zlib.compress(original_bytes)
results.append(size_info("Zip Only", zipped))

# Base64 then Zip
b64_then_zip = zlib.compress(base64.b64encode(original_bytes))
results.append(size_info("Base64 -> Zip", b64_then_zip))

# Zip then Base64
zip_then_b64 = base64.b64encode(zlib.compress(original_bytes))
results.append(size_info("Zip -> Base64", zip_then_b64))

# === Print results ===
print(f"Original Size: {original_size} bytes\n")
for r in results:
    print(f"{r['method']}:")
    print(f"  Compressed Size: {r['compressed_size']} bytes")
    print(f"  Bytes Saved:     {r['bytes_saved']} bytes")
    print(f"  Percent Saved:   {r['percent_saved']}%")
    print()

most_savings_in_percentage = max(results, key=lambda x: x['percent_saved'])
most_savings_in_bytes = max(results, key=lambda x: x['bytes_saved'])
print(f"The most optimal result comes from: {most_savings_in_percentage}")

"""
Original Size: 11904 bytes

Base64 Only:
  Compressed Size: 15872 bytes
  Bytes Saved:     -3968 bytes
  Percent Saved:   -33.33%

Zip Only:
  Compressed Size: 4605 bytes
  Bytes Saved:     7299 bytes
  Percent Saved:   61.32%

Base64 -> Zip:
  Compressed Size: 6654 bytes
  Bytes Saved:     5250 bytes
  Percent Saved:   44.1%

Zip -> Base64:
  Compressed Size: 6140 bytes
  Bytes Saved:     5764 bytes
  Percent Saved:   48.42%

The most optimal result comes from: {'method': 'Zip Only', 'compressed_size': 4605, 'bytes_saved': 7299, 'percent_saved': 61.32}
"""