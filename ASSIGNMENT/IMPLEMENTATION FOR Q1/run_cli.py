import os
import sys
import json
import argparse
from datetime import datetime

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from generator import HealthcareDataGenerator
from security import SecurityEngine
from distributed_engine import DistributedStorageEngine, StreamWindowProcessor
from analytics import HealthcareAnalytics
from benchmark import BigDataBenchmarkRunner

def run_pipeline(record_count=10000, num_workers=4):
    print("=" * 70)
    print(" HEALTHPULSE SECURE BIG DATA ANALYTICS SYSTEM")
    print("=" * 70)
    
    gen = HealthcareDataGenerator()
    sec = SecurityEngine()
    storage = DistributedStorageEngine()
    stream_proc = StreamWindowProcessor(window_size_seconds=10)
    
    # 1. Volume & Variety Data Generation
    print(f"\n[1/6] Generating {record_count:,} EHR Records (Structured & Unstructured)...")
    ehr_records = gen.generate_ehr_batch(record_count, inject_noise=True)
    fhir_logs = gen.generate_fhir_json_logs(count=min(200, record_count // 10))
    vitals_stream = gen.generate_vitals_stream(patient_count=10, ticks=30)
    print(f"      -> Ingested {len(ehr_records):,} Structured EHR Records")
    print(f"      -> Ingested {len(fhir_logs):,} Semi-Structured FHIR Observation Logs")
    print(f"      -> Ingested {len(vitals_stream):,} Real-time Sensor Vitals Events")
    
    # 2. Security Controls & Encryption
    print("\n[2/6] Applying Security Controls (AES-256 Encryption & SHA-256 PII Hashing)...")
    sec_records = []
    for r in ehr_records:
        r_masked = sec.apply_rbac_masking(r, role="Data_Scientist")
        r_masked["encrypted_diagnosis"] = sec.encrypt_field(r["diagnosis_name"])
        sec_records.append(r_masked)
        
    merkle_root = sec.compute_merkle_root(sec_records[:500])
    sec.log_audit_event(
        action="BATCH_INGESTION_AND_ENCRYPTION",
        user="system_admin",
        role="Admin",
        records_affected=len(sec_records),
        details=f"Merkle Root: {merkle_root[:16]}..."
    )
    print(f"      -> Cryptographic Merkle Root Hash: {merkle_root}")
    print(f"      -> AES-256 Diagnosis Encryption & PII Anonymization Complete")

    # 3. Distributed Storage Write (HDFS simulation)
    print("\n[3/6] Writing to Distributed Partitioned Storage (HDFS/S3 simulation)...")
    partitions = storage.write_partitioned_dataset(sec_records)
    print(f"      -> Partitioned data written across {len(partitions)} regional directory partitions.")

    # 4. MapReduce Parallel Execution
    print(f"\n[4/6] Executing Parallel MapReduce Engine ({num_workers} Worker Threads)...")
    mapreduce_res = storage.run_parallel_mapreduce(sec_records, num_workers=num_workers)
    print(f"      -> Processed {mapreduce_res['total_records_processed']:,} records in {mapreduce_res['execution_time_seconds']} seconds.")
    print(f"      -> Pipeline Throughput: {mapreduce_res['throughput_records_per_sec']:,} records/sec.")
    print(f"      -> Veracity Cleansing: Imputed/Filtered {mapreduce_res['total_corrupt_imputed']:,} corrupt entries.")

    # 5. Velocity Stream Processing
    print("\n[5/6] Running Real-Time Vitals Stream Processing (Sliding Windows)...")
    stream_windows = stream_proc.process_stream_windows(vitals_stream)
    critical_windows = [w for w in stream_windows if w["status"] == "CRITICAL"]
    print(f"      -> Processed {len(stream_windows)} sliding windows. Flagged {len(critical_windows)} CRITICAL patient vitals spikes.")

    # 6. Advanced Analytics & Machine Learning
    print("\n[6/6] Computing Advanced Analytics & Outbreak Detection...")
    geo_outbreaks = HealthcareAnalytics.analyze_geo_outbreaks(sec_records)
    nlp_insights = HealthcareAnalytics.extract_clinical_nlp_insights(sec_records)
    cost_outliers = HealthcareAnalytics.detect_cost_outliers(sec_records)

    # Sample risk predictions
    sample_risks = [HealthcareAnalytics.calculate_readmission_risk_score(r) for r in ehr_records[:5]]

    print("\n" + "=" * 70)
    print(" EXECUTION RESULTS SUMMARY")
    print("=" * 70)
    print(f" Total Treatment Cost Aggregated : ${mapreduce_res['total_cost_usd']:,.2f}")
    print(f" Top Symptoms Extracted (NLP)    : {list(nlp_insights['top_symptoms'].keys())[:3]}")
    print(f" Cost Anomaly Upper Threshold    : ${cost_outliers['upper_bound_threshold']:,.2f} ({cost_outliers['outliers_count']} outliers)")
    print(f" Regional Outbreak Leader (East) : {geo_outbreaks.get('East', {}).get('dominant_condition', 'N/A')}")
    print("=" * 70)

    # Export data export file for Dashboard frontend preview
    export_payload = {
        "summary": mapreduce_res,
        "merkle_root": merkle_root,
        "sample_records": [sec.apply_rbac_masking(r, role="Doctor") for r in ehr_records[:10]],
        "sample_risks": sample_risks,
        "geo_outbreaks": geo_outbreaks,
        "nlp_insights": nlp_insights,
        "cost_outliers": cost_outliers,
        "stream_windows": stream_windows[:10]
    }
    
    export_path = os.path.join(os.path.dirname(__file__), "data", "dashboard_payload.json")
    with open(export_path, "w") as f:
        json.dump(export_payload, f, indent=2)
    print(f"\n[OK] Dashboard Payload saved to: {export_path}")
    return export_payload

def run_benchmarks():
    print("\n[BENCHMARK] Running Big Data Scalability Suite...")
    runner = BigDataBenchmarkRunner()
    results = runner.run_benchmark_scale(scale_tiers=[1000, 5000, 25000, 100000])
    
    out_path = os.path.join(os.path.dirname(__file__), "data", "benchmark_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"[OK] Scalability Benchmark Results saved to: {out_path}")
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Secure Big Data Analytics CLI")
    parser.add_argument("--records", type=int, default=10000, help="Number of records to process")
    parser.add_argument("--workers", type=int, default=4, help="Number of parallel worker processes")
    parser.add_argument("--benchmark", action="store_true", help="Run multi-tier scalability benchmark")
    
    args = parser.parse_args()
    if args.benchmark:
        run_benchmarks()
    else:
        run_pipeline(record_count=args.records, num_workers=args.workers)
