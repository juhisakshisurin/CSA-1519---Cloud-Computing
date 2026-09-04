import json
import random
import os
import time
from datetime import datetime, timedelta

FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]

DIAGNOSES = [
    ("E11.9", "Type 2 Diabetes Mellitus"),
    ("I10", "Essential Primary Hypertension"),
    ("J44.9", "Chronic Obstructive Pulmonary Disease"),
    ("I50.9", "Heart Failure Unspecified"),
    ("N18.9", "Chronic Kidney Disease"),
    ("J18.9", "Pneumonia Unspecified"),
    ("I21.9", "Acute Myocardial Infarction"),
    ("C34.90", "Malignant Neoplasm of Bronchus/Lung")
]

REGIONS = ["North", "South", "East", "West", "Central"]

CLINICAL_NOTE_TEMPLATES = [
    "Patient reported severe {symptom} over the last {duration} days. Prescribed {medication}. Follow-up in 2 weeks.",
    "Routine evaluation for {condition}. Vitals stable, but patient displays early signs of {symptom}. Adjusting dosage.",
    "Emergency admission due to acute {symptom} and elevated vitals. Administered IV {medication} immediately.",
    "Post-operative check for {condition}. Wound healing well, no infection signs observed. Continue baseline treatment."
]

SYMPTOMS = ["chest pain", "shortness of breath", "high fever", "fatigue", "joint stiffness", "dizziness", "cough"]
MEDICATIONS = ["Metformin 500mg", "Lisinopril 10mg", "Atorvastatin 20mg", "Albuterol inhaler", "Amoxicillin 500mg", "Furosemide 40mg"]

class HealthcareDataGenerator:
    """Generates synthetic multi-scale healthcare datasets demonstrating Big Data 5Vs."""
    
    def __init__(self, seed=42):
        random.seed(seed)
        
    def generate_ssn(self):
        return f"{random.randint(100,999):03d}-{random.randint(10,99):02d}-{random.randint(1000,9999):04d}"

    def generate_ehr_batch(self, count=1000, inject_noise=True):
        """Generates structured EHR records (Volume & Variety)."""
        records = []
        base_date = datetime(2026, 1, 1)
        
        for i in range(count):
            diag_code, diag_name = random.choice(DIAGNOSES)
            fname = random.choice(FIRST_NAMES)
            lname = random.choice(LAST_NAMES)
            
            # Introduce intentional veracity issues if enabled (for data cleaning testing)
            is_corrupt = inject_noise and (random.random() < 0.05)
            
            records.append({
                "patient_id": f"P-{100000 + i}",
                "ssn": self.generate_ssn(),
                "patient_name": f"{fname} {lname}",
                "age": None if is_corrupt else random.randint(18, 92),
                "gender": random.choice(["M", "F"]),
                "zip_code": f"{random.randint(10000, 99999)}",
                "region": random.choice(REGIONS),
                "admission_date": (base_date + timedelta(days=random.randint(0, 240))).strftime("%Y-%m-%d"),
                "diagnosis_code": diag_code,
                "diagnosis_name": diag_name,
                "blood_pressure_systolic": -999 if is_corrupt else random.randint(90, 180),
                "blood_pressure_diastolic": random.randint(60, 110),
                "cholesterol_mg_dl": random.randint(120, 310),
                "glucose_mg_dl": random.randint(70, 250),
                "treatment_cost_usd": round(random.uniform(1200.0, 45000.0), 2),
                "readmitted_30d": random.choice([0, 1]),
                "clinical_notes": random.choice(CLINICAL_NOTE_TEMPLATES).format(
                    symptom=random.choice(SYMPTOMS),
                    duration=random.randint(1, 10),
                    medication=random.choice(MEDICATIONS),
                    condition=diag_name
                )
            })
            
        return records

    def generate_fhir_json_logs(self, count=100):
        """Generates semi-structured FHIR-compliant JSON records (Variety)."""
        fhir_entries = []
        for i in range(count):
            fhir_entries.append({
                "resourceType": "Observation",
                "id": f"obs-{1000 + i}",
                "status": "final",
                "code": {
                    "coding": [{"system": "http://loinc.org", "code": "8867-4", "display": "Heart rate"}]
                },
                "subject": {"reference": f"Patient/P-{100000 + (i % 50)}"},
                "effectiveDateTime": datetime.utcnow().isoformat() + "Z",
                "valueQuantity": {
                    "value": random.randint(55, 140),
                    "unit": "beats/minute",
                    "system": "http://unitsofmeasure.org",
                    "code": "/min"
                },
                "interpretation": {
                    "coding": [{"system": "http://terminology.hlpt7.org", "code": "N" if random.random() > 0.15 else "H"}]
                }
            })
        return fhir_entries

    def generate_vitals_stream(self, patient_count=10, ticks=50):
        """Generates real-time sensor vitals telemetry stream (Velocity)."""
        stream_events = []
        now = time.time()
        
        for t in range(ticks):
            timestamp = now + t * 2.0  # Every 2 seconds
            for p in range(patient_count):
                pid = f"P-{100000 + p}"
                # Generate anomaly spike occasionally
                is_anomaly = random.random() < 0.08
                hr = random.randint(130, 175) if is_anomaly else random.randint(60, 95)
                spo2 = random.randint(75, 88) if is_anomaly else random.randint(95, 100)
                
                stream_events.append({
                    "timestamp": timestamp,
                    "timestamp_iso": datetime.fromtimestamp(timestamp).strftime("%H:%M:%S"),
                    "patient_id": pid,
                    "heart_rate_bpm": hr,
                    "spo2_percent": spo2,
                    "respiratory_rate": random.randint(12, 28),
                    "is_alert": is_anomaly
                })
        return stream_events

if __name__ == "__main__":
    gen = HealthcareDataGenerator()
    data = gen.generate_ehr_batch(10)
    print("Generated sample EHR:", json.dumps(data[0], indent=2))
