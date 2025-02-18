import sys

# Encrypt function: C = P^e mod n
def encrypt(plaintext_hex):
    try:
        with open("public_key.txt", "r") as file:
            e, n = map(int, file.read().strip().split(","))  # Load public key
    except FileNotFoundError:
        print("Error: 'public_key.txt' not found. Run 'keygen.py' first.")
        sys.exit(1)

    plaintext_bytes = bytes.fromhex(plaintext_hex)  # Convert hex to bytes
    plaintext_int = int.from_bytes(plaintext_bytes, byteorder="big")  # Convert to int

    if plaintext_int >= n:
        print("Error: RSA modulus (n) is too small for this input. Generate larger keys.")
        sys.exit(1)

    ciphertext = pow(plaintext_int, e, n)  # Encrypt
    hex_cipher = format(ciphertext, "x").zfill(16)  # Convert to hex

    # Save encrypted key to file
    with open("encrypted_key.txt", "w") as enc_file:
        enc_file.write(hex_cipher)

    print(f"Encrypted Key: {hex_cipher}")
    print("Saved to 'encrypted_key.txt'.")

if __name__ == "__main__":
    plaintext_hex = input("Enter 8-byte symmetric key in hex (e.g., 62b75f90d8dbfd54): ").strip()
    encrypt(plaintext_hex)
