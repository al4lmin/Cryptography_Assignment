import sys

# Decrypt function: P = C^d mod n
def decrypt(ciphertext_hex):
    try:
        with open("private_key.txt", "r") as file:
            d, n = map(int, file.read().strip().split(","))  # Load private key
    except FileNotFoundError:
        print("Error: 'private_key.txt' not found. Run 'keygen.py' first.")
        sys.exit(1)

    ciphertext = int(ciphertext_hex, 16)  # Convert hex to int
    plaintext_int = pow(ciphertext, d, n)  # Decrypt
    decrypted_bytes = plaintext_int.to_bytes(8, byteorder="big")  # Convert back to bytes
    decrypted_hex = decrypted_bytes.hex()

    # Save decrypted key to file
    with open("decrypted_key.txt", "w") as dec_file:
        dec_file.write(decrypted_hex)

    print(f"Decrypted Key: {decrypted_hex}")
    print("Saved to 'decrypted_key.txt'.")

if __name__ == "__main__":
    try:
        with open("encrypted_key.txt", "r") as enc_file:
            ciphertext_hex = enc_file.read().strip()  # Read from file
    except FileNotFoundError:
        ciphertext_hex = input("Enter encrypted key in hex: ").strip()

    decrypt(ciphertext_hex)
