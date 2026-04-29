"""
Encryption Service for User Data Privacy
"""
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os
import json
from typing import Any, Optional


class EncryptionService:
    """Service for encrypting and decrypting sensitive user data."""

    def __init__(self, encryption_key: Optional[str] = None):
        """
        Initialize the encryption service.

        Args:
            encryption_key: Base64-encoded encryption key (optional)
        """
        if encryption_key:
            self.key = base64.urlsafe_b64decode(encryption_key.encode())
        else:
            self.key = Fernet.generate_key()

        self.cipher = Fernet(self.key)

    @staticmethod
    def generate_key() -> str:
        """
        Generate a new encryption key.

        Returns:
            Base64-encoded encryption key
        """
        key = Fernet.generate_key()
        return base64.urlsafe_b64encode(key).decode()

    @staticmethod
    def derive_key_from_password(password: str, salt: Optional[bytes] = None) -> tuple:
        """
        Derive an encryption key from a password.

        Args:
            password: User password
            salt: Salt for key derivation (generated if not provided)

        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = os.urandom(16)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key.decode(), salt

    def encrypt(self, data: str) -> str:
        """
        Encrypt a string.

        Args:
            data: String to encrypt

        Returns:
            Encrypted string (base64-encoded)
        """
        encrypted = self.cipher.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypt a string.

        Args:
            encrypted_data: Encrypted string (base64-encoded)

        Returns:
            Decrypted string
        """
        encrypted = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = self.cipher.decrypt(encrypted)
        return decrypted.decode()

    def encrypt_json(self, data: Any) -> str:
        """
        Encrypt JSON-serializable data.

        Args:
            data: JSON-serializable data

        Returns:
            Encrypted string (base64-encoded)
        """
        json_str = json.dumps(data)
        return self.encrypt(json_str)

    def decrypt_json(self, encrypted_data: str) -> Any:
        """
        Decrypt JSON-serializable data.

        Args:
            encrypted_data: Encrypted string (base64-encoded)

        Returns:
            Decrypted JSON data
        """
        json_str = self.decrypt(encrypted_data)
        return json.loads(json_str)

    def encrypt_dict(self, data: dict, fields: list) -> dict:
        """
        Encrypt specific fields in a dictionary.

        Args:
            data: Dictionary with data
            fields: List of field names to encrypt

        Returns:
            Dictionary with encrypted fields
        """
        encrypted_data = data.copy()
        for field in fields:
            if field in encrypted_data:
                value = encrypted_data[field]
                if isinstance(value, (dict, list)):
                    encrypted_data[field] = self.encrypt_json(value)
                else:
                    encrypted_data[field] = self.encrypt(str(value))

        return encrypted_data

    def decrypt_dict(self, data: dict, fields: list) -> dict:
        """
        Decrypt specific fields in a dictionary.

        Args:
            data: Dictionary with encrypted data
            fields: List of field names to decrypt

        Returns:
            Dictionary with decrypted fields
        """
        decrypted_data = data.copy()
        for field in fields:
            if field in decrypted_data:
                try:
                    value = decrypted_data[field]
                    decrypted_data[field] = self.decrypt_json(value)
                except Exception:
                    # If decryption fails, keep original value
                    pass

        return decrypted_data

    def hash_password(self, password: str) -> str:
        """
        Hash a password (for authentication).

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        # Use a proper password hashing library in production
        # This is a simplified version
        import hashlib
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return base64.urlsafe_b64encode(salt + key).decode()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hash.

        Args:
            password: Plain text password
            hashed_password: Hashed password

        Returns:
            True if password matches, False otherwise
        """
        try:
            decoded = base64.urlsafe_b64decode(hashed_password.encode())
            salt = decoded[:32]
            stored_key = decoded[32:]

            new_key = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt,
                100000
            )

            return new_key == stored_key
        except Exception:
            return False


# Example usage
if __name__ == "__main__":
    # Generate encryption key
    key = EncryptionService.generate_key()
    print(f"Generated key: {key}")

    # Initialize service
    service = EncryptionService(key)

    # Encrypt/decrypt string
    original = "Sensitive user data"
    encrypted = service.encrypt(original)
    decrypted = service.decrypt(encrypted)

    print(f"Original: {original}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")

    # Encrypt/decrypt JSON
    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "interests": ["AI", "ML", "NLP"]
    }
    encrypted_json = service.encrypt_json(data)
    decrypted_json = service.decrypt_json(encrypted_json)

    print(f"\nOriginal JSON: {data}")
    print(f"Decrypted JSON: {decrypted_json}")

    # Encrypt specific fields
    user_data = {
        "user_id": "123",
        "name": "John Doe",
        "email": "john@example.com",
        "preferences": {"theme": "dark", "language": "en"}
    }
    encrypted_dict = service.encrypt_dict(user_data, ["email", "preferences"])
    decrypted_dict = service.decrypt_dict(encrypted_dict, ["email", "preferences"])

    print(f"\nEncrypted dict: {encrypted_dict}")
    print(f"Decrypted dict: {decrypted_dict}")
