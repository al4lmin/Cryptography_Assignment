import os

def generate_8byte_hex_key():
    return os.urandom(8).hex()

# Generate and print the key
random_hex_key = generate_8byte_hex_key()
print(f"Generated 8-byte symmetric key: {random_hex_key}")
