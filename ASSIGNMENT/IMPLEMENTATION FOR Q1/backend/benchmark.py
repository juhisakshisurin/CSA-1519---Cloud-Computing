import time
import os
import json
try:
    import psutil
except ImportError:
    psutil = None
from generator import HealthcareDataGenerator
from security import SecurityEngine
from distributed_engine import DistributedStorageEngine
from analytics import HealthcareAnalytics

class BigDataBenchmarkRunner:
    """Benchmarks processing performance, memory, throughput, and compression across data scale tiers."""

    def __init__(self):
        self.generator = HealthcareDataGenerator()
        self.security = SecurityEngine()
        self.storage = DistributedStorageEngine()

    def get_process_memory_mb(self):
        """Returns current process RAM usage in Megabytes."""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 * 1024)

    def run_benchmark_scale(self, scale_tiers=[1000, 5000, 25000, 100000], num_workers=4):
        """Runs benchmarks across multiple scale tiers."""
        results = []
        
        for scale in scale_tiers:
            mem_start = self.get_process_memory_mb()
            
            # Step 1: Data Generation (Volume & Variety)
            t0 = time.time()
            data = self.generator.generate_ehr_batch(scale, inject_noise=True)
            gen_time = time.time() - t0
            
            # Step 2: Security & Cryptography Overhead
            t1 = time.time()
            anonymized_data = []
            for r in data:
                r_sec = self.security.apply_rbac_masking(r, role="Data_Scientist")
                r_sec["encrypted_diagnosis"] = self.security.encrypt_field(r["diagnosis_name"])
                anonymized_data.append(r_sec)
            sec_time = time.time() - t1
            
            # Step 3: Write to Distributed Partitioned Storage
            t2 = time.time()
            partition_paths = self.storage.write_partitioned_dataset(anonymized_data)
            storage_write_time = time.time() - t2
            
            # Step 4: Parallel MapReduce Processing
            t3 = time.time()
            mapreduce_metrics = self.storage.run_parallel_mapreduce(anonymized_data, num_workers=num_workers)
            processing_time = time.time() - t3
            
            # Step 5: Advanced Analytics & Anomaly Detection
            t4 = time.time()
            geo_outbreaks = HealthcareAnalytics.analyze_geo_outbreaks(anonymized_data)
            nlp_insights = HealthcareAnalytics.extract_clinical_nlp_insights(anonymized_data)
            cost_outliers = HealthcareAnalytics.detect_cost_outliers(anonymized_data)
            analytics_time = time.time() - t4
            
            total_time = gen_time + sec_time + storage_write_time + processing_time + analytics_time
            mem_end = self.get_process_memory_mb()
            
            # Estimate raw JSON size vs partition size
            raw_size_mb = (len(json.dumps(data)) / (1024 * 1024))
            
            tier_result = {
                "record_count": scale,
                "generation_time_sec": round(gen_time, 3),
                "security_crypto_time_sec": round(sec_time, 3),
                "storage_write_time_sec": round(storage_write_time, 3),
                "parallel_processing_time_sec": round(processing_time, 3),
                "analytics_time_sec": round(analytics_time, 3),
                "total_pipeline_time_sec": round(total_time, 3),
                "throughput_records_per_sec": round(scale / total_time if total_time > 0 else 0, 1),
                "memory_used_mb": round(max(mem_end - mem_start, 5.0), 2),
                "dataset_size_mb": round(raw_size_mb, 2),
                "num_workers": num_workers,
                "partitions_written": len(partition_paths)
            }
            
            results.append(tier_result)
            print(f"[BENCHMARK] Scale {scale:,} records -> Total Time: {total_time:.2f}s | Throughput: {tier_result['throughput_records_per_sec']:,} rec/sec")

        return results

if __name__ == "__main__":
    runner = BigDataBenchmarkRunner()
    res = runner.run_benchmark_scale([500, 2000, 10000])
    print(json.dumps(res, indent=2))
