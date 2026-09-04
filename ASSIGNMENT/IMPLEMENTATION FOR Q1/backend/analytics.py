import re
import math
from collections import Counter

class HealthcareAnalytics:
    """Advanced Business Intelligence, Machine Learning Scoring & Unstructured Text Analytics."""

    @staticmethod
    def calculate_readmission_risk_score(record):
        """
        Predictive Risk Scoring algorithm for 30-day hospital readmission.
        Inputs: Age, Systolic BP, Glucose, Cholesterol, Diagnosis severity.
        """
        score = 0.0
        
        # Age risk factor
        age = record.get("age", 45)
        if age > 75:
            score += 35
        elif age > 60:
            score += 20
        elif age > 45:
            score += 10

        # Systolic BP risk factor
        bp = record.get("blood_pressure_systolic", 120)
        if bp >= 160 or bp < 90:
            score += 25
        elif bp >= 140:
            score += 15

        # Glucose risk factor
        glucose = record.get("glucose_mg_dl", 100)
        if glucose > 200 or glucose < 70:
            score += 25
        elif glucose > 140:
            score += 10

        # Diagnosis severity index
        diag_code = record.get("diagnosis_code", "")
        if diag_code in ["I21.9", "I50.9"]:  # Acute Myocardial Infarction / Heart Failure
            score += 25
        elif diag_code in ["J44.9", "N18.9"]:  # COPD / Chronic Kidney Disease
            score += 15

        risk_category = "HIGH" if score >= 60 else ("MEDIUM" if score >= 35 else "LOW")
        return {
            "patient_id": record.get("patient_id"),
            "risk_score": min(score, 100.0),
            "risk_category": risk_category
        }

    @staticmethod
    def analyze_geo_outbreaks(records):
        """Aggregates diagnoses by region to detect potential disease outbreak hotspots."""
        geo_clusters = {}
        for r in records:
            region = r.get("region", "Unknown")
            diag = r.get("diagnosis_name", "Unknown")
            
            if region not in geo_clusters:
                geo_clusters[region] = Counter()
            geo_clusters[region][diag] += 1

        summary = {}
        for region, counts in geo_clusters.items():
            top_diag, count = counts.most_common(1)[0]
            summary[region] = {
                "total_cases": sum(counts.values()),
                "dominant_condition": top_diag,
                "dominant_condition_cases": count,
                "breakdown": dict(counts)
            }
        return summary

    @staticmethod
    def extract_clinical_nlp_insights(records):
        """NLP Miner for unstructured clinical notes text (Variety)."""
        symptom_keywords = ["chest pain", "shortness of breath", "high fever", "fatigue", "joint stiffness", "dizziness", "cough"]
        medication_keywords = ["Metformin", "Lisinopril", "Atorvastatin", "Albuterol", "Amoxicillin", "Furosemide"]
        
        extracted_symptoms = Counter()
        extracted_meds = Counter()
        emergency_mentions = 0

        for r in records:
            note = r.get("clinical_notes", "").lower()
            if "emergency" in note or "acute" in note:
                emergency_mentions += 1
            
            for s in symptom_keywords:
                if s in note:
                    extracted_symptoms[s] += 1
                    
            for m in medication_keywords:
                if m.lower() in note:
                    extracted_meds[m] += 1

        return {
            "total_notes_analyzed": len(records),
            "emergency_acute_cases": emergency_mentions,
            "top_symptoms": dict(extracted_symptoms.most_common(5)),
            "top_medications": dict(extracted_meds.most_common(5))
        }

    @staticmethod
    def detect_cost_outliers(records):
        """Detects anomalous treatment costs using Interquartile Range (IQR)."""
        costs = [float(r.get("treatment_cost_usd", 0.0)) for r in records if "treatment_cost_usd" in r]
        if not costs:
            return {"outliers_count": 0, "threshold_upper": 0.0}

        sorted_costs = sorted(costs)
        n = len(sorted_costs)
        q1 = sorted_costs[int(n * 0.25)]
        q3 = sorted_costs[int(n * 0.75)]
        iqr = q3 - q1
        upper_bound = q3 + 1.5 * iqr

        outliers = [c for c in costs if c > upper_bound]
        return {
            "total_records": n,
            "q1_cost": round(q1, 2),
            "q3_cost": round(q3, 2),
            "iqr": round(iqr, 2),
            "upper_bound_threshold": round(upper_bound, 2),
            "outliers_count": len(outliers),
            "max_outlier_cost": round(max(outliers), 2) if outliers else 0.0
        }

if __name__ == "__main__":
    from generator import HealthcareDataGenerator
    gen = HealthcareDataGenerator()
    data = gen.generate_ehr_batch(100)
    print("Geo Outbreak Analysis:", HealthcareAnalytics.analyze_geo_outbreaks(data))
    print("NLP Clinical Insights:", HealthcareAnalytics.extract_clinical_nlp_insights(data))
