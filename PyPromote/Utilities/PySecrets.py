from cryptography.fernet import Fernet


class PySecrets:
    """
    Module for encrypting/decrypting database entries
    """
    def __init__(self):
        self.key = b'1seB4qb6ENRQboaLMXqN_o3V6crVkTGboZWCaJKhiEw='
        self.fernet = Fernet(self.key)

    def make_secret(self, secret: str) -> bytes:
        return self.fernet.encrypt(secret.encode())

    def make_public(self, secret: bytes) -> str:
        _secret = self.fernet.decrypt(secret).decode()
        return self.fernet.decrypt(secret).decode()
