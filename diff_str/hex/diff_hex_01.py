import hashlib
from binascii import unhexlify, hexlify

# Define hexadecimal strings (no spaces or newlines)
m1_hex = 'd131dd02c5e6eec4693d9a0698aff95c2fcab58712467eab4004583eb8fb7f8955ad340609f4b30283e488832571415a085125e8f7cdc99fd91dbdf280373c5bd8823e3156348f5bae6dacd436c919c6dd53e2b487da03fd02396306d248cda0e99f33420f577ee8ce54b67080a80d1ec69821bcb6a8839396f9652b6ff72a70'
#m2_hex = 'd131dd02c5e6eec4693d9a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70'
m2_hex = 'd131dd02c5e6eec469309a0698aff95c2fcab50712467eab4004583eb8fb7f8955ad340609f4b30283e4888325f1415a085125e8f7cdc99fd91dbd7280373c5bd8823e3156348f5bae6dacd436c919c6dd53e23487da03fd02396306d248cda0e99f33420f577ee8ce54b67080280d1ec69821bcb6a8839396f965ab6ff72a70'

# Alternative test strings
#m1_hex = '0e306561559aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef'
#m2_hex = '0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef'

def compare_strings_with_color(str1, str2, str1_name="String 1", str2_name="String 2", 
                              encoding='hex', highlight_color='red', context_chars=2):
    """
    Compare two strings and display differences with color highlighting.
    
    Args:
        str1: First string to compare
        str2: Second string to compare
        str1_name: Name for first string (for display)
        str2_name: Name for second string (for display)
        encoding: 'hex', 'bytes', or 'text'
        highlight_color: Color for highlighting differences ('red', 'green', 'yellow', 'blue', 'magenta', 'cyan')
        context_chars: Number of characters to show around differences for context
    """
    
    # Color codes
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m'
    }
    reset_color = '\033[0m'
    color_code = colors.get(highlight_color, colors['red'])
    
    # Convert strings based on encoding
    if encoding == 'hex':
        bytes1 = unhexlify(str1)
        bytes2 = unhexlify(str2)
        str1_display = str1
        str2_display = str2
    elif encoding == 'bytes':
        bytes1 = str1 if isinstance(str1, bytes) else str1.encode()
        bytes2 = str2 if isinstance(str2, bytes) else str2.encode()
        str1_display = hexlify(bytes1).decode() if isinstance(bytes1, bytes) else str1
        str2_display = hexlify(bytes2).decode() if isinstance(bytes2, bytes) else str2
    else:  # text
        bytes1 = str1.encode() if isinstance(str1, str) else str1
        bytes2 = str2.encode() if isinstance(str2, str) else str2
        str1_display = str1
        str2_display = str2
    
    # Find differences
    min_len = min(len(bytes1), len(bytes2))
    max_len = max(len(bytes1), len(bytes2))
    
    diffs = []
    for i in range(min_len):
        if bytes1[i] != bytes2[i]:
            diffs.append(i)
    
    # Handle length differences
    if len(bytes1) != len(bytes2):
        diffs.extend(range(min_len, max_len))
        print(f"Warning: Strings have different lengths ({len(bytes1)} vs {len(bytes2)})")
    
    print(f"\nChanges found at {len(diffs)} position(s): {diffs}")
    
    # Create colored versions showing differences
    def add_color_highlight(text, diff_positions, color, context=context_chars):
        if not diff_positions:
            return text
        
        result = []
        i = 0
        while i < len(text):
            if i in diff_positions:
                # Find consecutive differences
                j = i
                while j < len(text) and j in diff_positions:
                    j += 1
                
                # Add context before
                start_context = max(0, i - context)
                if start_context < i:
                    result.append(text[start_context:i])
                
                # Add colored differences
                result.append(color + text[i:j] + reset_color)
                i = j
            else:
                result.append(text[i])
                i += 1
        
        return ''.join(result)
    
    # Display results
    print(f"\n{str1_name} with differences highlighted:")
    colored1 = add_color_highlight(str1_display, diffs, color_code)
    print(colored1)
    
    print(f"\n{str2_name} with differences highlighted:")
    colored2 = add_color_highlight(str2_display, diffs, color_code)
    print(colored2)
    
    # Show side-by-side comparison for small differences
    if len(diffs) <= 10:
        print(f"\nDetailed side-by-side comparison:")
        for pos in diffs[:10]:  # Limit to first 10 differences
            if pos < len(str1_display) and pos < len(str2_display):
                char1 = str1_display[pos] if pos < len(str1_display) else 'N/A'
                char2 = str2_display[pos] if pos < len(str2_display) else 'N/A'
                print(f"  Position {pos}: '{char1}' vs '{char2}'")
    
    return diffs, bytes1, bytes2

def hash_with_append(data1, data2, append_data=b"hello", hash_algorithm='md5'):
    """
    Append data to both inputs and compute hashes.
    
    Args:
        data1: First data (bytes)
        data2: Second data (bytes)
        append_data: Data to append (bytes)
        hash_algorithm: Hash algorithm ('md5', 'sha1', 'sha256')
    """
    
    # Select hash algorithm
    if hash_algorithm == 'md5':
        hasher = hashlib.md5
    elif hash_algorithm == 'sha1':
        hasher = hashlib.sha1
    elif hash_algorithm == 'sha256':
        hasher = hashlib.sha256
    else:
        raise ValueError(f"Unsupported hash algorithm: {hash_algorithm}")
    
    # Compute hashes
    h1 = hasher()
    h2 = hasher()
    
    h1.update(data1 + append_data)
    h2.update(data2 + append_data)
    
    hash1 = h1.hexdigest()
    hash2 = h2.hexdigest()
    
    print(f"\nHash results with appended data '{append_data.decode()}' using {hash_algorithm}:")
    print(f"Data 1 + append: {hexlify(data1 + append_data)}")
    print(f"Hash: {hash1}")
    print(f"Data 2 + append: {hexlify(data2 + append_data)}")
    print(f"Hash: {hash2}")
    
    if hash1 == hash2:
        print("✓ Hashes are IDENTICAL")
    else:
        print("✗ Hashes are DIFFERENT")
    
    return hash1, hash2

# Example usage
if __name__ == "__main__":
    # Compare the hexadecimal strings
    diffs, m1, m2 = compare_strings_with_color(
        m1_hex, 
        m2_hex, 
        str1_name="Message 1", 
        str2_name="Message 2",
        encoding='hex',
        highlight_color='red',
        context_chars=3
    )
    
    # Hash with appended data
    hash1, hash2 = hash_with_append(m1, m2, b"hello", 'md5')
    
    # Example with text strings
    print("\n" + "="*60)
    print("EXAMPLE WITH TEXT STRINGS:")
    
    text1 = "The quick brown fox jumps over the lazy dog"
    text2 = "The quick brown fox jumps over the lazy cat"
    
    compare_strings_with_color(
        text1,
        text2,
        str1_name="Text 1",
        str2_name="Text 2", 
        encoding='text',
        highlight_color='yellow'
    )