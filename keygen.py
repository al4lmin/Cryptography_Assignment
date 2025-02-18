import math
import os

# Function to check if a number is prime
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

# Function to generate large prime numbers
def generate_large_primes():
    while True:
        p = int.from_bytes(os.urandom(6), byteorder='big') | 1  # 6-byte primes
        q = int.from_bytes(os.urandom(6), byteorder='big') | 1

        if is_prime(p) and is_prime(q) and p != q:
            return p, q

# Function to generate RSA keys
def generate_rsa_keys():
    while True:
        p, q = generate_large_primes()
        n = p * q
        phi = (p - 1) * (q - 1)

        e = 65537  # Common public exponent
        if math.gcd(e, phi) == 1 and n > (1 << 64):  # Ensure n is > 8-byte integer
            break

    d = pow(e, -1, phi)
    return e, d, n

# Save keys to files
def save_keys():
    e, d, n = generate_rsa_keys()

    with open("public_key.txt", "w") as pub_file:
        pub_file.write(f"{e},{n}")

    with open("private_key.txt", "w") as priv_file:
        priv_file.write(f"{d},{n}")

    print("RSA Keys Generated!")
    print("Saved 'public_key.txt' and 'private_key.txt'.")

if __name__ == "__main__":
    save_keys()
