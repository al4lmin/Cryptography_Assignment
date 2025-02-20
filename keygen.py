import sympy

# Generate a large prime number using sympy (efficient)
def generate_large_prime(bits=512):
    return sympy.randprime(2**(bits-1), 2**bits)

# Generate RSA keys
def key_generation():
    p = generate_large_prime(512)
    q = generate_large_prime(512)
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 65537  # Common choice for e
    d = pow(e, -1, phi)  # Compute d (modular inverse)

    # Save public key (e, n) in hex format
    with open("public_key.txt", "w") as pub:
        pub.write(f"{e:x}\n{n:x}")

    # Save private key (d, n) in hex format
    with open("private_key.txt", "w") as priv:
        priv.write(f"{d:x}\n{n:x}")

    print("Keys generated successfully and stored in hex format!")

if __name__ == "__main__":
    key_generation()
