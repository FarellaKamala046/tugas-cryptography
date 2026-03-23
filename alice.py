from Crypto.Cipher import AES
import os

plaintext = "Bob, cek situasi di lokasi X".encode()

key = os.urandom(32)  # AES-256
iv = os.urandom(16)

pad_len = 16 - len(plaintext) % 16
plaintext_padded = plaintext + bytes([pad_len]) * pad_len

cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(plaintext_padded)

import base64

print("Plaintext:", plaintext.decode())
print("Ciphertext:", base64.b64encode(ciphertext).decode())
print("IV:", base64.b64encode(iv).decode())
print("Key:", base64.b64encode(key).decode())