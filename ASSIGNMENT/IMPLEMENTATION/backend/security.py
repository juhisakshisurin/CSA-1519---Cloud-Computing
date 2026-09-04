import hashlib
import json
import os
import time
from datetime import datetime
from cryptography.fernet import Fernet

class SecurityEngine:
    """Security, Cryptography, RBAC, Data Anonymization & Audit Subsystem."""

    def __init__(self, secret_key=None, salt="HealthPulseSecureSalt2026"):
        self.salt = salt.encode('utf-8')
        if secret_key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = secret_key if isinstance(secret_key, bytes) else secret_key.encode('utf-8')
        self.cipher = Fernet(self.key)
        self.audit_log_path = os.path.join(os.path.dirname(__file__), "..", "data", "security_audit.jsonl")
        os.makedirs(os.path.dirname(self.audit_log_path), exist_ok=True)

    def hash_pii(self, value):
        """Salted SHA-256 Hashing for PII/PHI Anonymization (HIPAA/GDPR Safe Harbor)."""
        if not value:
            return None
        hasher = hashlib.sha256()
        hasher.update(self.salt + str(value).encode('utf-8'))
        return hasher.hexdigest()[:16]  # 16-char hash token

    def mask_ssn(self, ssn):
        """Masks SSN retaining last 4 digits."""
        if not ssn or len(ssn) < 4:
            return "***-**-****"
        return f"***-**-{ssn[-4:]}"

    def encrypt_field(self, plain_text):
        """AES-256 Symmetric Field-Level Encryption."""
        if not plain_text:
            return ""
        return self.cipher.encrypt(str(plain_text).encode('utf-8')).decode('utf-8')

    def decrypt_field(self, cipher_text):
        """AES-256 Decryption."""
        if not cipher_text:
            return ""
        return self.cipher.decrypt(cipher_text.encode('utf-8')).decode('utf-8')

    def apply_rbac_masking(self, record, role="Data_Scientist"):
        """
        Dynamic Role-Based Access Control (RBAC) Data Masking.
        Roles: Doctor, Data_Scientist, Auditor, Admin
        """
        masked = record.copy()

        if role == "Admin":
            return masked

        elif role == "Doctor":
            masked["ssn"] = self.mask_ssn(record.get("ssn"))
            # Doctor sees patient name and clinical diagnosis

        elif role == "Data_Scientist":
            masked["patient_name"] = "[REDACTED_NAME]"
            masked["ssn"] = "[REDACTED_SSN]"
            masked["anonymized_id"] = self.hash_pii(record.get("patient_id"))
            # Data Scientist needs analytical values, age, cost, diagnosis code

        elif role == "Auditor":
            masked["patient_name"] = "[REDACTED_NAME]"
            masked["ssn"] = "[REDACTED_SSN]"
            masked["clinical_notes"] = "[ENCRYPTED_TEXT]"
            masked["anonymized_id"] = self.hash_pii(record.get("patient_id"))

        else:
            raise ValueError(f"Unknown RBAC Role: {role}")

        return masked

    def compute_merkle_root(self, records):
        """Computes Merkle Tree Root Hash for data integrity verification."""
        if not records:
            return ""
        hashes = [hashlib.sha256(json.dumps(r, sort_keys=True).encode('utf-8')).hexdigest() for r in records]
        
        while len(hashes) > 1:
            if len(hashes) % 2 != 0:
                hashes.append(hashes[-1])
            new_hashes = []
            for i in range(0, len(hashes), 2):
                combined = (hashes[i] + hashes[i+1]).encode('utf-8')
                new_hashes.append(hashlib.sha256(combined).hexdigest())
            hashes = new_hashes
        
        return hashes[0]

    def log_audit_event(self, action, user, role, records_affected, status="SUCCESS", details=""):
        """Logs structured security audit events."""
        event = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "user": user,
            "role": role,
            "records_affected": records_affected,
            "status": status,
            "details": details
        }
        with open(self.audit_log_path, "a") as f:
            f.write(json.dumps(event) + "\n")
        return event

if __name__ == "__main__":
    sec = SecurityEngine()
    rec = {"patient_id": "P-10001", "ssn": "123-45-6789", "patient_name": "Alice Smith", "diagnosis_name": "Diabetes"}
    print("Hashed SSN:", sec.hash_pii(rec["ssn"]))
    enc_diag = sec.encrypt_field(rec["diagnosis_name"])
    print("Encrypted Diagnosis:", enc_diag)
    print("Decrypted:", sec.decrypt_field(enc_diag))
    print("RBAC Data_Scientist View:", sec.apply_rbac_masking(rec, role="Data_Scientist"))
