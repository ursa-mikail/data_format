"""
🎨 Color Features:
Red: Errors and differences
Green: Success messages and second values in differences
Blue: Original values and file information
Yellow: Warnings and section headers
Magenta: Difference counts
Cyan: Main headers and titles

🔧 Features:
- Works with any strings (hex, text, binary, etc.)
- Side-by-side color comparison
- Length mismatch handling
- Visual difference display
- Collision detection
"""

import hashlib
from binascii import unhexlify, hexlify
import sys

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    PURPLE_VIOLET = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_colored(text, color):
    print(f"{color}{text}{Colors.END}")

def is_hex_string(s):
    """Check if string is valid hexadecimal"""
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

def create_side_by_side_visual(str1, str2, max_line_length=80):
    """Create a color-coded side-by-side visual comparison"""
    # Ensure strings are the same length for comparison
    min_len = min(len(str1), len(str2))
    str1 = str1[:min_len]
    str2 = str2[:min_len]
    
    result = []
    line1 = []
    line2 = []
    diff_line = []
    
    for i in range(min_len):
        char1 = str1[i]
        char2 = str2[i]
        
        if char1 == char2:
            # Same character - show in PURPLE_VIOLET
            line1.append(f"{Colors.PURPLE_VIOLET}{char1}{Colors.END}")
            line2.append(f"{Colors.PURPLE_VIOLET}{char2}{Colors.END}")
            diff_line.append(f"{Colors.PURPLE_VIOLET}│{Colors.END}")
        else:
            # Different character - show in red/green
            line1.append(f"{Colors.RED}{char1}{Colors.END}")
            line2.append(f"{Colors.GREEN}{char2}{Colors.END}")
            diff_line.append(f"{Colors.RED}✘{Colors.END}")
    
    # Combine into side-by-side display
    result.append(f"{Colors.CYAN}String 1:{Colors.END} {''.join(line1)}")
    result.append(f"{Colors.CYAN}Diff Map:{Colors.END} {''.join(diff_line)}")
    result.append(f"{Colors.CYAN}String 2:{Colors.END} {''.join(line2)}")
    
    return "\n".join(result)

