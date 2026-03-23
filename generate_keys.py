from Crypto.PublicKey import RSA

def generate_keypair(name):
    key = RSA.generate(2048)

    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open(f"keys/{name}_private.pem", "wb") as f:
        f.write(private_key)

    with open(f"keys/{name}_public.pem", "wb") as f:
        f.write(public_key)

generate_keypair("alice")
generate_keypair("bob")

print("Keys generated!")