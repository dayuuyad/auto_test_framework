import hashlib
import base64
from cryptography.fernet import Fernet

class EncryptUtil:
    @staticmethod
    def md5_encrypt(text: str) -> str:
        md5 = hashlib.md5()
        md5.update(text.encode('utf-8'))
        return md5.hexdigest()
    
    @staticmethod
    def sha256_encrypt(text: str) -> str:
        sha256 = hashlib.sha256()
        sha256.update(text.encode('utf-8'))
        return sha256.hexdigest()
    
    @staticmethod
    def base64_encode(text: str) -> str:
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def base64_decode(encoded_text: str) -> str:
        return base64.b64decode(encoded_text.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def generate_key() -> bytes:
        return Fernet.generate_key()
    
    @staticmethod
    def fernet_encrypt(text: str, key: bytes) -> str:
        fernet = Fernet(key)
        return fernet.encrypt(text.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def fernet_decrypt(encrypted_text: str, key: bytes) -> str:
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_text.encode('utf-8')).decode('utf-8')