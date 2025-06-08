# Reference: https://symbl.cc/en/unicode-table/#latin-extended-b
# print_data_character_codes.py
import random

def get_codepoint_info(char):
    """Returns a dictionary of various encoding representations of a character."""
    try:
        return {
            'char': repr(char),
            'code_point': f"U+{ord(char):04X}",
            'utf8': char.encode('utf-8'),
            'utf16': char.encode('utf-16'),
            'utf32': char.encode('utf-32'),
            'html_entity': f"&#{ord(char)};",
            'utf8_bytes': [f"0x{b:02X}" for b in char.encode('utf-8')]
        }
    except UnicodeEncodeError:
        return None # Skip characters that can't be encoded

def print_codepoint_info(info):
    """Pretty-prints the encoding information dictionary."""
    if not info:
        return
    print(f"Char       : {info['char']}")
    print(f"Code Point : {info['code_point']}")
    print(f"UTF-8      : {info['utf8']}")
    print(f"UTF-16     : {info['utf16']}")
    print(f"UTF-32     : {info['utf32']}")
    print(f"HTML Entity: {info['html_entity']}")
    print(f"UTF-8 Bytes: {', '.join(info['utf8_bytes'])}")
    print("-" * 50)


def analyze_char(char):
    """Analyze and print a single character."""
    info = get_codepoint_info(char)
    print_codepoint_info(info)


def analyze_codepoint(codepoint):
    """Analyze a Unicode codepoint (int or hex string)."""
    try:
        if isinstance(codepoint, str):
            codepoint = int(codepoint, 16)
        char = chr(codepoint)
        analyze_char(char)
    except (ValueError, TypeError):
        print(f"Invalid codepoint: {codepoint}")


def random_unicode_sample(start=1, end=150_000, window=5):
    """Sample and analyze a window of random codepoints."""
    start_index = random.randint(start, end - window)
    for cp in range(start_index, start_index + window):
        analyze_codepoint(cp)


# Example Usages
if __name__ == "__main__":
    print(">>> Random Unicode Window")
    random_unicode_sample()

    print("\n>>> Analyze U+01E7 (Latin small letter g with caron)")
    code_point = 0x01E7
    analyze_codepoint(code_point)

    print("\n>>> Analyze hex string '01e7'")
    hex_str = '01e7'
    analyze_codepoint(hex_str)

    print("\n>>> Analyze specific non-ASCII character")
    char_to_check = '你'
    analyze_char(char_to_check)

