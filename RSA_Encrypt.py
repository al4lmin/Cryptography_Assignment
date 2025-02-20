def encrypt():
    # Read public key from file (hex format)
    with open("public_key.txt", "r") as pub:
        e, n = [int(line.strip(), 16) for line in pub.readlines()]

    # Get 16-byte symmetric key from user
    plaintext_hex = input("Enter 16-byte symmetric key in hex: ")
    if len(plaintext_hex) != 32:
        raise ValueError("Invalid input! Must be exactly 16 bytes (32 hex characters).")

    # Convert hex to integer
    plaintext_bytes = bytes.fromhex(plaintext_hex)
    plaintext_int = int.from_bytes(plaintext_bytes, byteorder='big')

    # Encrypt using RSA
    ciphertext = pow(plaintext_int, e, n)

    # Convert encrypted integer to hex and save
    hex_ciphertext = format(ciphertext, 'x')

    with open("encrypted_key.txt", "w") as enc_file:
        enc_file.write(hex_ciphertext)

    print(f"Encrypted Key (Hex): {hex_ciphertext}")
    print("Encrypted key saved to encrypted_key.txt")

if __name__ == "__main__":
    encrypt()
