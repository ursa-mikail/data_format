import binascii
import base64
import os

def ascii_to_hex(s):
    """Convert an ASCII string to hexadecimal."""
    return binascii.hexlify(s.encode()).decode()

def hex_to_ascii(hex_str):
    """Convert a hexadecimal string to ASCII."""
    return binascii.unhexlify(hex_str).decode()

def hex_to_bytes(hex_str):
    """Convert a hexadecimal string to bytes."""
    return binascii.unhexlify(hex_str)

def bytes_to_hex(b):
    """Convert bytes to a hexadecimal string."""
    return binascii.hexlify(b).decode()

def ascii_to_bytes(s):
    """Convert an ASCII string to bytes."""
    return s.encode()

def bytes_to_ascii(b):
    """Convert bytes to an ASCII string."""
    return b.decode()

def ascii_to_base64(s):
    """Convert an ASCII string to base64."""
    return base64.b64encode(s.encode()).decode()

def base64_to_ascii(b64_str):
    """Convert a base64 string to ASCII."""
    return base64.b64decode(b64_str).decode()

def bytes_to_base64(b):
    """Convert bytes to a base64 string."""
    return base64.b64encode(b).decode()

def base64_to_bytes(b64_str):
    """Convert a base64 string to bytes."""
    return base64.b64decode(b64_str)

def generate_random_hex(number_of_hex_bytes):
    """Generate a random hexadecimal string of a given length."""
    return binascii.hexlify(os.urandom(number_of_hex_bytes)).decode()

# Use cases

# 1. Convert ASCII string to hexadecimal and back
ascii_string = "Hello, World!"
hex_string = ascii_to_hex(ascii_string)
print(f"ASCII to Hex: {hex_string}")  # Output: 48656c6c6f2c20576f726c6421
print(f"Hex to ASCII: {hex_to_ascii(hex_string)}")  # Output: Hello, World!

# 2. Convert ASCII string to bytes and back
bytes_data = ascii_to_bytes(ascii_string)
print(f"ASCII to Bytes: {bytes_data}")  # Output: b'Hello, World!'
print(f"Bytes to ASCII: {bytes_to_ascii(bytes_data)}")  # Output: Hello, World!

# 3. Convert hexadecimal string to bytes and back
number_of_bytes_to_generate = 200
hex_str = generate_random_hex(number_of_bytes_to_generate)  # Generates a random N-byte hex string
print(f"Generated Hex: {hex_str}")  # Example output: a1b2c3d4e5f67890abcdef12
bytes_from_hex = hex_to_bytes(hex_str)
print(f"Hex to Bytes: {bytes_from_hex}")  # Output: b'\xa1\xb2\xc3\xd4\xe5\xf6x\x90\xab\xcd\xef\x12'
print(f"Bytes to Hex: {bytes_to_hex(bytes_from_hex)}")  # Output: a1b2c3d4e5f67890abcdef12

# 4. Convert ASCII string to base64 and back
base64_string = ascii_to_base64(ascii_string)
print(f"ASCII to Base64: {base64_string}")  # Output: SGVsbG8sIFdvcmxkIQ==
print(f"Base64 to ASCII: {base64_to_ascii(base64_string)}")  # Output: Hello, World!

# 5. Convert bytes to base64 and back
base64_from_bytes = bytes_to_base64(bytes_data)
print(f"Bytes to Base64: {base64_from_bytes}")  # Output: SGVsbG8sIFdvcmxkIQ==
print(f"Base64 to Bytes: {base64_to_bytes(base64_from_bytes)}")  # Output: b'Hello, World!'

"""
ASCII to Hex: 48656c6c6f2c20576f726c6421
Hex to ASCII: Hello, World!
ASCII to Bytes: b'Hello, World!'
Bytes to ASCII: Hello, World!
Generated Hex: 7aca5f0720b7d37f51304b7d1f1ddfc8f59d3260a7f1cd4057c20d9960278b96d233ed6be74c3a8a8085c3016f122341c4ba9624fdfb9423047f93ee7086c7cf5f1ee1c965a86ee1d5a83e72438b080611e34ce63506397026ef81ac356f6797b95e73c58f771e7a7ff9e2351f9968907ab0dcbacf4f8111bf619e56a561154ac5bb90db57a9919a549fe0488d0e1608ee05a21aa2fa5298e4622cbdbfd15af333ddffe308eecfa606583e39d465984fb487a5bc80026e0d623ed51de8db739693b503ba7f95a740
Hex to Bytes: b"z\xca_\x07 \xb7\xd3\x7fQ0K}\x1f\x1d\xdf\xc8\xf5\x9d2`\xa7\xf1\xcd@W\xc2\r\x99`'\x8b\x96\xd23\xedk\xe7L:\x8a\x80\x85\xc3\x01o\x12#A\xc4\xba\x96$\xfd\xfb\x94#\x04\x7f\x93\xeep\x86\xc7\xcf_\x1e\xe1\xc9e\xa8n\xe1\xd5\xa8>rC\x8b\x08\x06\x11\xe3L\xe65\x069p&\xef\x81\xac5og\x97\xb9^s\xc5\x8fw\x1ez\x7f\xf9\xe25\x1f\x99h\x90z\xb0\xdc\xba\xcfO\x81\x11\xbfa\x9eV\xa5a\x15J\xc5\xbb\x90\xdbW\xa9\x91\x9aT\x9f\xe0H\x8d\x0e\x16\x08\xee\x05\xa2\x1a\xa2\xfaR\x98\xe4b,\xbd\xbf\xd1Z\xf33\xdd\xff\xe3\x08\xee\xcf\xa6\x06X>9\xd4e\x98O\xb4\x87\xa5\xbc\x80\x02n\rb>\xd5\x1d\xe8\xdbs\x96\x93\xb5\x03\xba\x7f\x95\xa7@"
Bytes to Hex: 7aca5f0720b7d37f51304b7d1f1ddfc8f59d3260a7f1cd4057c20d9960278b96d233ed6be74c3a8a8085c3016f122341c4ba9624fdfb9423047f93ee7086c7cf5f1ee1c965a86ee1d5a83e72438b080611e34ce63506397026ef81ac356f6797b95e73c58f771e7a7ff9e2351f9968907ab0dcbacf4f8111bf619e56a561154ac5bb90db57a9919a549fe0488d0e1608ee05a21aa2fa5298e4622cbdbfd15af333ddffe308eecfa606583e39d465984fb487a5bc80026e0d623ed51de8db739693b503ba7f95a740
ASCII to Base64: SGVsbG8sIFdvcmxkIQ==
Base64 to ASCII: Hello, World!
Bytes to Base64: SGVsbG8sIFdvcmxkIQ==
Base64 to Bytes: b'Hello, World!'
"""