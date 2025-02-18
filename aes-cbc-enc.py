from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

def aes_cbc_encrypt_file(input_file, output_file, key):
    with open(input_file, 'r', encoding='utf-8') as f:
        plaintext = f.read()

    iv = os.urandom(16)  # Generate a random IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))

    # Save IV + Ciphertext (binary format)
    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext)

    print(f"Encryption complete! Ciphertext saved to {output_file}")

# Example Usage
key = b'16bytesAESkey!!!'  # Ensure this is 16, 24, or 32 bytes
plaintext_file = "plaintext.txt"
ciphertext_file = "ciphertext.enc"

aes_cbc_encrypt_file(plaintext_file, ciphertext_file, key)
