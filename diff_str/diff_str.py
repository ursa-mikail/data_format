import hashlib
from binascii import unhexlify, hexlify
import sys

def compare_strings_with_color(str1, str2, str1_name="String 1", str2_name="String 2", 
                              encoding='auto', highlight_color='red', context_chars=2,
                              show_hex=False):
    """
    Compare two strings and display differences with color highlighting.
    
    Args:
        str1: First string to compare (any type)
        str2: Second string to compare (any type)
        str1_name: Name for first string (for display)
        str2_name: Name for second string (for display)
        encoding: 'auto', 'hex', 'bytes', 'text', or 'raw'
        highlight_color: Color for highlighting differences
        context_chars: Number of characters to show around differences for context
        show_hex: Whether to show hexadecimal representation alongside text
    """
    
    # Color codes
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m'
    }
    reset_color = '\033[0m'
    color_code = colors.get(highlight_color, colors['red'])
    
    # Helper function to safely convert to display format
    def safe_convert(data, encoding_type):
        if encoding_type == 'hex':
            try:
                bytes_data = unhexlify(data)
                return hexlify(bytes_data).decode('ascii'), bytes_data
            except:
                # If hex conversion fails, treat as text
                return data, data.encode('utf-8', errors='replace')
        elif encoding_type == 'bytes':
            if isinstance(data, bytes):
                return data.hex(), data
            else:
                return data.encode('utf-8', errors='replace').hex(), data.encode('utf-8', errors='replace')
        else:  # text, auto, or raw
            if isinstance(data, bytes):
                # Try to decode as text, fall back to hex representation
                try:
                    return data.decode('utf-8'), data
                except:
                    return data.hex(), data
            else:
                return str(data), str(data).encode('utf-8', errors='replace')
    
    # Auto-detect encoding if needed
    if encoding == 'auto':
        if (isinstance(str1, bytes) and isinstance(str2, bytes)):
            encoding = 'bytes'
        elif (all(c in '0123456789abcdefABCDEF' for c in str(str1)) and 
              all(c in '0123456789abcdefABCDEF' for c in str(str2)) and
              len(str(str1)) % 2 == 0 and len(str(str2)) % 2 == 0):
            encoding = 'hex'
        else:
            encoding = 'text'
    
    # Convert strings to display format and get bytes for hashing
    str1_display, bytes1 = safe_convert(str1, encoding)
    str2_display, bytes2 = safe_convert(str2, encoding)
    
    # Find differences based on display strings
    min_len = min(len(str1_display), len(str2_display))
    max_len = max(len(str1_display), len(str2_display))
    
    diffs = []
    for i in range(min_len):
        if str1_display[i] != str2_display[i]:
            diffs.append(i)
    
    # Handle length differences
    length_diff = False
    if len(str1_display) != len(str2_display):
        diffs.extend(range(min_len, max_len))
        length_diff = True
        print(f"⚠️  Strings have different lengths ({len(str1_display)} vs {len(str2_display)})")
    
    print(f"\nChanges found at {len(diffs)} position(s): {diffs}")
    
    # Create colored versions showing differences
    def add_color_highlight(text, diff_positions, color, context=context_chars):
        if not diff_positions:
            return text
        
        result = []
        i = 0
        processed_positions = set()
        
        while i < len(text):
            if i in diff_positions and i not in processed_positions:
                # Find consecutive differences
                j = i
                while j < len(text) and j in diff_positions:
                    processed_positions.add(j)
                    j += 1
                
                # Add context before if available
                start_context = max(0, i - context)
                if start_context < i:
                    result.append(text[start_context:i])
                
                # Add colored differences
                result.append(color + text[i:j] + reset_color)
                i = j
            else:
                if i < len(text):
                    result.append(text[i])
                i += 1
        
        return ''.join(result)
    
    # Display results
    print(f"\n{color_code}↘ {str1_name} with differences highlighted:{reset_color}")
    colored1 = add_color_highlight(str1_display, diffs, color_code)
    print(colored1)
    
    print(f"\n{color_code}↘ {str2_name} with differences highlighted:{reset_color}")
    colored2 = add_color_highlight(str2_display, diffs, color_code)
    print(colored2)
    
    # Show hex representation if requested or for non-printable characters
    if show_hex or encoding == 'bytes':
        print(f"\nHex representations:")
        print(f"{str1_name}: {bytes1.hex()}")
        print(f"{str2_name}: {bytes2.hex()}")
    
    # Show detailed side-by-side comparison
    if diffs:
        print(f"\n{color_code}Detailed comparison:{reset_color}")
        for i, pos in enumerate(diffs[:15]):  # Limit to first 15 differences
            if pos < len(str1_display) and pos < len(str2_display):
                char1 = str1_display[pos]
                char2 = str2_display[pos]
                
                # Show character codes for better understanding
                char1_repr = repr(char1) if char1.isprintable() else f"\\x{ord(char1):02x}"
                char2_repr = repr(char2) if char2.isprintable() else f"\\x{ord(char2):02x}"
                
                print(f"  Position {pos:3d}: '{char1_repr}' vs '{char2_repr}'")
        
        if len(diffs) > 15:
            print(f"  ... and {len(diffs) - 15} more differences")
    
    return diffs, bytes1, bytes2, str1_display, str2_display

