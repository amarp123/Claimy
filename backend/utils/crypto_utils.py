from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.fernet import Fernet
from passlib.context import CryptContext
import os

# ----------------------------
# 1️⃣ PASSWORD HASHING (ARGON2)
# ----------------------------

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)           

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)



# ----------------------------
# 2️⃣ MASTER KEY (HARDCODED)
# ----------------------------

FERNET_MASTER_KEY_VALUE = "P-kCEEniSFm6p_KLSXZRTFQJKdFjkLBqwFJZ-0GJHq0="
FERNET_KEY = FERNET_MASTER_KEY_VALUE.encode()



# ----------------------------
# 3️⃣ FILE ENCRYPTION (AES-256)
# ----------------------------

def generate_file_key():
    """Generate AES file encryption key."""
    return AESGCM.generate_key(bit_length=256)


def encrypt_bytes_with_aes(data: bytes, key: bytes):
    aes = AESGCM(key)
    nonce = os.urandom(12)
    encrypted = aes.encrypt(nonce, data, None)
    return nonce + encrypted


def decrypt_bytes_with_aes(data: bytes, key: bytes):
    nonce = data[:12]
    encrypted = data[12:]
    aes = AESGCM(key)
    return aes.decrypt(nonce, encrypted, None)



# ----------------------------
# 4️⃣ ENCRYPT AES KEY WITH FERNET
# ----------------------------

def encrypt_key_with_fernet(key: bytes) -> str:
    return Fernet(FERNET_KEY).encrypt(key).decode()


def decrypt_key_with_fernet(token: str) -> bytes:
    return Fernet(FERNET_KEY).decrypt(token.encode())
