#pip install pyCryptodome
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import time

#AES Decryption
def decryption(ciphertext, sym_key, iv):
    cipher = AES.new(sym_key, AES.MODE_CBC, iv)
    start_time = time.perf_counter()
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    end_time = time.perf_counter()
    return plaintext.decode(), end_time - start_time
    
def load_ciphertext(filename="ciphertext.txt"):
    with open(filename, "rb") as f:
        ciphertext = f.read()
    return ciphertext

def save_plaintext(plaintext, filename="decrypted.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write (plaintext)

#Bit Error
def corrupt_decrypt(corrupted, sym_key, iv):
    cipher = AES.new(sym_key, AES.MODE_CBC, iv)
    try:
        # For ease to see the decryption
        # plaintext1 = cipher.decrypt(corrupted)
        # print ("Partial Decrypt:", plaintext1)
        # plaintext = unpad(plaintext1, AES.block_size)

        # Normal CBC
        plaintext = unpad(cipher.decrypt(corrupted), AES.block_size)
        return plaintext.decode()
    except Exception as e:
        return f"Decryption Error: {e}"

def load_corrupt(filename="corrupted.txt"):
    with open(filename, "rb") as f:
        corrupted = f.read()
    return corrupted

def save_corrupt(corrupted, filename="corrupt_decrypt.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write (corrupted)

def main():
    sym_key = b"7183ed5a7dbcfdeb"   #manually set
    iv = b"13d73a9b6e2e32e4"        #manually set

    receive = load_ciphertext()
    corrupted = load_corrupt()

    decrypted, dec_time = decryption (receive, sym_key, iv)
    print(f"Decryption Time: {dec_time:.6f} seconds")
    print("Decrypted:", decrypted)

    error_decrypt = corrupt_decrypt(corrupted, sym_key, iv)
    print(error_decrypt)

    save_plaintext(decrypted)
    save_corrupt(error_decrypt)

main()