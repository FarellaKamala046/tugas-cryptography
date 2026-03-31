from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
import base64
import json
import socket

print("[ALICE] Starting secure message process...\n")

#input plaintext
# user_input = input("[ALICE] Input plaintext: ")
# plaintext = user_input.encode()

#plaintext
message = "Bob, cek situasi di lokasi X"
plaintext = message.encode()
print(message)

#ciphertext AES-256-CBC
key = os.urandom(32)  #AES-256
iv = os.urandom(16)

pad_len = 16 - len(plaintext) % 16
plaintext_padded = plaintext + bytes([pad_len]) * pad_len

cipher = AES.new(key, AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(plaintext_padded)


print("[ALICE] Plaintext:", plaintext.decode())
print("[ALICE] Ciphertext:", base64.b64encode(ciphertext).decode())
print("[ALICE] IV:", base64.b64encode(iv).decode())
print("[ALICE] AES Key:", base64.b64encode(key).decode())


#hash
hash_obj = SHA256.new(plaintext)
hash_bytes = hash_obj.digest()

hash_hex = hash_bytes.hex()

print("[ALICE] Hash:", hash_hex)

#signature
print("\n[ALICE] Creating digital signature...")
with open("keys/alice_private.pem", "rb") as f:
    alice_private_key = RSA.import_key(f.read())
    
signature = pkcs1_15.new(alice_private_key).sign(hash_obj)  
signature_b64 = base64.b64encode(signature).decode()

print("[ALICE] Signature:", signature_b64)

#encrypt AES key (RSA)
print("\n[ALICE] Encrypting AES key using Bob's public key...")
with open("keys/bob_public.pem", "rb") as f:
    bob_public_key = RSA.import_key(f.read())
    
rsa_cipher = PKCS1_OAEP.new(bob_public_key)
encrypted_key = rsa_cipher.encrypt(key)
encrypted_key_b64 = base64.b64encode(encrypted_key).decode()

print("[ALICE] Encrypted Key:", encrypted_key_b64)

#payload
print("\n[ALICE] Building payload...")
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

payload_json = json.dumps(payload, indent=4)

print("\n===== PAYLOAD ======")
print(payload_json)

#socket programming send to Bob
print("\n[ALICE] Sending payload to Bob...")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.2", 5000)) #IP Bob
client.send(payload_json.encode())
client.close()
print("\nPayload successfully sent to Bob")