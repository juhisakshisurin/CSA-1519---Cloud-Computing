import os
import json
import time
from hdfs_manager import HDFSCluster
from hadoop_streaming import HadoopStreamingRunner

class HadoopEcosystemAnalyzer:
    """Evaluates Hadoop system performance: Storage Efficiency, Reliability Failover, and Scalability."""

    def __init__(self):
        self.cluster = HDFSCluster()
        self.streaming_runner = HadoopStreamingRunner(self.cluster)

    def analyze_storage_efficiency(self, raw_file_size_bytes, block_size_mb=128, replication_factor=3):
        """
        Calculates HDFS Storage Overhead, Block Padding Waste, and Net Storage Efficiency.
        Math:
          Total Raw Size = S
          Blocks Needed = ceil(S / BlockSize)
          Block Allocated Storage = Blocks Needed * BlockSize
          Padding Waste = Block Allocated Storage - S
          Total Distributed HDFS Footprint = Block Allocated Storage * ReplicationFactor
        """
        block_size_bytes = block_size_mb * 1024 * 1024
        blocks_needed = (raw_file_size_bytes + block_size_bytes - 1) // block_size_bytes if raw_file_size_bytes > 0 else 1
        allocated_bytes = blocks_needed * block_size_bytes
        padding_waste_bytes = allocated_bytes - raw_file_size_bytes
        total_hdfs_storage_bytes = allocated_bytes * replication_factor

        efficiency_ratio = (raw_file_size_bytes / total_hdfs_storage_bytes) if total_hdfs_storage_bytes > 0 else 0

        return {
            "raw_file_size_mb": round(raw_file_size_bytes / (1024 * 1024), 4),
            "block_size_mb": block_size_mb,
            "replication_factor": replication_factor,
            "blocks_allocated": blocks_needed,
            "allocated_storage_mb": round(allocated_bytes / (1024 * 1024), 2),
            "padding_waste_mb": round(padding_waste_bytes / (1024 * 1024), 4),
            "total_hdfs_footprint_mb": round(total_hdfs_storage_bytes / (1024 * 1024), 2),
            "net_storage_efficiency_percent": round(efficiency_ratio * 100, 2),
            "replication_overhead_multiplier": f"{replication_factor}x"
        }

    def test_datanode_reliability_failover(self, target_datanode="DN-2"):
        """
        Simulates DataNode failure and measures HDFS self-healing re-replication recovery.
        """
        # Populate HDFS with sample files
        sample_file = os.path.join(self.cluster.base_dir, "failover_test.txt")
        with open(sample_file, "w") as f:
            f.write("DataNode Reliability & Self-Healing Replication Test\n" * 500)
        
        self.cluster.put_file(sample_file, "/test/failover.txt", replication_factor=3)
        before_report = self.cluster.report()

        # Simulate DataNode failure
        t0 = time.time()
        failover_res = self.cluster.simulate_datanode_failure(target_datanode)
        recovery_time = time.time() - t0

        after_report = self.cluster.report()

        # Verify data accessibility post-failover
        cat_result = self.cluster.cat("/test/failover.txt")
        data_accessible = len(cat_result) > 0

        return {
            "target_failed_node": target_datanode,
            "data_accessible_post_failure": data_accessible,
            "recovery_time_sec": round(recovery_time, 4),
            "self_healing_replications": failover_res["self_healing_re_replications"],
            "before_cluster_health": before_report["cluster_health"],
            "after_cluster_health": after_report["cluster_health"],
            "surviving_datanodes": after_report["active_datanodes"]
        }

    def evaluate_hadoop_scalability(self, line_counts=[1000, 5000, 25000]):
        """Evaluates Hadoop Streaming performance across varying data scale tiers."""
        benchmark_metrics = []

        for count in line_counts:
            test_file = os.path.join(self.cluster.base_dir, f"scale_{count}.txt")
            with open(test_file, "w") as f:
                f.write(f"hadoop hdfs streaming mapreduce patient record log item_{count}\n" * count)

            # Measure Put Time into HDFS
            t0 = time.time()
            self.cluster.put_file(test_file, f"/input/scale_{count}.txt")
            hdfs_put_time = time.time() - t0

            # Measure Hadoop Streaming Execution Time
            t1 = time.time()
            job_res = self.streaming_runner.run_streaming_job(f"/input/scale_{count}.txt", f"/output/scale_{count}")
            streaming_time = time.time() - t1

            file_size_bytes = os.path.getsize(test_file)
            total_time = hdfs_put_time + streaming_time

            benchmark_metrics.append({
                "records_count": count,
                "file_size_mb": round(file_size_bytes / (1024 * 1024), 3),
                "hdfs_put_latency_sec": round(hdfs_put_time, 4),
                "hadoop_streaming_time_sec": round(streaming_time, 4),
                "total_pipeline_time_sec": round(total_time, 4),
                "throughput_records_per_sec": round(count / total_time if total_time > 0 else 0, 1),
                "map_records": job_res["map_output_records"],
                "reduce_records": job_res["reduce_output_records"]
            })

            if os.path.exists(test_file):
                os.remove(test_file)

        return benchmark_metrics

if __name__ == "__main__":
    analyzer = HadoopEcosystemAnalyzer()
    print("Storage Efficiency:", json.dumps(analyzer.analyze_storage_efficiency(50 * 1024 * 1024), indent=2))
    print("Reliability Failover Test:", json.dumps(analyzer.test_datanode_reliability_failover("DN-2"), indent=2))
