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

import base64

def baseN_to_baseN(value: str, from_base: int, to_base: int) -> str:
    """
    Convert a string representation of a number from one base to another.
    Special case: base64 is treated as base 64 with a custom alphabet.
    :param value: String representation of the number in from_base.
    :param from_base: The base to convert from (e.g., 10).
    :param to_base: The base to convert to (e.g., 64).
    :return: String representation of the number in to_base.
    """
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    
    def decode_custom_base(value: str, base: int, alphabet: str) -> int:
        num = 0
        for char in value:
            num = num * base + alphabet.index(char)
        return num

    def encode_custom_base(num: int, base: int, alphabet: str) -> str:
        if num == 0:
            return alphabet[0]
        encoded = ''
        while num > 0:
            encoded = alphabet[num % base] + encoded
            num //= base
        return encoded

    # Decode from input base
    if from_base == 64:
        decimal_value = decode_custom_base(value, 64, base64_chars)
    else:
        decimal_value = int(value, from_base)

    # Encode to output base
    if to_base == 64:
        return encode_custom_base(decimal_value, 64, base64_chars)
    elif to_base == 10:
        return str(decimal_value)
    elif to_base == 16:
        return hex(decimal_value)[2:]
    elif to_base == 2:
        return bin(decimal_value)[2:]
    elif to_base == 8:
        return oct(decimal_value)[2:]
    else:
        digits = "0123456789abcdefghijklmnopqrstuvwxyz"
        if to_base > len(digits):
            raise ValueError("Base too large, max base supported is 36 (or 64 for base64).")
        result = ""
        while decimal_value > 0:
            result = digits[decimal_value % to_base] + result
            decimal_value //= to_base
        return result or "0"

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

# Example test: Convert big integer from base 10 to base 16
int_big = '123456789123456789'
hex_big = baseN_to_baseN(int_big, 10, 16)
print(f"baseN_to_baseN(int_big, 10, 16): {hex_big}")  

int_big_recovered = baseN_to_baseN(hex_big, 16, 10)
print(f"baseN_to_baseN(hex_big, 16, 10): {int_big_recovered}")  
assert int_big_recovered == int_big

# Decimal to Base64
b64 = baseN_to_baseN(int_big, 10, 64)
print(f"Decimal to Base64: {b64}")

# Base64 back to Decimal
int_big_recovered = baseN_to_baseN(b64, 64, 10)
print(f"Base64 to Decimal: {int_big_recovered}")
assert int_big_recovered == int_big

"""
ASCII to Hex: 48656c6c6f2c20576f726c6421
Hex to ASCII: Hello, World!
ASCII to Bytes: b'Hello, World!'
Bytes to ASCII: Hello, World!
Generated Hex: 2d40adc0d9997a2209b030a470e53065612b86b0ba1aacb32c6a9e6d5350f8a96ef6134cc22fcbbaf617f00a9326cdd7a23a6530e644ac61103b83fc5f1cdf5149fe3edf7965489fcce2dd012ff69b3861388f247c44de1d68b9973f0a40bb1e608041870ffad6a61d08cdd1c8d1810aa195e0ea07276fc44f69ca430fe2cbd770f899d2aecdde6333544cf58679c66b4e44bbbb5d95f8d2e7f0af9bd52f0aef2395da7e31b40caee296acfd925a884ca2a5b8883bf2d33be69e85157fe4cae4c3958e5fc0eeeab8
Hex to Bytes: b'-@\xad\xc0\xd9\x99z"\t\xb00\xa4p\xe50ea+\x86\xb0\xba\x1a\xac\xb3,j\x9emSP\xf8\xa9n\xf6\x13L\xc2/\xcb\xba\xf6\x17\xf0\n\x93&\xcd\xd7\xa2:e0\xe6D\xaca\x10;\x83\xfc_\x1c\xdfQI\xfe>\xdfyeH\x9f\xcc\xe2\xdd\x01/\xf6\x9b8a8\x8f$|D\xde\x1dh\xb9\x97?\n@\xbb\x1e`\x80A\x87\x0f\xfa\xd6\xa6\x1d\x08\xcd\xd1\xc8\xd1\x81\n\xa1\x95\xe0\xea\x07\'o\xc4Oi\xcaC\x0f\xe2\xcb\xd7p\xf8\x99\xd2\xae\xcd\xdec3TL\xf5\x86y\xc6kND\xbb\xbb]\x95\xf8\xd2\xe7\xf0\xaf\x9b\xd5/\n\xef#\x95\xda~1\xb4\x0c\xae\xe2\x96\xac\xfd\x92Z\x88L\xa2\xa5\xb8\x88;\xf2\xd3;\xe6\x9e\x85\x15\x7f\xe4\xca\xe4\xc3\x95\x8e_\xc0\xee\xea\xb8'
Bytes to Hex: 2d40adc0d9997a2209b030a470e53065612b86b0ba1aacb32c6a9e6d5350f8a96ef6134cc22fcbbaf617f00a9326cdd7a23a6530e644ac61103b83fc5f1cdf5149fe3edf7965489fcce2dd012ff69b3861388f247c44de1d68b9973f0a40bb1e608041870ffad6a61d08cdd1c8d1810aa195e0ea07276fc44f69ca430fe2cbd770f899d2aecdde6333544cf58679c66b4e44bbbb5d95f8d2e7f0af9bd52f0aef2395da7e31b40caee296acfd925a884ca2a5b8883bf2d33be69e85157fe4cae4c3958e5fc0eeeab8
ASCII to Base64: SGVsbG8sIFdvcmxkIQ==
Base64 to ASCII: Hello, World!
Bytes to Base64: SGVsbG8sIFdvcmxkIQ==
Base64 to Bytes: b'Hello, World!'
baseN_to_baseN(int_big, 10, 16): 1b69b4bacd05f15
baseN_to_baseN(hex_big, 16, 10): 123456789123456789
Decimal to Base64: G2m0us0F8V
Base64 to Decimal: 123456789123456789
"""