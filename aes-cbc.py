from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# AES Encryption (Reads from file, encrypts, and saves)
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

# AES Decryption (Reads encrypted file, decrypts, and saves)
def aes_cbc_decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        raw_data = f.read()

    iv, ciphertext = raw_data[:16], raw_data[16:]  # Extract IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    try:
        decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(decrypted.decode())
        print(f"Decryption complete! Plaintext saved to {output_file}")
    except:
        print(f"Decryption failed! Corrupted ciphertext caused padding error.")

# Introduce a Bit Error in Ciphertext
def introduce_bit_error(input_file, output_file, byte_index=20, bit_position=1):
    with open(input_file, 'rb') as f:
        ciphertext = bytearray(f.read())

    # Flip a single bit
    ciphertext[byte_index] ^= (1 << bit_position)

    with open(output_file, 'wb') as f:
        f.write(ciphertext)

    print(f"Bit error introduced in {output_file} at byte index {byte_index}, bit position {bit_position}.")

# Example Usage
key = b'16bytesAESkey!!!'  # Ensure this is 16, 24, or 32 bytes
plaintext_file = "plaintext.txt"
ciphertext_file = "ciphertext.txt"
decrypted_file = "decrypted.txt"
corrupted_ciphertext_file = "corrupted_ciphertext.txt"
corrupted_decrypted_file = "corrupted_decrypted.txt"

# Encrypt the plaintext file
aes_cbc_encrypt_file(plaintext_file, ciphertext_file, key)

# Decrypt normally
aes_cbc_decrypt_file(ciphertext_file, decrypted_file, key)

# Introduce bit errors in the ciphertext file
introduce_bit_error(ciphertext_file, corrupted_ciphertext_file)

# Decrypt the corrupted ciphertext
aes_cbc_decrypt_file(corrupted_ciphertext_file, corrupted_decrypted_file, key)
