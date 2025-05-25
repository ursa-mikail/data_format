import os
import binascii
import random
import string
import hashlib

# Create the sample_data directory if it doesn't exist
os.makedirs('./sample_data', exist_ok=True)

# Function to generate random text
def generate_random_text(length=100):
    letters = string.ascii_letters + string.digits + string.punctuation + ' '
    return ''.join(random.choice(letters) for _ in range(length))

# Write random text to out.txt
number_of_ascii_chars_to_generate = 200
random_text = generate_random_text(number_of_ascii_chars_to_generate)
with open('./sample_data/out.txt', 'w') as file:
    file.write(random_text)

# Read the text from out.txt and convert to bytes
with open('./sample_data/out.txt', 'r') as file:
    text = file.read()

text_bytes = text.encode()

# Convert the bytes to a hexadecimal string
hex_str = bytes_to_hex(text_bytes)

# Convert the hexadecimal string back to ASCII
ascii_str = hex_to_ascii(hex_str)

# Print the results
print(f"Original text: {text}")
print(f"Text bytes: {text_bytes}")
print(f"Hexadecimal string: {hex_str}")
print(f"Converted back to ASCII: {ascii_str}")


# Compute SHA-256 hash of the file contents
file_hash = hashlib.sha256(text_bytes).hexdigest()

# Compute SHA-256 hash of the recovered string
recovered_hash = hashlib.sha256(ascii_str.encode()).hexdigest()

# Print the hash
print(f"SHA-256 hash of file contents: {file_hash}")
print(f"SHA-256 hash of recovered string: {recovered_hash}")

if (file_hash == recovered_hash):
    print("Hashes [match]")
else:
    print("Hashes [do not match]")

"""
Original text: xeWXAd5nJ^"6x}Th)/&Cj[SEB>s%zw"kpN$M/X<~Ve=1{p`^M[75wHUo>Nl.teWyq;Ni_OP&y]z@4F&m0(<?L!?gk7*sAE:_p{Sq
Text bytes: b'xeWXAd5nJ^"6x}Th)/&Cj[SEB>s%zw"kpN$M/X<~Ve=1{p`^M[75wHUo>Nl.teWyq;Ni_OP&y]z@4F&m0(<?L!?gk7*sAE:_p{Sq'
Hexadecimal string: 786557584164356e4a5e2236787d5468292f26436a5b5345423e73257a77226b704e244d2f583c7e56653d317b70605e4d5b37357748556f3e4e6c2e74655779713b4e695f4f5026795d7a403446266d30283c3f4c213f676b372a7341453a5f707b5371
Converted back to ASCII: xeWXAd5nJ^"6x}Th)/&Cj[SEB>s%zw"kpN$M/X<~Ve=1{p`^M[75wHUo>Nl.teWyq;Ni_OP&y]z@4F&m0(<?L!?gk7*sAE:_p{Sq
SHA-256 hash of file contents: 3633faa016abdcbe685eee459b45ff13ea367bc11290ea67086093b3ec552bbc
SHA-256 hash of recovered string: 3633faa016abdcbe685eee459b45ff13ea367bc11290ea67086093b3ec552bbc
Hashes [match]
"""
