#pip install pyCryptodome
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import random
import time

#AES Encryption
def encryption(plaintext, sym_key, iv):
    cipher = AES.new(sym_key, AES.MODE_CBC, iv)
    start_time = time.perf_counter()
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    end_time = time.perf_counter()
    return ciphertext, end_time - start_time

def load_plaintext(filename="plaintext.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        plaintext = f.read()
    return plaintext

def save_ciphertext(ciphertext, filename="ciphertext.txt"):
    with open(filename, "wb") as f:
        f.write (ciphertext)

#Bit Error
def bit_error(ciphertext, filename="corrupted.txt"):
    
    ciphertext = bytearray(ciphertext)

    byteIndex = random.randint(0, len(ciphertext) - 1)
    bitIndex = random.randint(0, 7)

    ciphertext[byteIndex] ^= (1 << bitIndex)

    print(f"Bit error introduced at byte {byteIndex}, bit {bitIndex}")

    with open(filename, "wb") as f:
        f.write (ciphertext)

    return bytes(ciphertext)

def main():
    plaintext = load_plaintext()
    print("Plaintext:", plaintext)

    sym_key = b"7183ed5a7dbcfdeb"   #manually set
    iv = b"13d73a9b6e2e32e4"        #manually set

    ciphertext, enc_time = encryption (plaintext, sym_key, iv)
    print(f"Encryption Time: {enc_time:.6f} seconds")
    print("Ciphertext:", ciphertext)

    save_ciphertext(ciphertext)
    bit_error(ciphertext)

main()