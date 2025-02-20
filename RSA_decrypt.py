def decrypt():
    # Read private key from file (hex format)
    with open("private_key.txt", "r") as priv:
        d, n = [int(line.strip(), 16) for line in priv.readlines()]

    # Read encrypted key from file (hex format)
    with open("encrypted_key.txt", "r") as enc_file:
        ciphertext = int(enc_file.read().strip(), 16)  # Convert hex back to int

    # Decrypt using RSA
    decrypted_int = pow(ciphertext, d, n)

    # Convert integer back to bytes
    decrypted_bytes = decrypted_int.to_bytes(16, byteorder='big')
    decrypted_hex = decrypted_bytes.hex()

    # Save decrypted data
    with open("decrypted_key.txt", "w") as dec_file:
        dec_file.write(decrypted_hex)

    print(f"Decrypted Key: {decrypted_hex}")
    print("Decrypted key saved to decrypted_key.txt")

if __name__ == "__main__":
    decrypt()
