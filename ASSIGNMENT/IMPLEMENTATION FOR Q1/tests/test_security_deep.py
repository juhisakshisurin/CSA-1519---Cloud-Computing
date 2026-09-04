import sys
import os
import pytest

# Add security_subsystem directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "security_subsystem"))

from crypto_vault import CryptoVault, SecurityError
from rbac_masker import RBACMasker
from tamper_ledger import MerkleTamperLedger
from threat_detector import SecurityIntrusionDetector

@pytest.fixture
def crypto_vault():
    return CryptoVault()

@pytest.fixture
def sample_patient_record():
    return {
        "patient_id": "P-99001",
        "patient_name": "Alexander Hamilton",
        "ssn": "987-65-4321",
        "age": 47,
        "region": "East",
        "diagnosis_name": "Acute Myocardial Infarction",
        "treatment_cost_usd": 34500.0,
        "clinical_notes": "Emergency admission due to acute chest pain."
    }

def test_crypto_vault_envelope_encryption(crypto_vault):
    plain_text = "Sensitive EHR Clinical Diagnosis Information"
    enc_text = crypto_vault.encrypt_data_at_rest(plain_text)
    assert enc_text != plain_text
    dec_text = crypto_vault.decrypt_data_at_rest(enc_text)
    assert dec_text == plain_text

def test_master_key_rotation(crypto_vault):
    orig_version = crypto_vault.key_version
    res = crypto_vault.rotate_master_key()
    assert res["status"] == "KEY_ROTATED_SUCCESSFULLY"
    assert crypto_vault.key_version == orig_version + 1

def test_data_in_transit_hmac_verification(crypto_vault, sample_patient_record):
    signed_packet = crypto_vault.sign_data_in_transit(sample_patient_record)
    assert "hmac_signature" in signed_packet
    assert crypto_vault.verify_data_in_transit(signed_packet) is True

    # Tamper with packet
    tampered_packet = signed_packet.copy()
    tampered_packet["payload"] = sample_patient_record.copy()
    tampered_packet["payload"]["treatment_cost_usd"] = 999999.0
    
    with pytest.raises(SecurityError):
        crypto_vault.verify_data_in_transit(tampered_packet)

def test_5_role_rbac_dynamic_masking(crypto_vault, sample_patient_record):
    masker = RBACMasker(crypto_vault)

    # 1. SuperAdmin (Level 5)
    admin_view = masker.apply_role_masking(sample_patient_record, "SuperAdmin")
    assert admin_view["patient_name"] == "Alexander Hamilton"
    assert admin_view["ssn"] == "987-65-4321"

    # 2. ChiefComplianceOfficer (Level 4)
    compliance_view = masker.apply_role_masking(sample_patient_record, "ChiefComplianceOfficer")
    assert compliance_view["ssn"] == "***-**-4321"

    # 3. LeadDoctor (Level 3)
    doc_view = masker.apply_role_masking(sample_patient_record, "LeadDoctor")
    assert doc_view["patient_name"] == "Alexander Hamilton"
    assert doc_view["ssn"] == "***-**-4321"

    # 4. DataScientist (Level 2)
    ds_view = masker.apply_role_masking(sample_patient_record, "DataScientist")
    assert ds_view["patient_name"] == "[REDACTED_NAME]"
    assert ds_view["ssn"] == "[REDACTED_SSN]"
    assert "anonymized_token" in ds_view

    # 5. ThirdPartyResearcher (Level 1)
    res_view = masker.apply_role_masking(sample_patient_record, "ThirdPartyResearcher")
    assert res_view["patient_name"] == "[REDACTED_NAME]"
    assert res_view["clinical_notes"] == "[ENCRYPTED_RESTRICTED]"

def test_merkle_tree_tamper_detection(sample_patient_record, tmp_path):
    ledger_path = str(tmp_path / "test_merkle_ledger.json")
    ledger = MerkleTamperLedger(ledger_file=ledger_path)

    batch = [sample_patient_record] * 20
    commit_res = ledger.commit_block_to_ledger("block_test_100", batch)
    assert len(commit_res["merkle_root"]) == 64

    # Verify clean batch
    verify_res = ledger.verify_block_integrity("block_test_100", batch)
    assert verify_res["is_valid"] is True

    # Mutate record to simulate tamper attack
    tampered_batch = [r.copy() for r in batch]
    tampered_batch[2]["patient_name"] = "Malicious Impostor"
    
    tamper_res = ledger.verify_block_integrity("block_test_100", tampered_batch)
    assert tamper_res["is_valid"] is False
    assert tamper_res["status"] == "TAMPERING_DETECTED"

def test_ids_intrusion_exfiltration_blocking(tmp_path):
    audit_path = str(tmp_path / "threat_audit.jsonl")
    ids = SecurityIntrusionDetector(audit_file=audit_path, pii_exfiltration_threshold=100)

    # Query within threshold
    res1 = ids.inspect_request("user_bob", "DataScientist", "QUERY", records_requested=50)
    assert res1["status"] == "PERMITTED"

    # Exfiltration attack triggering threshold
    with pytest.raises(PermissionError) as exc_info:
        ids.inspect_request("user_bob", "DataScientist", "BULK_EXPORT", records_requested=150)
    
    assert "CRITICAL SECURITY INTRUSION ALERT" in str(exc_info.value)

if __name__ == "__main__":
    pytest.main(["-v", __file__])
