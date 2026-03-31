# 🔐 End-to-End Secure Message Delivery (Alice & Bob)

Project ini merupakan implementasi sistem komunikasi aman antara Alice (client) dan Bob (server) menggunakan pendekatan **hybrid cryptography**.

Sistem ini menjamin:
- 🔒 Confidentiality (kerahasiaan)
- 🧩 Integrity (keutuhan data)
- ✅ Authenticity (keaslian pengirim)

---

## 📌 Deskripsi Singkat

Alice mengirim pesan ke Bob melalui jaringan dengan cara:
1. Mengenkripsi pesan menggunakan AES-256-CBC
2. Mengenkripsi AES key menggunakan RSA (public key Bob)
3. Membuat hash (SHA-256)
4. Membuat digital signature (private key Alice)
5. Mengirim semua dalam bentuk payload JSON melalui socket

Bob kemudian:
1. Mendekripsi AES key
2. Mendekripsi pesan
3. Memverifikasi hash
4. Memverifikasi digital signature

---

## 🧠 Algoritma yang Digunakan

- **AES-256-CBC** → Enkripsi pesan (confidentiality)
- **RSA-2048** → Enkripsi key & digital signature
- **SHA-256** → Hash untuk integrity
- **Base64 Encoding** → Representasi data biner

---

## 🏗️ Arsitektur Sistem

- Alice → Client (`127.0.0.1`)
- Bob → Server (`127.0.0.2`, port 5000)
- Komunikasi menggunakan **TCP/IP socket**
- Data dikirim dalam format **JSON payload**

---

## 📦 Struktur Payload

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
