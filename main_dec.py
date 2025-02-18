
def decrypt_key(ciphertext, sym_key):
    return bytearray(ciphertext[i] ^ sym_key[i] for i in range(len(ciphertext)))

def decrypt_iv(ciphertext, iv_key):
    return [chr(ciphertext[i] ^ iv_key[i]) for i in range(len(ciphertext))]

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

def combineMessage(plaintext_list):
    flat_list = ["".join(block) for block in plaintext_list]  # Convert to string
    return "".join(flat_list).rstrip()  

def load_ciphertext(filename="ciphertext.txt"):
    with open(filename, "r") as f:
        return [bytearray(eval(line.strip())) for line in f.readlines()]


def save_plaintext(plaintext_list, filename="plaintext.txt"):
    with open(filename, "w") as f:
        for block in plaintext_list:
            f.write("".join(block))


def main():
    ciphertext_list = load_ciphertext()

    sym_key = b"7183ed5a7dbcfdeb"  # Manually set the key in form of bytes
    iv_key = b"13d73a9b6e2e32e4"   # Manually set the key in form of bytes

    plaintext_list = decrypt_ciphertext(ciphertext_list, sym_key, iv_key)
    print("Decrypted Blocks:", plaintext_list)

    message = combineMessage(plaintext_list)
    print("Decrypted Message:", message)

    save_plaintext(plaintext_list)

main()
