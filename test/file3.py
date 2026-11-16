
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

key = base64.b64decode(input("Enter KEY: "))
encrypted = base64.b64decode(input("Enter ENCRYPTED DATA: "))

nonce = encrypted[:12]
ciphertext = encrypted[12:]

try:
    original = AESGCM(key).decrypt(
        nonce, ciphertext, None
    )

    print("DECRYPTED:", original.decode())

except Exception:
    print("Wrong key or modified data!")
