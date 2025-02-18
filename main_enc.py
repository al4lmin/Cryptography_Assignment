
def encrypt_iv(plaintext, iv_key):
    return bytearray([ord(plaintext[i]) ^ iv_key[i] for i in range(len(plaintext))])

def encrypt_key(plaintext, sym_key):
    return bytearray(plaintext[i] ^ sym_key[i] for i in range(len(plaintext)))

def encrypt_plaintext(blockList, sym_key, iv_key):
    list_of_ciphers = []
    for i in range(len(blockList)):
        cipher_iv = encrypt_iv(blockList[i], iv_key)
        cipher_key = encrypt_key(cipher_iv, sym_key)
        list_of_ciphers.append(cipher_key)
        iv_key = cipher_key
    return list_of_ciphers

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

def load_plaintext(filename="plaintext.txt"):
    with open(filename, "r") as f:
        return f.read().replace("\n", "")
    
def save_ciphertext(ciphertext_list, filename="ciphertext.txt"):
    with open(filename, "w") as f:
        for cipher in ciphertext_list:
            f.write(str(cipher) + "\n")

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

main()
