import os
import sys
import json
import argparse

# Add hadoop_ecosystem directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "hadoop_ecosystem"))

from hdfs_manager import HDFSCluster
from hadoop_streaming import HadoopStreamingRunner
from hadoop_analyzer import HadoopEcosystemAnalyzer

def run_hadoop_pipeline(line_count=10000):
    print("=" * 75)
    print(" APACHE HADOOP ECOSYSTEM & HDFS DISTRIBUTED SOLUTION (QUESTION 2)")
    print("=" * 75)

    cluster = HDFSCluster()
    streaming_runner = HadoopStreamingRunner(cluster)
    analyzer = HadoopEcosystemAnalyzer()

    # Step 1: Create local sample dataset for ingestion
    print(f"\n[1/5] Preparing Raw Dataset ({line_count:,} records)...")
    sample_file_path = os.path.join(cluster.base_dir, "sample_healthcare_logs.txt")
    with open(sample_file_path, "w", encoding="utf-8") as f:
        for i in range(line_count):
            f.write(f"2026-09-03 21:00:00 INFO Patient_P-{10000+i} Diagnosis_Cardiovascular Status_Active Region_East\n")

    raw_file_size = os.path.getsize(sample_file_path)
    print(f"      -> Created local file: {sample_file_path} ({raw_file_size / (1024*1024):.2f} MB)")

    # Step 2: HDFS Data Ingestion (-put)
    print("\n[2/5] Moving Data into HDFS Cluster (`hdfs dfs -put`)....")
    put_res = cluster.put_file(sample_file_path, "/user/hadoop/input/healthcare_logs.txt", replication_factor=3)
    print(f"      -> HDFS Target Path : {put_res['hdfs_path']}")
    print(f"      -> HDFS Block Count : {put_res['blocks_count']} blocks (128 MB configured block size)")
    print(f"      -> Replication      : {put_res['replication_factor']}x Replicas across DataNodes")

    # Step 3: Run Hadoop Streaming MapReduce Job
    print("\n[3/5] Executing Hadoop Streaming MapReduce (`mapper.py` | sort | `reducer.py`)....")
    job_res = streaming_runner.run_streaming_job("/user/hadoop/input/healthcare_logs.txt", "/user/hadoop/output/wordcount")
    print(f"      -> Job Status     : {job_res['status']} ({job_res['job_id']})")
    print(f"      -> Execution Time : {job_res['execution_time_seconds']} seconds")
    print(f"      -> Map Records    : {job_res['map_output_records']:,} mapped tokens")
    print(f"      -> Reduce Records : {job_res['reduce_output_records']:,} aggregated key-value results")

    # Step 4: Export Data out of HDFS (-get)
    print("\n[4/5] Moving Data out of HDFS (`hdfs dfs -get`)....")
    get_target_path = os.path.join(cluster.base_dir, "exported_part-r-00000.txt")
    get_res = cluster.get_file("/user/hadoop/output/wordcount", get_target_path)
    print(f"      -> Exported Local File : {get_res['local_destination']}")
    print(f"      -> Checksum Integrity  : {get_res['status']}")

    # Step 5: Storage Efficiency & Failover Reliability Analysis
    print("\n[5/5] Running Storage Efficiency & DataNode Failover Analysis....")
    storage_eval = analyzer.analyze_storage_efficiency(raw_file_size)
    failover_eval = analyzer.test_datanode_reliability_failover("DN-2")

    print("\n" + "=" * 75)
    print(" HADOOP SYSTEM PERFORMANCE & RELIABILITY REPORT SUMMARY")
    print("=" * 75)
    print(f" HDFS Storage Overhead Ratio : {storage_eval['replication_overhead_multiplier']} ({storage_eval['total_hdfs_footprint_mb']} MB Total HDFS Footprint)")
    print(f" Block Padding Waste          : {storage_eval['padding_waste_mb']} MB")
    print(f" Net Storage Efficiency      : {storage_eval['net_storage_efficiency_percent']}%")
    print(f" Failed DataNode Simulated    : {failover_eval['target_failed_node']} (Status: DATANODE_DEAD)")
    print(f" Post-Failover Accessibility  : {'YES - READABLE' if failover_eval['data_accessible_post_failure'] else 'NO'}")
    print(f" Self-Healing Re-replications : {failover_eval['self_healing_replications']} blocks restored on surviving nodes")
    print("=" * 75)

    # Save payload for frontend UI dashboard visualization
    payload = {
        "report": cluster.report(),
        "storage_eval": storage_eval,
        "failover_eval": failover_eval,
        "streaming_job": job_res,
        "hdfs_ls": cluster.ls()
    }
    
    out_payload_path = os.path.join(os.path.dirname(__file__), "data", "hadoop_dashboard_payload.json")
    with open(out_payload_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"\n[OK] Hadoop Dashboard Payload saved to: {out_payload_path}")
    return payload

def run_hadoop_benchmarks():
    print("\n[HADOOP BENCHMARK] Evaluating Hadoop Streaming Scalability Suite...")
    analyzer = HadoopEcosystemAnalyzer()
    benchmark_res = analyzer.evaluate_hadoop_scalability([1000, 5000, 25000, 100000])
    
    out_path = os.path.join(os.path.dirname(__file__), "data", "hadoop_benchmark_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(benchmark_res, f, indent=2)
    print(f"[OK] Hadoop Scalability Benchmark Results saved to: {out_path}")
    return benchmark_res

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hadoop Ecosystem & HDFS Solution CLI")
    parser.add_argument("--records", type=int, default=10000, help="Number of input records")
    parser.add_argument("--benchmark", action="store_true", help="Run Hadoop scalability benchmarks")
    
    args = parser.parse_args()
    if args.benchmark:
        run_hadoop_benchmarks()
    else:
        run_hadoop_pipeline(line_count=args.records)