def hash_with_append(data1, data2, append_data=b"hello", hash_algorithm='md5'):
    """
    Append data to both inputs and compute hashes.
    
    Args:
        data1: First data (bytes)
        data2: Second data (bytes)
        append_data: Data to append (bytes or string)
        hash_algorithm: Hash algorithm ('md5', 'sha1', 'sha256', 'sha512')
    """
    
    # Convert append_data to bytes if it's a string
    if isinstance(append_data, str):
        append_data = append_data.encode('utf-8')
    
    # Select hash algorithm
    hash_functions = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }
    
    if hash_algorithm not in hash_functions:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")
    
    hasher = hash_functions[hash_algorithm]
    
    # Compute hashes
    h1 = hasher()
    h2 = hasher()
    
    h1.update(data1 + append_data)
    h2.update(data2 + append_data)
    
    hash1 = h1.hexdigest()
    hash2 = h2.hexdigest()
    
    print(f"\n{'-'*60}")
    print(f"Hash results with appended data '{append_data.decode('utf-8', errors='replace')}' using {hash_algorithm}:")
    print(f"{'-'*60}")
    
    # Show the combined data being hashed
    try:
        combined1 = (data1 + append_data).decode('utf-8', errors='replace')
        print(f"Data 1 + append: {repr(combined1)}")
    except:
        print(f"Data 1 + append (hex): {(data1 + append_data).hex()}")
    
    print(f"Hash 1: {hash1}")
    
    try:
        combined2 = (data2 + append_data).decode('utf-8', errors='replace')
        print(f"Data 2 + append: {repr(combined2)}")
    except:
        print(f"Data 2 + append (hex): {(data2 + append_data).hex()}")
    
    print(f"Hash 2: {hash2}")
    
    if hash1 == hash2:
        print("🎉 Hashes are IDENTICAL (collision found!)")
    else:
        print("❌ Hashes are DIFFERENT")
    
    return hash1, hash2

# Example usage and test cases
if __name__ == "__main__":
    print("STRING COMPARISON TOOL WITH COLOR HIGHLIGHTING")
    print("=" * 60)
    
    # Test case 1: Original hex strings (MD5 collision example)
    print("\n1. HEXADECIMAL STRINGS (MD5 Collision):")
    m1_hex = 'd131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f8955ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70'
    m2_hex = 'd131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70'
    
    diffs, m1_bytes, m2_bytes, m1_disp, m2_disp = compare_strings_with_color(
        m1_hex, m2_hex,
        str1_name="Collision 1", 
        str2_name="Collision 2",
        encoding='hex',
        highlight_color='red'
    )
    
    hash_with_append(m1_bytes, m2_bytes, b"hello", 'md5')
    
    # Test case 2: Text strings
    print("\n\n2. TEXT STRINGS:")
    text1 = "The quick brown fox jumps over the lazy dog"
    text2 = "The quick brown fox jumps over the lazy cat"
    
    compare_strings_with_color(
        text1, text2,
        str1_name="Text 1",
        str2_name="Text 2", 
        encoding='text',
        highlight_color='green'
    )
    
    # Test case 3: Mixed characters
    print("\n\n3. MIXED CHARACTERS (including special chars):")
    mixed1 = "Hello\nWorld\t123\x00\x01\xff"
    mixed2 = "Hello\nWorld\t124\x00\x02\xfe"
    
    diffs, b1, b2, disp1, disp2 = compare_strings_with_color(
        mixed1, mixed2,
        str1_name="Mixed 1",
        str2_name="Mixed 2",
        encoding='raw',
        highlight_color='yellow',
        show_hex=True
    )
    
    # Test case 4: Byte strings
    print("\n\n4. BYTE STRINGS:")
    bytes1 = b'\x00\x01\x02\x03\x04hello\xff\xfe'
    bytes2 = b'\x00\x01\x02\x03\x05hello\xff\xfd'
    
    compare_strings_with_color(
        bytes1, bytes2,
        str1_name="Bytes 1",
        str2_name="Bytes 2",
        encoding='bytes',
        highlight_color='cyan',
        show_hex=True
    )
    
    # Test case 5: Unicode characters
    print("\n\n5. UNICODE STRINGS:")
    unicode1 = "Hello 🌍 World 🚀"
    unicode2 = "Hello 🌎 World 🚀"
    
    compare_strings_with_color(
        unicode1, unicode2,
        str1_name="Unicode 1", 
        str2_name="Unicode 2",
        encoding='text',
        highlight_color='magenta'
    )
    
    # Test different hash algorithms
    print("\n\n6. TESTING DIFFERENT HASH ALGORITHMS:")
    hash_with_append(m1_bytes, m2_bytes, "collision", 'sha1')
    hash_with_append(m1_bytes, m2_bytes, "collision", 'sha256')

    