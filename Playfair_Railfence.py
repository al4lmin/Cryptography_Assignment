import time
import numpy as np

# Playfair Cipher 
def generate_playfair_matrix(key):
    key = "".join(dict.fromkeys(key.replace("J", "I")))  # Remove duplicates, replace J with I
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    matrix = "".join(dict.fromkeys(key + alphabet))  # Remove duplicates again
    return np.array(list(matrix)).reshape(5, 5)

def find_position(matrix, letter):
    row, col = np.where(matrix == letter)
    return row[0], col[0]

def prepare_playfair_message(message):
    message = message.upper().replace("J", "I").replace(" ", "")
    
    processed = []
    i = 0
    while i < len(message):
        a = message[i]
        if i + 1 < len(message) and message[i] == message[i + 1]:  
            processed.append(a + 'X')  # Insert 'X' if duplicate letters appear together
            i += 1
        else:
            if i + 1 < len(message):
                processed.append(a + message[i + 1])
            else:
                processed.append(a + 'X')  # If last character is single, append 'X'
            i += 2

    return "".join(processed)

def playfair_encrypt(message, key):
    matrix = generate_playfair_matrix(key)
    message = message.upper().replace("J", "I").replace(" ", "")

    if len(message) % 2 != 0:
        message += "X"  # ensure message length = even
    
    ciphertext = ""
    for i in range(0, len(message), 2):
        a, b = message[i], message[i + 1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)
        
        if row_a == row_b:  # Same row
            ciphertext += matrix[row_a, (col_a + 1) % 5] + matrix[row_b, (col_b + 1) % 5]
        elif col_a == col_b:  # Same column
            ciphertext += matrix[(row_a + 1) % 5, col_a] + matrix[(row_b + 1) % 5, col_b]
        else:  # Rectangle swap
            ciphertext += matrix[row_a, col_b] + matrix[row_b, col_a]
    return ciphertext

def playfair_encrypt(message, key):
    matrix = generate_playfair_matrix(key)
    message = prepare_playfair_message(message)

    ciphertext = ""
    for i in range(0, len(message), 2):
        a, b = message[i], message[i + 1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)
        
        if row_a == row_b:  # Same row
            ciphertext += matrix[row_a, (col_a + 1) % 5] + matrix[row_b, (col_b + 1) % 5]
        elif col_a == col_b:  # Same column
            ciphertext += matrix[(row_a + 1) % 5, col_a] + matrix[(row_b + 1) % 5, col_b]
        else:  # Rectangle swap
            ciphertext += matrix[row_a, col_b] + matrix[row_b, col_a]
    return ciphertext

def playfair_decrypt(ciphertext, key):
    matrix = generate_playfair_matrix(key)
    message = ""
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i + 1]
        row_a, col_a = find_position(matrix, a)
        row_b, col_b = find_position(matrix, b)
        
        if row_a == row_b:  # Same row
            message += matrix[row_a, (col_a - 1) % 5] + matrix[row_b, (col_b - 1) % 5]
        elif col_a == col_b:  # Same column
            message += matrix[(row_a - 1) % 5, col_a] + matrix[(row_b - 1) % 5, col_b]
        else:  # Rectangle swap
            message += matrix[row_a, col_b] + matrix[row_b, col_a]

    return message.replace("X", "")  # Remove 'X' used for padding in encryption

# Rail Fence Cipher
def rail_fence_encrypt(text, depth):
    rail = [[" " for _ in range(len(text))] for _ in range(depth)]
    
    direction_down = False
    row, col = 0, 0
    for char in text:
        if row == 0 or row == depth - 1:
            direction_down = not direction_down
        rail[row][col] = char
        col += 1
        row += 1 if direction_down else -1
    
    return "".join([char for row in rail for char in row if char != " "])

def rail_fence_decrypt(ciphertext, depth):
    rail = [[" " for _ in range(len(ciphertext))] for _ in range(depth)]
    
    direction_down = None
    row, col = 0, 0
    for _ in range(len(ciphertext)):
        if row == 0:
            direction_down = True
        if row == depth - 1:
            direction_down = False
        rail[row][col] = "*"
        col += 1
        row += 1 if direction_down else -1
    
    index = 0
    for i in range(depth):
        for j in range(len(ciphertext)):
            if rail[i][j] == "*" and index < len(ciphertext):
                rail[i][j] = ciphertext[index]
                index += 1
    
    result = []
    row, col = 0, 0
    for _ in range(len(ciphertext)):
        if row == 0:
            direction_down = True
        if row == depth - 1:
            direction_down = False
        result.append(rail[row][col])
        col += 1
        row += 1 if direction_down else -1
    
    return "".join(result)

# Product Cipher (Playfair & Rail Fence)
def product_cipher_encrypt(message, key, depth):
    step1 = playfair_encrypt(message, key)
    step2 = rail_fence_encrypt(step1, depth)
    return step2

def product_cipher_decrypt(ciphertext, key, depth):
    step1 = rail_fence_decrypt(ciphertext, depth)
    step2 = playfair_decrypt(step1, key)
    return step2

# Testing Encryption & Decryption of the combined cipher and time taken
message = "Amin I just wanna tell you that your team manchester united is currently seating at bottom table and you guys are nowhere near champions league"
key = "MONARCHY"
depth = 3

start_time = time.perf_counter() # time.time()
ciphertext = product_cipher_encrypt(message, key, depth)
decrypted_text = product_cipher_decrypt(ciphertext, key, depth)
end_time = time.perf_counter() # time.time()

time_taken = (end_time - start_time) * 1_000_000
print(f"Ciphertext: {ciphertext}")
print(f"Decrypted Text: {decrypted_text}")
print(f"Time Taken: {time_taken :.3f} µs")