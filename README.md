# Secure Message Delivery (Alice & Bob)

Project ini merupakan tugas mata kuliah II3230 Keamanan Informasi yang dibuat oleh **Farella Kamala Budianto (18223046)** dan **Kenlyn Tesalonika Winata (18223098)** untuk implementasi sistem komunikasi yang dilakukan antara Alice (client) dan Bob (server) menggunakan pendekatan **hybrid cryptography** yang menggabungkan:
- AES-256-CBC → untuk enkripsi pesan
- RSA → untuk enkripsi kunci AES & digital signature
- SHA-256 → untuk menjaga integritas data
Untuk menjamin **confidentiality**, **integrity**, dan **authenticity**.

---

## Arsitektur Sistem

- Alice → Client (`127.0.0.1`)
- Bob → Server (`127.0.0.2`, port 5000)
- Komunikasi menggunakan **TCP/IP socket**
- Data dikirim dalam format **JSON payload**

---

## Struktur Payload

```json
{
  "source_ip": "127.0.0.1",
  "destination_ip": "127.0.0.2",
  "ciphertext": "...",
  "encrypted_key": "...",
  "hash": "...",
  "signature": "...",
  "iv": "...",
  "algorithm": {
    "symmetric": "AES-256-CBC",
    "asymmetric": "RSA",
    "hash": "SHA-256"
  }
}
```
Semua data biner dikonversi ke Base64 agar bisa dikirim melalui socket.

---

## Requirements

Pastikan bahwa perangkat telah memenuhi kebutuhan berikut:
- Python 3 dan OpenSSL sudah terunduh
- Library yang diperlukan telah terunduh, dengan cara mengetik ini pada bash:

```bash
pip install pycryptodome
```

---

## Generate Key

Sebelum menjalankan program, kita perlu mengenerate key untuk Alice dan Bob dengan kode berikut:

```bash
openssl genrsa -out keys/alice_private.pem 2048
openssl rsa -in keys/alice_private.pem -pubout -out keys/alice_public.pem

openssl genrsa -out keys/bob_private.pem 2048
openssl rsa -in keys/bob_private.pem -pubout -out keys/bob_public.pem
```

alice_private.pem akan digunakan untuk membuat digital signature, alice_public.pem akan digunakan Bob untuk verifikasi signature, bob_public.pem akan digunakan Alice untuk mengenkripsi AES key, dan bob_private.pem akan digunakan Bob untuk mendekripsi AES key.

*Folder keys/ tidak disertakan di repository (sudah di .gitignore) untuk keamanan.

```
├── alice.py
├── bob.py
├── keys/
│   ├── alice_private.pem
│   ├── alice_public.pem
│   ├── bob_private.pem
│   └── bob_public.pem
```

---

## Menjalankan Program

1. Menjalankan Bob (Server)
```bash
python bob.py
```
Bob akan listening di 127.0.0.2:5000 dan menunggu koneksi dari Alice

2. Menjalankan Alice (Client)
```bash
python alice.py
```
Di sini Alice akan mengenerate AES key secara acak, mengenkripsi plaintext (AES-256-CBC), mengenkripsi AES key (RSA), membuat hash (SHA-256), membuat digital signature, dan mengirimkan payload ke Bob.

