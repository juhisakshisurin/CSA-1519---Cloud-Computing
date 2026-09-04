import sys
import os
import pytest

# Add hadoop_ecosystem directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "hadoop_ecosystem"))

from hdfs_manager import HDFSCluster
from hadoop_streaming import HadoopStreamingRunner
from hadoop_analyzer import HadoopEcosystemAnalyzer

@pytest.fixture
def hdfs_cluster(tmp_path):
    cluster_dir = str(tmp_path / "hdfs_test_cluster")
    return HDFSCluster(base_hdfs_dir=cluster_dir)

def test_hdfs_put_and_get_integrity(hdfs_cluster, tmp_path):
    # Create sample file
    local_in = str(tmp_path / "sample.txt")
    with open(local_in, "w", encoding="utf-8") as f:
        f.write("Hadoop Distributed File System HDFS Verification Test\n" * 50)

    # Ingest into HDFS (`hdfs dfs -put`)
    put_res = hdfs_cluster.put_file(local_in, "/test/sample.txt", replication_factor=3)
    assert put_res["blocks_count"] > 0
    assert put_res["replication_factor"] == 3

    # Export out of HDFS (`hdfs dfs -get`)
    local_out = str(tmp_path / "restored.txt")
    get_res = hdfs_cluster.get_file("/test/sample.txt", local_out)
    assert get_res["status"] == "SUCCESS_CHECKSUM_VERIFIED"
    
    with open(local_out, "r", encoding="utf-8") as f:
        restored_text = f.read()
    
    with open(local_in, "r", encoding="utf-8") as f:
        orig_text = f.read()

    assert restored_text == orig_text

def test_hadoop_streaming_mapreduce_job(hdfs_cluster, tmp_path):
    # Prepare input file in HDFS
    local_in = str(tmp_path / "streaming_input.txt")
    with open(local_in, "w", encoding="utf-8") as f:
        f.write("hadoop streaming mapreduce hadoop hdfs streaming hadoop\n")

    hdfs_cluster.put_file(local_in, "/input/words.txt")

    runner = HadoopStreamingRunner(hdfs_cluster)
    job_res = runner.run_streaming_job("/input/words.txt", "/output/wordcount")

    assert job_res["status"] == "SUCCEEDED"
    assert job_res["map_output_records"] > 0
    assert job_res["reduce_output_records"] > 0

    cat_output = hdfs_cluster.cat("/output/wordcount")
    assert "hadoop\t3" in cat_output or "hadoop" in cat_output
    assert "streaming\t2" in cat_output or "streaming" in cat_output

def test_datanode_failover_and_self_healing(hdfs_cluster, tmp_path):
    local_in = str(tmp_path / "failover_data.txt")
    with open(local_in, "w", encoding="utf-8") as f:
        f.write("Critical DataNode Failover Test Content\n" * 100)

    hdfs_cluster.put_file(local_in, "/test/failover_data.txt", replication_factor=3)

    # Fail DN-2
    failover_res = hdfs_cluster.simulate_datanode_failure("DN-2")
    assert failover_res["status"] == "DATANODE_DEAD"
    assert failover_res["self_healing_re_replications"] > 0

    # Ensure file is still fully readable post-failover from surviving nodes
    cat_content = hdfs_cluster.cat("/test/failover_data.txt")
    assert len(cat_content) > 0
    assert "Critical DataNode Failover" in cat_content

def test_storage_efficiency_calc():
    analyzer = HadoopEcosystemAnalyzer()
    res = analyzer.analyze_storage_efficiency(raw_file_size_bytes=10 * 1024 * 1024, block_size_mb=128, replication_factor=3)
    assert res["raw_file_size_mb"] == 10.0
    assert res["blocks_allocated"] == 1
    assert res["replication_overhead_multiplier"] == "3x"

if __name__ == "__main__":
    pytest.main(["-v", __file__])
