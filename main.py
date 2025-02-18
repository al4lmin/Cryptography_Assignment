import random

def encrypt_iv(plaintext, iv_key):
    return bytearray([ord(plaintext[i]) ^ iv_key[i] for i in range(len(plaintext))])

def encrypt_key(plaintext, sym_key):
    return bytearray(plaintext[i] ^ sym_key[i] for i in range(len(plaintext)))

def decrypt_key(ciphertext, sym_key):
    return bytearray(ciphertext[i] ^ sym_key[i] for i in range(len(ciphertext)))

def decrypt_iv(ciphertext, iv_key):
    return [chr(ciphertext[i] ^ iv_key[i]) for i in range(len(ciphertext))]

def encrypt_plaintext(blockList, sym_key, iv_key):
    list_of_ciphers = []
    for i in range(len(blockList)):
        cipher_iv = encrypt_iv(blockList[i], iv_key)
        cipher_key = encrypt_key(cipher_iv, sym_key)
        list_of_ciphers.append(cipher_key)
        iv_key = cipher_key
    return list_of_ciphers

def decrypt_ciphertext(ciphertext, sym_key, iv_key):
    list_of_plains = []
    for i in range(len(ciphertext)):
        if i == 0:
            temp = decrypt_key(ciphertext[i], sym_key)
            plaintext = decrypt_iv(temp, iv_key)
        else:
            temp = decrypt_key(ciphertext[i], sym_key)
            plaintext = decrypt_iv(temp, ciphertext[i - 1])
        list_of_plains.append(plaintext)
    return list_of_plains

def breakMessage(plaintext, len_of_block):
    list_of_blocks = []
    for i in range(0, len(plaintext), len_of_block):
        block = plaintext[i:i+len_of_block]
        if len(block) == len_of_block:
            list_of_blocks.append(block)
        else:
            pad = len_of_block - len(block)
            for _ in range(pad):
                block = block + " "
            list_of_blocks.append(block)
    return list_of_blocks

def combineMessage(plaintext_list):
    flat_list = ["".join(block) for block in plaintext_list]  # Convert to string
    return "".join(flat_list).rstrip()  

def load_plaintext(filename="plaintext.txt"):
    with open(filename, "r") as f:
        return f.read().replace("\n", "")
    
def load_ciphertext(filename="ciphertext.txt"):
    with open(filename, "r") as f:
        return [bytearray(eval(line.strip())) for line in f.readlines()]
    
def save_ciphertext(ciphertext_list, filename="ciphertext.txt"):
    with open(filename, "w") as f:
        for cipher in ciphertext_list:
            f.write(str(cipher) + "\n")

def save_plaintext(plaintext_list, filename="plaintext.txt"):
    with open(filename, "w") as f:
        for block in plaintext_list:
            f.write("".join(block))

def introduce_error(ciphertext_list):
    if not ciphertext_list: 
        return ciphertext_list #ensure not empty
    
    block_index = random.randint(0, len(ciphertext_list) - 1)               #random block
    byte_index = random.randint(0, len(ciphertext_list[block_index]) - 1)   #random byte
    bit_index = random.randint(0, 7)                                        #random bit

    corrupted_block = bytearray(ciphertext_list[block_index])

    corrupted_block[byte_index] ^= (1 << bit_index)

    ciphertext_list[block_index] = corrupted_block
    print(f"Introduced bit error in block {block_index}, byte {byte_index}, bit {bit_index}")

    return ciphertext_list

def main():
    plaintext = load_plaintext()
    print("Plaintext:", plaintext)

    len_of_block = 8
    blockList = breakMessage(plaintext, len_of_block)
    print("Blocks:", blockList)

    sym_key = b"7183ed5a7dbcfdeb"  # Manually set the key in form of bytes
    iv_key = b"13d73a9b6e2e32e4"   # Manually set the key in form of bytes

    ciphertext_list = encrypt_plaintext(blockList, sym_key, iv_key)
    print("Ciphertext:", ciphertext_list)

    save_ciphertext(ciphertext_list)

    ciphertext_list = load_ciphertext()

    plaintext_list = decrypt_ciphertext(ciphertext_list, sym_key, iv_key)
    print("Decrypted Blocks:", plaintext_list)

    message = combineMessage(plaintext_list)
    print("Decrypted Message:", message)

    save_plaintext(plaintext_list)

    corrupted_ciphertext = introduce_error(ciphertext_list)
    print("Ciphertext after error:", corrupted_ciphertext)

    decrypt_corrupted_ciphertext = decrypt_ciphertext(corrupted_ciphertext, sym_key, iv_key)
    print("\nDecrypted Message with Bit Error: ", combineMessage(decrypt_corrupted_ciphertext))

main()
