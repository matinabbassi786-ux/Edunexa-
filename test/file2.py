
import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

key = base64.b64decode(input("Enter KEY: "))
text = input("Enter message: ")

nonce = os.urandom(12)

encrypted = AESGCM(key).encrypt(
    nonce, text.encode(), None
)

# Include nonce internally with encrypted data
result = nonce + encrypted

print("ENCRYPTED:", base64.b64encode(result).decode())
