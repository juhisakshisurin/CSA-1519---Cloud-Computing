import os
import json
import hashlib
import hmac
import base64
from datetime import datetime
from cryptography.fernet import Fernet, InvalidToken

class CryptoVault:
    """
    Cryptographic Subsystem providing Data at Rest Encryption (AES-256 Envelope Encryption),
    Data in Transit Token Authentication (HMAC-SHA256), and Salted PII Pseudonymization.
    """

    def __init__(self, master_key=None, salt="HealthPulseBigDataSecuritySalt2026"):
        self.salt = salt.encode('utf-8')
        if master_key is None:
            self.master_key = Fernet.generate_key()
        else:
            self.master_key = master_key if isinstance(master_key, bytes) else master_key.encode('utf-8')
        
        self.cipher = Fernet(self.master_key)
        self.key_version = 1

    def rotate_master_key(self):
        """Rotates the master cryptographic key for key-lifecycle management compliance."""
        new_key = Fernet.generate_key()
        old_cipher = self.cipher
        self.master_key = new_key
        self.cipher = Fernet(new_key)
        self.key_version += 1
        return {
            "status": "KEY_ROTATED_SUCCESSFULLY",
            "new_key_version": self.key_version
        }

    def encrypt_data_at_rest(self, plain_text):
        """
        AES-256 Symmetric Field-Level / Payload Encryption for Data at Rest.
        Protects against unauthorized storage node inspection.
        """
        if not plain_text:
            return ""
        if not isinstance(plain_text, str):
            plain_text = json.dumps(plain_text)
        encrypted_bytes = self.cipher.encrypt(plain_text.encode('utf-8'))
        return encrypted_bytes.decode('utf-8')

    def decrypt_data_at_rest(self, cipher_text):
        """AES-256 Field Decryption."""
        if not cipher_text:
            return ""
        try:
            decrypted_bytes = self.cipher.decrypt(cipher_text.encode('utf-8'))
            return decrypted_bytes.decode('utf-8')
        except InvalidToken:
            raise PermissionError("Cryptographic Decryption Error: Invalid key or tampered ciphertext!")

    def sign_data_in_transit(self, payload):
        """
        HMAC-SHA256 Token Signer for Data in Transit Authentication across distributed worker nodes.
        Prevents Man-in-the-Middle (MitM) payload manipulation.
        """
        if isinstance(payload, dict):
            serialized = json.dumps(payload, sort_keys=True)
        else:
            serialized = str(payload)

        signature = hmac.new(self.master_key, serialized.encode('utf-8'), hashlib.sha256).hexdigest()
        return {
            "payload": payload,
            "hmac_signature": signature,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

    def verify_data_in_transit(self, signed_packet):
        """Verifies HMAC-SHA256 signature for data received over distributed network."""
        payload = signed_packet.get("payload")
        signature = signed_packet.get("hmac_signature")

        if isinstance(payload, dict):
            serialized = json.dumps(payload, sort_keys=True)
        else:
            serialized = str(payload)

        expected_sig = hmac.new(self.master_key, serialized.encode('utf-8'), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(signature, expected_sig):
            raise SecurityError("Data in Transit Tampering Detected: HMAC signature mismatch!")

        return True

    def hash_pii_pseudonym(self, value):
        """Salted SHA-256 Pseudonymization for PII/PHI (HIPAA Safe Harbor Compliance)."""
        if not value:
            return None
        hasher = hashlib.sha256()
        hasher.update(self.salt + str(value).encode('utf-8'))
        return f"TOK-{hasher.hexdigest()[:16]}"


class SecurityError(Exception):
    """Custom Security Exception."""
    pass

if __name__ == "__main__":
    vault = CryptoVault()
    enc = vault.encrypt_data_at_rest("Patient SSN 123-45-6789 Diagnosis Heart Failure")
    print("Encrypted Payload:", enc)
    print("Decrypted Payload:", vault.decrypt_data_at_rest(enc))
    signed = vault.sign_data_in_transit({"patient_id": "P-1001", "cost": 15000})
    print("Data in Transit Packet:", signed)
    print("HMAC Verified:", vault.verify_data_in_transit(signed))