def analyze_strings(str1, str2, suffix_word="hello"):
    """Analyze two strings for differences and hash collisions"""
    print_colored(f"String 1 (length: {len(str1)}, type: {'hex' if is_hex_string(str1) else 'text'}):", Colors.BLUE)
    print_colored(str1, Colors.PURPLE_VIOLET)
    
    print_colored(f"String 2 (length: {len(str2)}, type: {'hex' if is_hex_string(str2) else 'text'}):", Colors.BLUE)
    print_colored(str2, Colors.PURPLE_VIOLET)
    
    # Check if strings have same length
    if len(str1) != len(str2):
        print_colored(f"⚠️  Strings have different lengths: {len(str1)} vs {len(str2)}", Colors.YELLOW)
        min_len = min(len(str1), len(str2))
        str1_truncated = str1[:min_len]
        str2_truncated = str2[:min_len]
        print_colored(f"Truncated to common length: {min_len}", Colors.YELLOW)
    else:
        str1_truncated = str1
        str2_truncated = str2
        min_len = len(str1)
    
    # Find differences
    diffs = []
    for i in range(min_len):
        if str1_truncated[i] != str2_truncated[i]:
            diffs.append((i, str1_truncated[i], str2_truncated[i]))
    
    print_colored(f"🔍 Found {len(diffs)} differences", Colors.MAGENTA)
    
    # Show side-by-side comparison
    print_colored("\n🔄 Side-by-Side Comparison:", Colors.BOLD + Colors.CYAN)
    print(create_side_by_side_visual(str1_truncated, str2_truncated))
    
    # Detailed difference report
    if diffs:
        print_colored("\n📊 Detailed differences (first 10):", Colors.BOLD + Colors.GREEN)
        for pos, char1, char2 in diffs[:10]:
            print_colored(f"Position {pos}: '{Colors.RED}{char1}{Colors.END}' → '{Colors.GREEN}{char2}{Colors.END}'", Colors.BLUE)
        
        if len(diffs) > 10:
            print_colored(f"... and {len(diffs) - 10} more differences", Colors.GREEN)
    
    # Compute hashes for different data types
    print_colored("\n🔐 Hash Analysis:", Colors.BOLD + Colors.CYAN)
    
    try:
        # Method 1: Direct string hashing
        hash1_direct = hashlib.md5(str1.encode('utf-8', errors='replace')).hexdigest()
        hash2_direct = hashlib.md5(str2.encode('utf-8', errors='replace')).hexdigest()
        
        print_colored("Direct string hashes (UTF-8 encoded):", Colors.PURPLE_VIOLET)
        print_colored(f"  String 1: {hash1_direct}", Colors.BLUE)
        print_colored(f"  String 2: {hash2_direct}", Colors.BLUE)
        
        # Method 2: With suffix
        suffix = suffix_word.encode('utf-8')
        hash1_with_suffix = hashlib.md5(str1.encode('utf-8', errors='replace') + suffix).hexdigest()
        hash2_with_suffix = hashlib.md5(str2.encode('utf-8', errors='replace') + suffix).hexdigest()
        
        print_colored(f"With suffix '{suffix_word}':", Colors.PURPLE_VIOLET)
        print_colored(f"  String 1: {hash1_with_suffix}", Colors.GREEN)
        print_colored(f"  String 2: {hash2_with_suffix}", Colors.GREEN)
        
        # Method 3: If strings are hex, also compute binary hashes
        if is_hex_string(str1) and is_hex_string(str2):
            try:
                bytes1 = unhexlify(str1)
                bytes2 = unhexlify(str2)
                
                hash1_hex = hashlib.md5(bytes1).hexdigest()
                hash2_hex = hashlib.md5(bytes2).hexdigest()
                
                print_colored("Binary hashes (from hex decoding):", Colors.PURPLE_VIOLET)
                print_colored(f"  String 1: {hash1_hex}", Colors.MAGENTA)
                print_colored(f"  String 2: {hash2_hex}", Colors.MAGENTA)
                
                # Check hex collisions
                if hash1_hex == hash2_hex:
                    print_colored("🎯 HEX COLLISION FOUND!", Colors.BOLD + Colors.RED)
                else:
                    print_colored("✅ No hex collision", Colors.GREEN)
                    
            except Exception as e:
                print_colored(f"⚠️  Hex decoding error: {e}", Colors.YELLOW)
        
        # Check direct string collisions
        if hash1_direct == hash2_direct:
            print_colored("🎯 DIRECT STRING COLLISION FOUND!", Colors.BOLD + Colors.RED)
        else:
            print_colored("✅ No direct string collision", Colors.GREEN)
            
        if hash1_with_suffix == hash2_with_suffix:
            print_colored("🎯 SUFFIX COLLISION FOUND!", Colors.BOLD + Colors.RED)
        else:
            print_colored("✅ No suffix collision", Colors.GREEN)
            
    except Exception as e:
        print_colored(f"❌ Error computing hashes: {e}", Colors.RED)

