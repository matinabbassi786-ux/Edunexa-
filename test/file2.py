
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

print("--- EDUNEXA DECRYPTION ---")

# Enter values printed by file1.py
key = base64.b64decode(input("Enter KEY: "))
nonce = base64.b64decode(input("Enter NONCE: "))
encrypted = base64.b64decode(input("Enter ENCRYPTED DATA: "))

try:
    original = AESGCM(key).decrypt(nonce, encrypted, None)

    print("\nDecryption successful!")
    print("Original message:", original.decode("utf-8"))

except Exception as error:
    print("\nDecryption failed!")
    print("Reason:", error)
