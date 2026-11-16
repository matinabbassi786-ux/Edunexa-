
import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Generate ONE key
key = AESGCM.generate_key(bit_length=256)

print("KEY:", base64.b64encode(key).decode())

text = input("Enter message: ")

nonce = os.urandom(12)

encrypted = AESGCM(key).encrypt(
    nonce,
    text.encode(),
    None
)

print("\nNONCE:", base64.b64encode(nonce).decode())
print("ENCRYPTED:", base64.b64encode(encrypted).decode())
'''
KEY: KLUiNo0lUyg4jwfKevUAlC2JRC0Z70LP0O5pUauTP1Y=
Enter message: hello
NONCE: /HDdXftuyBe/ryuh
ENCRYPTED: o9l8GeB5pWh9JCY9lHDPT/6y11/j
'''