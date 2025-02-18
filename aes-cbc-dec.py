from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

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

# Example Usage
key = b'16bytesAESkey!!!'  # Must match the encryption key
ciphertext_file = "ciphertext.enc"
decrypted_file = "decrypted.txt"

aes_cbc_decrypt_file(ciphertext_file, decrypted_file, key)
