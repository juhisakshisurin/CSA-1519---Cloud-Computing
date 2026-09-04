import json
from crypto_vault import CryptoVault

class RBACMasker:
    """
    5-Role Fine-Grained Role-Based Access Control (RBAC) & Dynamic Column Masking Engine.
    Roles:
      - SuperAdmin (Clearance Level 5)
      - ChiefComplianceOfficer (Clearance Level 4)
      - LeadDoctor (Clearance Level 3)
      - DataScientist (Clearance Level 2)
      - ThirdPartyResearcher (Clearance Level 1)
    """

    ROLE_CLEARANCES = {
        "SuperAdmin": 5,
        "ChiefComplianceOfficer": 4,
        "LeadDoctor": 3,
        "DataScientist": 2,
        "ThirdPartyResearcher": 1
    }

    def __init__(self, crypto_vault=None):
        if crypto_vault is None:
            self.vault = CryptoVault()
        else:
            self.vault = crypto_vault

    def mask_ssn_last4(self, ssn):
        if not ssn or len(ssn) < 4:
            return "***-**-****"
        return f"***-**-{ssn[-4:]}"

    def apply_role_masking(self, record, role="DataScientist"):
        """Applies dynamic column-level security masking based on user role clearance."""
        if role not in self.ROLE_CLEARANCES:
            raise PermissionError(f"Access Denied: Invalid Security Role '{role}'")

        clearance = self.ROLE_CLEARANCES[role]
        masked = record.copy()

        # Level 5: SuperAdmin
        if clearance == 5:
            masked["_security_clearance"] = "Level 5 - FULL_UNRESTRICTED"
            return masked

        # Level 4: ChiefComplianceOfficer
        elif clearance == 4:
            masked["_security_clearance"] = "Level 4 - COMPLIANCE_AUDIT"
            masked["ssn"] = self.mask_ssn_last4(record.get("ssn"))
            return masked

        # Level 3: LeadDoctor
        elif clearance == 3:
            masked["_security_clearance"] = "Level 3 - CLINICAL_PHYSICIAN"
            masked["ssn"] = self.mask_ssn_last4(record.get("ssn"))
            # Doctor sees patient name and diagnosis
            return masked

        # Level 2: DataScientist
        elif clearance == 2:
            masked["_security_clearance"] = "Level 2 - ANALYTICS_ANONYMIZED"
            masked["patient_name"] = "[REDACTED_NAME]"
            masked["ssn"] = "[REDACTED_SSN]"
            masked["anonymized_token"] = self.vault.hash_pii_pseudonym(record.get("patient_id"))
            return masked

        # Level 1: ThirdPartyResearcher
        elif clearance == 1:
            masked["_security_clearance"] = "Level 1 - RESEARCH_AGGREGATED"
            masked["patient_name"] = "[REDACTED_NAME]"
            masked["ssn"] = "[REDACTED_SSN]"
            masked["patient_id"] = "[REDACTED_ID]"
            masked["clinical_notes"] = "[ENCRYPTED_RESTRICTED]"
            
            # Bucketed k-anonymity rounding for cost
            cost = float(record.get("treatment_cost_usd", 0.0))
            masked["treatment_cost_usd"] = round(cost / 10000.0) * 10000.0
            return masked

        return masked

    def batch_mask_dataset(self, dataset, role="DataScientist"):
        """Applies RBAC masking policy across a dataset batch."""
        return [self.apply_role_masking(r, role=role) for r in dataset]

if __name__ == "__main__":
    masker = RBACMasker()
    rec = {"patient_id": "P-1001", "ssn": "123-45-6789", "patient_name": "Alice Smith", "diagnosis_name": "Hypertension", "treatment_cost_usd": 24500.0}
    print("Researcher View:", masker.apply_role_masking(rec, "ThirdPartyResearcher"))
    print("Doctor View:", masker.apply_role_masking(rec, "LeadDoctor"))
