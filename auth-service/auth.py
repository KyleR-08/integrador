import os
import base64
from dotenv import load_dotenv
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


load_dotenv()

AES_KEY = os.getenv("AES_KEY", "")

if not AES_KEY:
    raise ValueError(
        "La variable de entorno AES_KEY no está definida. "
        "Configúrala en el archivo .env"
    )

if len(AES_KEY) < 32:
    AES_KEY = AES_KEY.ljust(32, "=")
elif len(AES_KEY) > 32:
    AES_KEY = AES_KEY[:32]

KEY_BYTES = AES_KEY.encode("utf-8")


def encrypt_password(password):
    iv = get_random_bytes(16)
    cipher = AES.new(KEY_BYTES, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(password.encode("utf-8"), AES.block_size))
    iv_b64 = base64.b64encode(iv).decode("utf-8")
    ciphertext_b64 = base64.b64encode(ciphertext).decode("utf-8")
    return f"{iv_b64}:{ciphertext_b64}"


def decrypt_password(encrypted):
    iv_b64, ciphertext_b64 = encrypted.split(":")
    iv = base64.b64decode(iv_b64)
    ciphertext = base64.b64decode(ciphertext_b64)
    cipher = AES.new(KEY_BYTES, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode("utf-8")
