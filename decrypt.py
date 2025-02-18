import json

# RSA decryption function
def decrypt(ciphertext, d, n):
    return pow(ciphertext, d, n)

def main():
    # Load RSA keys
    with open("rsa_keys.json", "r") as file:
        keys = json.load(file)

    d, n = keys["d"], keys["n"]

    # Read the encrypted key from the file
    with open("encrypted_key.txt", "r") as file:
        hex_cipher = file.read().strip()

    ciphertext = int(hex_cipher, 16)

    # Decrypt the ciphertext
    decrypted_int = decrypt(ciphertext, d, n)
    decrypted_bytes = decrypted_int.to_bytes(8, byteorder='big')
    decrypted_hex = decrypted_bytes.hex()

    print(f"Decrypted Key: {decrypted_hex}")

if __name__ == "__main__":
    main()
