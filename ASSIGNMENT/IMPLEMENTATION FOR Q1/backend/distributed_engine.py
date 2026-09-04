import os
import json
import time
import math
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import pandas as pd

def map_chunk_process(chunk_data):
    """
    Map worker function: Processes a chunk of records in parallel.
    Performs data cleaning, validation, and local aggregation.
    """
    valid_records = []
    corrupt_count = 0
    local_diag_counts = {}
    local_region_cost = {}
    local_cost_sum = 0.0

    for r in chunk_data:
        # Data Cleaning / Veracity Filter
        if r.get("age") is None or r.get("blood_pressure_systolic", 0) <= 0:
            corrupt_count += 1
            # Impute age with median default (e.g., 45) if missing
            r["age"] = r.get("age") or 45
            r["blood_pressure_systolic"] = 120 if r.get("blood_pressure_systolic", 0) <= 0 else r["blood_pressure_systolic"]
        
        valid_records.append(r)

        # Local Map Aggregations
        diag = r.get("diagnosis_name", "Unknown")
        local_diag_counts[diag] = local_diag_counts.get(diag, 0) + 1

        reg = r.get("region", "Central")
        cost = float(r.get("treatment_cost_usd", 0.0))
        local_region_cost[reg] = local_region_cost.get(reg, 0.0) + cost
        local_cost_sum += cost

    return {
        "valid_records_count": len(valid_records),
        "corrupt_count": corrupt_count,
        "diag_counts": local_diag_counts,
        "region_costs": local_region_cost,
        "total_cost": local_cost_sum,
        "sample_valid": valid_records[:5]
    }


class DistributedStorageEngine:
    """Simulates Distributed Partitioned File Storage (HDFS/S3 layout) and Parallel MapReduce execution."""

    def __init__(self, base_storage_dir=None):
        if base_storage_dir is None:
            self.base_dir = os.path.join(os.path.dirname(__file__), "..", "data", "hdfs_storage")
        else:
            self.base_dir = base_storage_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def write_partitioned_dataset(self, dataset, year="2026", month="09"):
        """Stores records in partitioned folder structure: year=YYYY/month=MM/region=REGION/"""
        partition_paths = []
        region_groups = {}
        
        for r in dataset:
            reg = r.get("region", "Central")
            if reg not in region_groups:
                region_groups[reg] = []
            region_groups[reg].append(r)

        for reg, records in region_groups.items():
            p_dir = os.path.join(self.base_dir, f"year={year}", f"month={month}", f"region={reg}")
            os.makedirs(p_dir, exist_ok=True)
            file_path = os.path.join(p_dir, "data_chunk.json")
            with open(file_path, "w") as f:
                json.dump(records, f)
            partition_paths.append(file_path)

        return partition_paths

    def read_all_partitions(self):
        """Discovers and reads all partitioned dataset files from HDFS storage."""
        all_records = []
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith(".json"):
                    fp = os.path.join(root, file)
                    with open(fp, "r") as f:
                        records = json.load(f)
                        all_records.extend(records)
        return all_records

    def run_parallel_mapreduce(self, records, num_workers=4, chunk_size=5000):
        """
        Executes parallel MapReduce across data chunks using ProcessPoolExecutor.
        """
        start_time = time.time()
        chunks = [records[i:i + chunk_size] for i in range(0, len(records), chunk_size)]
        
        mapped_results = []
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(map_chunk_process, chunk) for chunk in chunks]
            for future in as_completed(futures):
                mapped_results.append(future.result())

        # Reduce Phase
        global_diag_counts = {}
        global_region_costs = {}
        total_valid = 0
        total_corrupt = 0
        total_cost = 0.0

        for res in mapped_results:
            total_valid += res["valid_records_count"]
            total_corrupt += res["corrupt_count"]
            total_cost += res["total_cost"]

            for diag, c in res["diag_counts"].items():
                global_diag_counts[diag] = global_diag_counts.get(diag, 0) + c

            for reg, cost in res["region_costs"].items():
                global_region_costs[reg] = global_region_costs.get(reg, 0.0) + cost

        elapsed_time = time.time() - start_time
        records_per_sec = len(records) / elapsed_time if elapsed_time > 0 else 0

        return {
            "total_records_processed": len(records),
            "total_valid": total_valid,
            "total_corrupt_imputed": total_corrupt,
            "total_cost_usd": round(total_cost, 2),
            "global_diag_counts": global_diag_counts,
            "global_region_costs": {k: round(v, 2) for k, v in global_region_costs.items()},
            "execution_time_seconds": round(elapsed_time, 4),
            "throughput_records_per_sec": round(records_per_sec, 2),
            "num_chunks": len(chunks),
            "num_workers": num_workers
        }


class StreamWindowProcessor:
    """Processes real-time streaming vitals events in sliding time windows (Velocity)."""

    def __init__(self, window_size_seconds=10):
        self.window_size = window_size_seconds

    def process_stream_windows(self, stream_events):
        """Aggregates streaming sensor events into windowed summaries and identifies anomaly spikes."""
        if not stream_events:
            return []

        # Sort events by timestamp
        sorted_events = sorted(stream_events, key=lambda x: x["timestamp"])
        min_ts = sorted_events[0]["timestamp"]
        max_ts = sorted_events[-1]["timestamp"]

        windows = []
        current_start = min_ts

        while current_start < max_ts:
            current_end = current_start + self.window_size
            window_events = [e for e in sorted_events if current_start <= e["timestamp"] < current_end]

            if window_events:
                avg_hr = sum(e["heart_rate_bpm"] for e in window_events) / len(window_events)
                avg_spo2 = sum(e["spo2_percent"] for e in window_events) / len(window_events)
                alert_count = sum(1 for e in window_events if e["is_alert"])

                windows.append({
                    "window_start": datetime.fromtimestamp(current_start).strftime("%H:%M:%S"),
                    "window_end": datetime.fromtimestamp(current_end).strftime("%H:%M:%S"),
                    "event_count": len(window_events),
                    "avg_heart_rate": round(avg_hr, 1),
                    "avg_spo2": round(avg_spo2, 1),
                    "critical_alerts": alert_count,
                    "status": "CRITICAL" if alert_count > 2 or avg_hr > 110 or avg_spo2 < 90 else "NORMAL"
                })

            current_start += self.window_size / 2.0  # 50% slide window

        return windows

if __name__ == "__main__":
    from generator import HealthcareDataGenerator
    gen = HealthcareDataGenerator()
    data = gen.generate_ehr_batch(1000)
    
    eng = DistributedStorageEngine()
    eng.write_partitioned_dataset(data)
    results = eng.run_parallel_mapreduce(data, num_workers=2)
    print("MapReduce Execution Summary:", json.dumps(results, indent=2))