def demonstrate_various_string_types():
    """Demonstrate analysis with different string types"""
    print_colored("🔍 String Collision Analysis", Colors.BOLD + Colors.CYAN)
    print_colored("=" * 50, Colors.CYAN)
    
    # Test case 1: Hex strings (original use case)
    print_colored("\n📋 Test Case 1: Hexadecimal Strings", Colors.BOLD + Colors.YELLOW)
    hex1 = '0e30656155aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef'
    hex2 = '0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef'
    analyze_strings(hex1, hex2)
    
    # Test case 2: Regular text strings
    print_colored("\n📋 Test Case 2: Text Strings", Colors.BOLD + Colors.YELLOW)
    text1 = "The quick brown fox jumps over the lazy dog"
    text2 = "The quick brown fox jumps over the lazy cog"
    analyze_strings(text1, text2)
    
    # Test case 3: Similar strings with small differences
    print_colored("\n📋 Test Case 3: Similar Strings", Colors.BOLD + Colors.YELLOW)
    similar1 = "Hello World! This is a test string for demonstration."
    similar2 = "Hello World? This is a test string for demonstration!"
    analyze_strings(similar1, similar2)
    
    # Test case 4: Binary-like strings
    print_colored("\n📋 Test Case 4: Binary-like Strings", Colors.BOLD + Colors.YELLOW)
    binary1 = "0101010001101000011010010111001100100000011010010111001100100000011000010010000001110100011001010111001101110100"
    binary2 = "0101010001101000011010010111001100100000011010010111001100100000011000010010000001110100011001010111001101110101"
    analyze_strings(binary1, binary2)

def main():
    print_colored("🚀 Universal String Collision Analyzer", Colors.BOLD + Colors.CYAN)
    print_colored("=" * 60, Colors.CYAN)
    
    try:
        # Run demonstration with various string types
        demonstrate_various_string_types()
        
        # Optional: Custom input
        print_colored("\n🎯 Custom Analysis", Colors.BOLD + Colors.YELLOW)
        custom = input("Perform custom analysis? (y/n): ").lower()
        if custom == 'y':
            str1 = input("Enter first string: ")
            str2 = input("Enter second string: ")
            suffix = input("Enter suffix (or press enter for default 'hello'): ") or "hello"
            analyze_strings(str1, str2, suffix)
            
    except KeyboardInterrupt:
        print_colored("\n⏹️  Operation cancelled by user", Colors.YELLOW)
    except Exception as e:
        print_colored(f"\n💥 Unexpected error: {e}", Colors.RED)
    
    print_colored("\n" + "=" * 60, Colors.CYAN)
    print_colored("Analysis complete! 🎉", Colors.BOLD + Colors.GREEN)

if __name__ == "__main__":
    main()

