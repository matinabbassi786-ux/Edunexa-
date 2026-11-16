
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

key = AESGCM.generate_key(bit_length=256)

print("KEY:", base64.b64encode(key).decode())
