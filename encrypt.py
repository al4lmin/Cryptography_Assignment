import json

# RSA encryption function
def encrypt(plaintext_int, e, n):
    return pow(plaintext_int, e, n)

def main():
    # Load RSA keys
    with open("rsa_keys.json", "r") as file:
        keys = json.load(file)

    e, n = keys["e"], keys["n"]

    # Get 8-byte symmetric key from user
    plaintext_hex = input("Enter 8-byte symmetric key in hex: ")
    
    if len(plaintext_hex) != 16:
        print("Error: Input must be exactly 8 bytes (16 hex characters).")
        return

    plaintext_int = int(plaintext_hex, 16)

    # Ensure n is large enough
    if plaintext_int >= n:
        print("Error: RSA modulus n is too small. Regenerate keys with keygen.py.")
        return

    # Encrypt the plaintext
    ciphertext = encrypt(plaintext_int, e, n)
    hex_cipher = format(ciphertext, 'x').zfill(16)  # Ensure at least 8-byte hex

    print(f"Encrypted Key: {hex_cipher}")

    # Save encrypted key to a file
    with open("encrypted_key.txt", "w") as file:
        file.write(hex_cipher)

if __name__ == "__main__":
    main()
