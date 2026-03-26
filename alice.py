from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import base64
import json
import socket

user_input = input("Input plaintext: ")
plaintext = user_input.encode()

#ciphertext AES-256-CBC
key = os.urandom(32)  #AES-256
iv = os.urandom(16)

pad_len = 16 - len(plaintext) % 16
plaintext_padded = plaintext + bytes([pad_len]) * pad_len

cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(plaintext_padded)


print("Plaintext:", plaintext.decode())
print("Ciphertext:", base64.b64encode(ciphertext).decode())
print("IV:", base64.b64encode(iv).decode())
print("Key:", base64.b64encode(key).decode())

#hash
hash_obj = SHA256.new(plaintext)
hash_bytes = hash_obj.digest()

hash_hex = hash_bytes.hex()

print("Hash:", hash_hex)

#signature
with open("keys/alice_private.pem", "rb") as f:
    alice_private_key = RSA.import_key(f.read())
    
signature = pkcs1_15.new(alice_private_key).sign(hash_obj)  
signature_b64 = base64.b64encode(signature).decode()

print("Signature:", signature_b64)

#load public key bob
with open("keys/bob_public.pem", "rb") as f:
    bob_public_key = RSA.import_key(f.read())
    
rsa_cipher = PKCS1_OAEP.new(bob_public_key)
encrypted_key = rsa_cipher.encrypt(key)
encrypted_key_b64 = base64.b64encode(encrypted_key).decode()

print("Encrypted Key:", encrypted_key_b64)

#payload
def send_b64(data):
    return base64.b64encode(data).decode()

ciphertext_b64 = send_b64(ciphertext)
encrypted_key_b64 = send_b64(encrypted_key)
signature_b64 = send_b64(signature)
iv_b64 = send_b64(iv)
hash_hex = hash_bytes.hex()
payload = {
  "source_ip": "127.0.0.1",
  "destination_ip": "127.0.0.2",
  "ciphertext": ciphertext_b64,
  "encrypted_key": encrypted_key_b64,
  "hash": hash_hex,
  "signature": signature_b64,
  "iv": iv_b64,
  "algorithm": {
    "symmetric": "AES-256-CBC",
    "asymmetric": "RSA",
    "hash": "SHA-256"
  }
}

payload_json = json.dumps(payload)

print("\n===== PAYLOAD ======")
print(payload_json)

#socket programming
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.2", 5000)) #IP Bob
client.send(payload_json.encode())
client.close()
print("\nPayload sent to Bob")