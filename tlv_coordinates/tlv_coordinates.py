import hashlib
import hmac

def generate_hmac(key, message):
    return hmac.new(key, message.encode('utf-8'), hashlib.sha256).hexdigest()

def get_hmac(tlv, hmac_key):
    """
    Get the HMAC for the given TLV string.
    """
    return generate_hmac(hmac_key, tlv)

def verify_hmac(tlv, received_hmac, hmac_key):
    """
    Verify the HMAC for the given TLV string.
    """
    expected_hmac = get_hmac(tlv, hmac_key)
    return hmac.compare_digest(received_hmac, expected_hmac)

def encode_tlv(field_tag, x, y, r, c, index, hmac_key):
    """
    Encode the given parameters into a TLV formatted string with HMAC.
    """
    # Ensure field_tag is 4 characters
    field_tag = f"{field_tag:>4}"[:4]

    # Ensure x and y are 3 characters, padded with zeros
    x = f"x{x:03d}"
    y = f"y{y:03d}"

    # Ensure r and c are 1 character
    r = f"r{r:01d}"
    c = f"c{c:01d}"

    # Combine value components
    value = f"{x}{y}{r}{c}{index}"

    # Calculate length of the value
    length = len(value)
    length_str = f"len={length}"

    # Combine all parts into a TLV string
    tlv = f"tag={field_tag};value=[{value}];{length_str}"

    # Generate HMAC for integrity
    hmac_value = get_hmac(tlv, hmac_key)
    tlv_with_hmac = f"{tlv};hmac={hmac_value}"

    return tlv_with_hmac

def decode_tlv(tlv_with_hmac, hmac_key):
    """
    Decode the given TLV formatted string with HMAC into its components.
    """
    # Split the TLV and HMAC
    tlv_parts = tlv_with_hmac.split(';')

    if len(tlv_parts) < 4:
        raise ValueError("Invalid TLV format.")

    tag_part = tlv_parts[0]
    value_part = tlv_parts[1]
    length_part = tlv_parts[2]
    received_hmac = tlv_parts[3].split('=')[1]

    # Reconstruct the original TLV string (excluding the HMAC part)
    tlv = ';'.join(tlv_parts[:3])

    # Verify HMAC
    if not verify_hmac(tlv, received_hmac, hmac_key):
        raise ValueError("HMAC verification failed.")
    else:
        print(f"HMAC verification OK")

    # Extract components from the TLV string
    field_tag = tag_part.split('=')[1]
    value = value_part.split('=')[1].strip('[]')
    length = int(length_part.split('=')[1])

    if len(value) != length:
        raise ValueError("Length verification failed.")
    else:
        print(f"len: { len(value) } OK")

    # Extract coordinates and indices from value
    x = int(value[1:4])
    y = int(value[5:8])
    r = int(value[9])
    c = int(value[11])
    index = int(value[12:])

    return field_tag, x, y, r, c, index, length

# Example usage
field_tag = "#111"
x = 12
y = 34
r = 1
c = 2
index = 123
hmac_key = b'secret_hmac_key'

# Encode the TLV with HMAC
tlv_encoded = encode_tlv(field_tag, x, y, r, c, index, hmac_key)
print(f"TLV Encoded: {tlv_encoded}")

# Decode the TLV and verify HMAC
decoded = decode_tlv(tlv_encoded, hmac_key)
print(f"Decoded TLV: {decoded}")

"""
TLV Encoded: tag=#111;value=[x012y034r1c2123];len=15;hmac=78deb07638cd360d461ee1e07c41489f6222b4c4e374639728d6237cf6efd548
HMAC verification OK
len: 15 OK
Decoded TLV: ('#111', 12, 34, 1, 2, 123, 15)

"""