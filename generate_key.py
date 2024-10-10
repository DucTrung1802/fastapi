import secrets

# Generate a 64-byte secret key
secret_key = secrets.token_hex(64)

print(secret_key)
