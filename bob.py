import json, socket, base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

# Coba coba pake file dummy
# with open("payload_sample.json", "r") as f:
#     payload = json.load(f)
# print(f"[BOB] Payload:\n{payload}")

# Buat server socket buat nerima payload
HOST = '127.0.0.2'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print("[Bob] Listening...")

conn, addr = server.accept()
print(f'[BOB] Terhubung dengan {addr}')

data = conn.recv(8192).decode()
conn.close()

# Parse JSON dan ambil data yang diperluin
payload = json.loads(data)
print(f"[BOB] Payload berhasil diterima:\n{json.dumps(payload, indent=2)}")

ciphertext_b64 = payload["ciphertext"]
ecrypted_key_b64 = payload["encrypted_key"]
iv_b64 = payload["iv"]
hash_received = payload["hash"]
signature_b64 = payload["signature"]

# Decode
ciphertext = base64.b64decode(ciphertext_b64)
encrypted_key = base64.b64decode(ecrypted_key_b64)
iv = base64.b64decode(iv_b64)
signature = base64.b64decode(signature_b64)

# Decrypt 
with open ("keys/bob_private.pem", "rb") as f:
    private_key = RSA.import_key(f.read())

rsa_cipher = PKCS1_OAEP.new(private_key)
aes_key = rsa_cipher.decrypt(encrypted_key)
print(f"\n[BOB] Simetric key berhasil didekripsi")

cipher = AES.new(aes_key, AES.MODE_CBC, iv)
plaintext_padded = cipher.decrypt(ciphertext)
print(f"\n[BOB] Ciphertext berhasil didekripsi")

# Unpadding
pad_len = plaintext_padded[-1]
plaintext = plaintext_padded[:-pad_len]

print(f"[BOB] Plaintext: {plaintext.decode()}")

# Hash verification
hash_plaintext = SHA256.new(plaintext)
computed_hash = hash_plaintext.hexdigest()

print("\n[BOB] Hash verification:")
print("Received:", hash_received)
print("Computed: ", computed_hash)

if computed_hash == hash_received:
    print("Hash Valid")
else:
    print("Hash Invalid")

# Signature verification
with open ("keys/alice_public.pem", "rb") as f:
    alice_public_key = RSA.import_key(f.read())

print("\n[BOB] Signature verification...")

try:
    pkcs1_15.new(alice_public_key).verify(hash_plaintext, signature)
    print("Signature Valid\n")
except:
    print("Signature Invalid\n")

# Kesimpulan
if (computed_hash == hash_received) and (pkcs1_15.new(alice_public_key).verify(hash_plaintext, signature) is None):
    print("Pesan valid dan asli (Integrity dan Authenticity terjamin)\n")