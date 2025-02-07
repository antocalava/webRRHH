import hashlib
import os


def generate_salt() -> str:
    """Generate a random salt."""
    salt = os.urandom(16)
    return salt.hex()


def generate_hash(password: str, salt: str) -> str:
    """Hash the password with the given salt."""
    hash_obj = hashlib.sha256()
    hash_obj.update(password.encode('utf-8'))
    hash_obj.update(bytes.fromhex(salt))
    return hash_obj.hexdigest()


def encrypt_password(password: str) -> tuple[str, str]:
    """Encrypt the password with a hash and salt. Returns the hash and the salt"""
    salt = generate_salt()
    hashed = generate_hash(password, salt)
    return hashed, salt


def decrypt_password(password: str, salt: str) -> str:
    """Decrypt the password with the salt from the user entered password. Returns the hash."""
    return generate_hash(password, salt)


def verify_password(hashed: str, salt: str, input_password: str) -> bool:
    """Verify the input password against the hashed password."""
    input_password_hash = decrypt_password(input_password, salt)
    # Compare the hashed passwords
    return input_password_hash == hashed
