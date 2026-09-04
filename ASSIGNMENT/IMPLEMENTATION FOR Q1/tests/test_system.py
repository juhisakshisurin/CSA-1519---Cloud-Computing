import sys
import os
import pytest

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from generator import HealthcareDataGenerator
from security import SecurityEngine
from distributed_engine import DistributedStorageEngine, StreamWindowProcessor
from analytics import HealthcareAnalytics

@pytest.fixture
def sample_ehr_records():
    gen = HealthcareDataGenerator(seed=123)
    return gen.generate_ehr_batch(100, inject_noise=True)

def test_security_encryption_and_hashing():
    sec = SecurityEngine()
    original_text = "Malignant Neoplasm of Lung"
    
    # Encryption roundtrip
    cipher_text = sec.encrypt_field(original_text)
    assert cipher_text != original_text
    decrypted_text = sec.decrypt_field(cipher_text)
    assert decrypted_text == original_text

    # Salted PII Hashing
    ssn = "123-45-6789"
    hash1 = sec.hash_pii(ssn)
    hash2 = sec.hash_pii(ssn)
    assert hash1 == hash2
    assert ssn not in hash1
    assert len(hash1) == 16

def test_rbac_data_masking(sample_ehr_records):
    sec = SecurityEngine()
    record = sample_ehr_records[0]

    # Data Scientist view (PII masked)
    ds_view = sec.apply_rbac_masking(record, role="Data_Scientist")
    assert ds_view["patient_name"] == "[REDACTED_NAME]"
    assert ds_view["ssn"] == "[REDACTED_SSN]"
    assert "anonymized_id" in ds_view

    # Doctor view (SSN masked retaining last 4 digits)
    doc_view = sec.apply_rbac_masking(record, role="Doctor")
    assert doc_view["patient_name"] != "[REDACTED_NAME]"
    assert doc_view["ssn"].startswith("***-**-")

def test_merkle_tamper_detection(sample_ehr_records):
    sec = SecurityEngine()
    root1 = sec.compute_merkle_root(sample_ehr_records)
    assert len(root1) == 64  # SHA-256 hash length

    # Mutate one record
    tampered_records = [r.copy() for r in sample_ehr_records]
    tampered_records[0]["treatment_cost_usd"] = 999999.99
    
    root2 = sec.compute_merkle_root(tampered_records)
    assert root1 != root2  # Tamper detected!

def test_distributed_mapreduce(sample_ehr_records):
    storage = DistributedStorageEngine()
    results = storage.run_parallel_mapreduce(sample_ehr_records, num_workers=2, chunk_size=20)
    
    assert results["total_records_processed"] == 100
    assert results["total_valid"] == 100
    assert results["throughput_records_per_sec"] > 0
    assert "global_diag_counts" in results
    assert "global_region_costs" in results

def test_stream_vitals_processor():
    gen = HealthcareDataGenerator()
    events = gen.generate_vitals_stream(patient_count=5, ticks=20)
    
    proc = StreamWindowProcessor(window_size_seconds=10)
    windows = proc.process_stream_windows(events)
    
    assert len(windows) > 0
    assert "avg_heart_rate" in windows[0]
    assert "status" in windows[0]

def test_readmission_risk_scoring(sample_ehr_records):
    record = sample_ehr_records[0]
    risk = HealthcareAnalytics.calculate_readmission_risk_score(record)
    
    assert "risk_score" in risk
    assert risk["risk_category"] in ["LOW", "MEDIUM", "HIGH"]
    assert 0.0 <= risk["risk_score"] <= 100.0

if __name__ == "__main__":
    pytest.main(["-v", __file__])
