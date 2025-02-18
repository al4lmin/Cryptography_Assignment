# pip install pyCryptodome
# how to encrypt iv_key ?
from Crypto.Random import get_random_bytes
import random

def decrypt_key (ciphertext, sym_key):
    return bytearray(ciphertext[i] ^ sym_key[i] for i in range(len(ciphertext)))

def decrypt_iv (ciphertext, iv_key):
    return [chr (ciphertext[i] ^ iv_key[i]) for i in range(len(ciphertext))]

def encrypt_iv (plaintext, iv_key):
    return bytearray([ord (plaintext[i]) ^ iv_key[i] for i in range(len(plaintext))])

def encrypt_key (plaintext, sym_key):
    return bytearray(plaintext[i] ^ sym_key[i] for i in range(len(plaintext)))

###########################################################################
def encrypt_plaintext (blockList, sym_key, iv_key):
    list_of_ciphers = []
    for i in range(len(blockList)):
        cipher_iv = encrypt_iv(blockList[i], iv_key)
        cipher_key = encrypt_key(cipher_iv, sym_key)
        list_of_ciphers.append (cipher_key)
        iv_key = cipher_key
    return list_of_ciphers

###########################################################################
def decrypt_ciphertext (ciphertext, sym_key, iv_key):
    list_of_plains = []
    for i in range(len(ciphertext)):
        if i == 0:
            temp = decrypt_key(ciphertext[i], sym_key)
            plaintext = decrypt_iv(temp, iv_key)
        else:
            temp = decrypt_key(ciphertext[i], sym_key)
            plaintext = decrypt_iv(temp, ciphertext[i-1])
        list_of_plains.append(plaintext)
    return list_of_plains

###########################################################################
def combineMessage (plaintext_list):
    flat_list = ["".join(block) for block in plaintext_list] # convert to string
    return "".join(flat_list).rstrip()  

###########################################################################
def breakMessage (plaintext, len_of_block):
    list_of_blocks = []
    for i in range (0, len(plaintext), len_of_block):
        block = plaintext[i:i+len_of_block]
        if (len(block) == len_of_block):
            list_of_blocks.append(block)
        else:
            pad = len_of_block - len(block)
            for i in range (pad):
                block = block + " "
            list_of_blocks.append(block)
    return list_of_blocks

###########################################################################
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

###########################################################################
def main():
    print("Enter a message to encrypt: ")
    plaintext = input()

    len_of_block = 8

    blockList = breakMessage(plaintext, len_of_block)
    print(blockList)

    sym_key = b"0361231230000000" # manually set the key in form of bytes
    iv_key = get_random_bytes(len_of_block)
    print (iv_key)

    ciphertext_list = encrypt_plaintext(blockList, sym_key, iv_key)
    print(ciphertext_list)

    plaintext_list = decrypt_ciphertext(ciphertext_list, sym_key, iv_key)
    print(plaintext_list)

    message = combineMessage(plaintext_list)
    print(message)

    corrupted_ciphertext = introduce_error(ciphertext_list)
    print("Ciphertext after error:", corrupted_ciphertext)
    try:
        decrypt_corrupted_ciphertext = decrypt_ciphertext(corrupted_ciphertext, sym_key, iv_key)
        print("\nDecrypted Message with Bit Error: ", combineMessage(decrypt_corrupted_ciphertext))
    except Exception as e:
        print ("\nDecryption Failed Due to Bit Error:", str(e))

    return

###########################################################################
main()