"""
🚀 Universal String Collision Analyzer
============================================================
🔍 String Collision Analysis
==================================================

📋 Test Case 1: Hexadecimal Strings
String 1 (length: 127, type: hex):
0e30656155aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef
String 2 (length: 128, type: hex):
0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1ef
⚠️  Strings have different lengths: 127 vs 128
Truncated to common length: 127
🔍 Found 105 differences

🔄 Side-by-Side Comparison:
String 1: 0e30656155aa787d00bc6f70bbdfe3404cf03659e704f8534c00ffb659c4c8740cc942feb2da115a3f4155cbb8607497386656d7d1f34a42059d78f5a8dd1ef
Diff Map: ││││││││││✗│✗✗✗✗✗│✗✗✗✗✗✗✗│✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗│✗✗✗✗✗✗✗│✗│✗✗✗✗✗✗✗✗✗✗✗✗│✗✗✗✗✗✗✗✗✗✗│✗✗✗✗✗✗✗│✗✗│✗✗✗✗✗✗✗✗✗✗│✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗│✗✗✗
String 2: 0e306561559aa787d00bc6f70bbdfe3404cf03659e744f8534c00ffb659c4c8740cc942feb2da115a3f415dcbb8607497386656d7d1f34a42059d78f5a8dd1e

📊 Detailed differences (first 10):
Position 10: 'a' → '9'
Position 12: '7' → 'a'
Position 13: '8' → '7'
Position 14: '7' → '8'
Position 15: 'd' → '7'
Position 16: '0' → 'd'
Position 18: 'b' → '0'
Position 19: 'c' → 'b'
Position 20: '6' → 'c'
Position 21: 'f' → '6'
... and 95 more differences

🔐 Hash Analysis:
Direct string hashes (UTF-8 encoded):
  String 1: 97911b3c3227cb9f3cd4827ac5ae73b3
  String 2: 0087c7b4268c88762b2d7fd3d638fc85
With suffix 'hello':
  String 1: 1429c2e8cabb9408b9faff33e70b1817
  String 2: fbefc12621f073d284ad8ecc51fd9909
⚠️  Hex decoding error: Odd-length string
✅ No direct string collision
✅ No suffix collision

📋 Test Case 2: Text Strings
String 1 (length: 43, type: text):
The quick brown fox jumps over the lazy dog
String 2 (length: 43, type: text):
The quick brown fox jumps over the lazy cog
🔍 Found 1 differences

🔄 Side-by-Side Comparison:
String 1: The quick brown fox jumps over the lazy dog
Diff Map: ││││││││││││││││││││││││││││││││││││││││✗││
String 2: The quick brown fox jumps over the lazy cog

📊 Detailed differences (first 10):
Position 40: 'd' → 'c'

🔐 Hash Analysis:
Direct string hashes (UTF-8 encoded):
  String 1: 9e107d9d372bb6826bd81d3542a419d6
  String 2: 1055d3e698d289f2af8663725127bd4b
With suffix 'hello':
  String 1: 0a4cd50e41fd20172b70231c6f75ec29
  String 2: 2c3a744bac4b11d2cbc9bb7a0bd39542
✅ No direct string collision
✅ No suffix collision

📋 Test Case 3: Similar Strings
String 1 (length: 53, type: text):
Hello World! This is a test string for demonstration.
String 2 (length: 53, type: text):
Hello World? This is a test string for demonstration!
🔍 Found 2 differences

🔄 Side-by-Side Comparison:
String 1: Hello World! This is a test string for demonstration.
Diff Map: │││││││││││✗││││││││││││││││││││││││││││││││││││││││✗
String 2: Hello World? This is a test string for demonstration!

📊 Detailed differences (first 10):
Position 11: '!' → '?'
Position 52: '.' → '!'

🔐 Hash Analysis:
Direct string hashes (UTF-8 encoded):
  String 1: 47a4dd8b6c0b4b55745c2b4c562ced19
  String 2: a3bf80fd090d89e0536002b9b2664ae0
With suffix 'hello':
  String 1: 6095fbbe484e32b8442fb21d2302efbc
  String 2: 49c24e63f9d818805292b85b6b5eda10
✅ No direct string collision
✅ No suffix collision

📋 Test Case 4: Binary-like Strings
String 1 (length: 112, type: hex):
0101010001101000011010010111001100100000011010010111001100100000011000010010000001110100011001010111001101110100
String 2 (length: 112, type: hex):
0101010001101000011010010111001100100000011010010111001100100000011000010010000001110100011001010111001101110101
🔍 Found 1 differences

🔄 Side-by-Side Comparison:
String 1: 0101010001101000011010010111001100100000011010010111001100100000011000010010000001110100011001010111001101110100
Diff Map: │││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││││✗
String 2: 0101010001101000011010010111001100100000011010010111001100100000011000010010000001110100011001010111001101110101

📊 Detailed differences (first 10):
Position 111: '0' → '1'

🔐 Hash Analysis:
Direct string hashes (UTF-8 encoded):
  String 1: 008392ba1da5735c5476e1a2f46c6817
  String 2: 105a0ed41bc0a3c41bfce7daa69b55ea
With suffix 'hello':
  String 1: 13c02dfb7955b0addb0c6827dbd0693f
  String 2: 99af200a4005dd8d6c13262025e2531a
Binary hashes (from hex decoding):
  String 1: 81aa58dd76412f4818fcc5698167f0f7
  String 2: 23599acdd8df8ef0beb9bda8f6661c31
✅ No hex collision
✅ No direct string collision
✅ No suffix collision

🎯 Custom Analysis
Perform custom analysis? (y/n): n

============================================================
Analysis complete! 🎉
"""    