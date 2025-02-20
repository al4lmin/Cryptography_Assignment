import os

def generate_16byte_hex_key():
    key = os.urandom(16).hex()  # Generate a 16-byte (128-bit) symmetric key
    with open("symmetric_key.txt", "w") as key_file:
        key_file.write(key)  # Save key to a text file
    return key

# Generate and save the key
random_hex_key = generate_16byte_hex_key()
print(f"Generated 16-byte symmetric key: {random_hex_key}")
print("Key saved to symmetric_key.txt")
