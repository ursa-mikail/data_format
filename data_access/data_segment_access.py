import json
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hmac import HMAC
from cryptography.hazmat.backends import default_backend

# Display helpers
def display_hex_str(byte_str): return byte_str.hex()
def indent_display_json(json_str): return json.dumps(json.loads(json_str), indent=4)

# Keys
aes_key = os.urandom(32)
hmac_key_before = os.urandom(16)
hmac_key_after = os.urandom(16)

def encrypt_and_hmac(data: str, aes_key: bytes, hmac_key_before: bytes, hmac_key_after: bytes) -> bytes:
    # --- HMAC before encryption ---
    hmac_before = HMAC(hmac_key_before, hashes.SHA256(), backend=default_backend())
    hmac_before.update(data.encode())
    hmac_before_value = hmac_before.finalize()

    # Append HMAC before encryption to plaintext
    combined = data.encode() + hmac_before_value

    # --- AES-GCM encryption ---
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(combined) + encryptor.finalize()
    encrypted_data = iv + encryptor.tag + ciphertext

    # --- HMAC after encryption ---
    hmac_after = HMAC(hmac_key_after, hashes.SHA256(), backend=default_backend())
    hmac_after.update(encrypted_data)
    hmac_after_value = hmac_after.finalize()

    # Return encrypted data + appended HMAC
    return encrypted_data + hmac_after_value

def decrypt_and_verify(encrypted_payload: bytes, aes_key: bytes, hmac_key_before: bytes, hmac_key_after: bytes) -> str:
    # --- Split HMAC after ---
    hmac_after_value = encrypted_payload[-32:]
    encrypted_data = encrypted_payload[:-32]

    # --- Verify HMAC after encryption ---
    hmac_after = HMAC(hmac_key_after, hashes.SHA256(), backend=default_backend())
    hmac_after.update(encrypted_data)
    hmac_after.verify(hmac_after_value)

    # --- Split encryption components ---
    iv = encrypted_data[:12]
    tag = encrypted_data[12:28]
    ciphertext = encrypted_data[28:]

    # --- AES-GCM decryption ---
    cipher = Cipher(algorithms.AES(aes_key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(ciphertext) + decryptor.finalize()

    # --- Split data and HMAC before ---
    data, hmac_before_value = decrypted[:-32], decrypted[-32:]

    # --- Verify HMAC before encryption ---
    hmac_before = HMAC(hmac_key_before, hashes.SHA256(), backend=default_backend())
    hmac_before.update(data)
    hmac_before.verify(hmac_before_value)

    return data.decode()

# Load profile
with open("profile.json", "r") as f:
    profile = json.load(f)

fields_to_share = ["name", "address", "volunteer_experience"]
shared_profile = {field: profile[field] for field in fields_to_share}
shared_profile_json = json.dumps(shared_profile)

# Encrypt + attach HMACs
final_encrypted_payload = encrypt_and_hmac(shared_profile_json, aes_key, hmac_key_before, hmac_key_after)
print("Encrypted Payload (hex):", display_hex_str(final_encrypted_payload))

json_to_print = json.loads(decrypt_and_verify(final_encrypted_payload, aes_key, hmac_key_before, hmac_key_after))
print("\nDecrypted Profile:", json.dumps(json_to_print, indent=4))

# Make another item to share
print("\n--- Making another item to share ---")
# Extract only the 'organization' field from each volunteer experience entry
shared_profile = {
    "volunteer_experience": [
        {"organization": item["organization"]}
        for item in profile.get("volunteer_experience", [])
        if item.get("organization")
    ]
}
shared_profile_json = json.dumps(shared_profile)

# Encrypt + attach HMACs
final_encrypted_payload = encrypt_and_hmac(shared_profile_json, aes_key, hmac_key_before, hmac_key_after)
print("Encrypted Payload (hex):", display_hex_str(final_encrypted_payload))

json_to_print = json.loads(decrypt_and_verify(final_encrypted_payload, aes_key, hmac_key_before, hmac_key_after))
print("\nDecrypted Profile:", json.dumps(json_to_print, indent=4))


"""
Encrypted Payload (hex): 6205a6d2d874fa51f4bb879b1671358fab1ab3be63935a8f35b6e573d4ab4d696714926bada76798f93ebd20274eac52033391307d9da8c614fe955e51a399e27b03bb1dbed13490d9c133d9702c5dca4377be862b9f129851e78cd3238aec5709bdbf705126b7fa8cafd67b892a81b3a77e350ed005d308b859455c960c0817014e778b621be63e25aca9fbeb39650915b7b853d76ccbca504848067c28e5a0d9e5831c336ec28052a541bf913c5ca66812402b29d9cf3678c30a6c56bb07516dc1978f1a40d5811346abb3d7de4c5b8b84be210a9a43be867d4b28f34631c7e99eb187ba5d91c781af9c31c1fe1b00d3d50836bff3c296135867cac84f536548a805e08f1b0f291b1fb09ad045a3a3295f688c0e0b74c0ad21052bdab0833088fa951fc3cc7b05a6b009fab6b849657cbc2d2dee90de4e6fc8d50045eb9b2e341c37181a35bc925d1a4c667f4a4f20d139aee5b3bbec3744a9447374

Decrypted Profile: {
    "name": "John Doe",
    "address": "1234 Main St, Anytown, USA",
    "volunteer_experience": [
        {
            "organization": "Code for Good",
            "role": "Volunteer Developer",
            "description": "Contributed to open-source projects aimed at social good.",
            "duration": "2019-present"
        }
    ]
}

--- Making another item to share ---
Encrypted Payload (hex): 1059d23f00356b3e1c05d35e6f6bb6a37ef52e9b9d085b650d1419a2c98be9a40115c95b1a8396cbcaf587c46561ed0d13ad3492cfc02392504342cfaa38d020c42e0183433cf1777c3ede8364d0852cab3de86e6a16e381744278197a4254d24ebca4d32c5cf12438ccc6901c47a064deee0abf33f8af6c9f6de7b2bdfafe186f472e000c0ffa3dd6e3beed2fea5bd05e3cf2975d23572dc3

Decrypted Profile: {
    "volunteer_experience": [
        {
            "organization": "Code for Good"
        }
    ]
}
"""