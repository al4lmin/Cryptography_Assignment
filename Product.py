import math
import time

def extended_gcd(a, b):
    """Returns the multiplicative inverse of a modulo b using Extended Euclidean Algorithm."""
    s1, s2, t1, t2 = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        s1, s2 = s2, s1 - q * s2
        t1, t2 = t2, t1 - q * t2
    return s1 % 26

def affine_encrypt(text, k1, k2):
    """Encrypts the text using Affine cipher formula: C = (P * k1 + k2) % 26"""
    encrypted_text = ""
    for char in text.lower():
        if 'a' <= char <= 'z':
            P = ord(char) - ord('a')
            C = (P * k1 + k2) % 26
            encrypted_text += chr(C + ord('A'))
        else:
            encrypted_text += char
    return encrypted_text

def affine_decrypt(text, k1, k2):
    """Decrypts the text using Affine cipher formula: P = (C - k2) * k1^-1 % 26"""
    k1_inv = extended_gcd(k1, 26)
    decrypted_text = ""
    for char in text.upper():
        if 'A' <= char <= 'Z':
            C = ord(char) - ord('A')
            P = (k1_inv * (C - k2)) % 26
            decrypted_text += chr(P + ord('a'))
        else:
            decrypted_text += char
    return decrypted_text

def get_column_order(keyword):
    """Returns the column order based on the alphabetical order of the keyword, handling duplicate letters correctly."""
    sorted_key = sorted(list(keyword))  # Sort keyword alphabetically
    order_map = {}
    
    for index, letter in enumerate(sorted_key):
        if letter in order_map:
            order_map[letter].append(index + 1)
        else:
            order_map[letter] = [index + 1]

    key_order = []
    for letter in keyword:
        key_order.append(order_map[letter].pop(0))  # Assign the next available number for duplicate letters

    return key_order


def create_table(msg, key_order):
    """Creates a matrix for Columnar Transposition."""
    col = len(key_order)
    row = math.ceil(len(msg) / col)
    msg += '_' * ((row * col) - len(msg))  # Padding with '_'
    return [list(msg[i: i + col]) for i in range(0, len(msg), col)]

def columnar_encrypt(msg, keyword):
    """Encrypts the message using Columnar Transposition Cipher."""
    key_order = get_column_order(keyword)
    matrix = create_table(msg, key_order)
    cipher = ""
    print("\nColumnar Transposition Table (Encryption):")
    print("Key Order: ", key_order)
    for row in matrix:
        print(row)
    for idx in sorted(range(len(key_order)), key=lambda k: key_order[k]):
        cipher += ''.join(row[idx] for row in matrix)
    return cipher

def columnar_decrypt(cipher, keyword):
    """Decrypts the message using Columnar Transposition Cipher."""
    key_order = get_column_order(keyword)
    col = len(key_order)
    row = math.ceil(len(cipher) / col)
    expected_size = row * col
    if len(cipher) < expected_size:
        cipher += '_' * (expected_size - len(cipher))
    dec_matrix = [[''] * col for _ in range(row)]
    sorted_indices = sorted(range(len(key_order)), key=lambda k: key_order[k])
    msg_indx = 0
    for sorted_idx in sorted_indices:
        for j in range(row):
            if msg_indx < len(cipher):
                dec_matrix[j][sorted_idx] = cipher[msg_indx]
                msg_indx += 1
    print("\nColumnar Transposition Table (Decryption):")
    print("Key Order: ", key_order)
    for row in dec_matrix:
        print(row)
    return ''.join(sum(dec_matrix, [])).rstrip('_')

def analyze_performance():
    plaintext = input("Enter plaintext: ")
    keyword = input("Enter keyword: ")
    k1  = int(input("Enter k1 (must be co prime t 26):"))
    k2  = int(input("Enter k2: "))  # Example coprime key for Affine Cipher
    
    # Affine Cipher Encryption
    start_time = time.time()
    affine_encrypted = affine_encrypt(plaintext, k1, k2)
    first_trans = columnar_encrypt(affine_encrypted, keyword)
    second_trans = columnar_encrypt(first_trans, keyword)
    encryption_time = time.time() - start_time
    
    print("\nDouble Columnar Transposition Cipher:")
    print("Encrypted Text: ", second_trans)
    
    # Decryption Process
    start_time = time.time()
    decrypted_first = columnar_decrypt(second_trans, keyword)
    decrypted_second = columnar_decrypt(decrypted_first, keyword)
    affine_decrypted = affine_decrypt(decrypted_second, k1, k2)
    decryption_time = time.time() - start_time
    
    print("\nDecrypted Text: ", affine_decrypted)
    print("\nPerformance Analysis:")
    print(f"Encryption Time: {encryption_time:.6f} seconds")
    print(f"Decryption Time: {decryption_time:.6f} seconds")

def main():
    analyze_performance()
    
if __name__ == "__main__":
    main()
