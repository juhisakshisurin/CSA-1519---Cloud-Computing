import os
import json
import hashlib
import time
from datetime import datetime

class HDFSBlock:
    """Represents a single HDFS data block stored on a DataNode."""
    def __init__(self, block_id, data_chunk, block_size_bytes=128 * 1024 * 1024):
        self.block_id = block_id
        self.data_chunk = data_chunk  # String / text bytes content
        self.size_bytes = len(data_chunk.encode('utf-8'))
        self.max_block_size = block_size_bytes
        self.checksum = hashlib.md5(data_chunk.encode('utf-8')).hexdigest()

class HDFSNameNode:
    """NameNode Metadata Manager: Manages HDFS directory tree, file-to-block mapping, and DataNode locations."""
    def __init__(self):
        self.file_namespace = {}  # { hdfs_path: { blocks: [block_ids], file_size: int, replication: int, created_at: str } }
        self.block_metadata = {}  # { block_id: { size: int, checksum: str, replicas: [datanode_ids] } }

    def register_file(self, hdfs_path, block_ids, file_size, replication_factor=3):
        self.file_namespace[hdfs_path] = {
            "blocks": block_ids,
            "file_size": file_size,
            "replication_factor": replication_factor,
            "created_at": datetime.utcnow().isoformat() + "Z"
        }

    def get_file_metadata(self, hdfs_path):
        return self.file_namespace.get(hdfs_path)


class HDFSCluster:
    """
    Hadoop Distributed File System (HDFS) Cluster Engine.
    Simulates NameNode metadata management, DataNode storage block allocation (128 MB blocks),
    3x Replication Factor, HDFS CLI tooling (`put`, `get`, `ls`, `cat`, `report`), and DataNode Failover Self-Healing.
    """
    def __init__(self, base_hdfs_dir=None, datanodes=["DN-1", "DN-2", "DN-3", "DN-4"], block_size_mb=128, default_replication=3):
        if base_hdfs_dir is None:
            self.base_dir = os.path.join(os.path.dirname(__file__), "..", "data", "hdfs_cluster")
        else:
            self.base_dir = base_hdfs_dir
        
        self.block_size_bytes = block_size_mb * 1024 * 1024  # 128 MB default
        self.default_replication = default_replication
        self.datanodes = {dn: {"status": "HEALTHY", "capacity_bytes": 500 * 1024 * 1024 * 1024} for dn in datanodes}
        self.namenode = HDFSNameNode()
        self.block_counter = 1000

        # Initialize physical DataNode directories
        for dn in self.datanodes.keys():
            os.makedirs(os.path.join(self.base_dir, dn), exist_ok=True)

    def put_file(self, local_file_path, hdfs_target_path, replication_factor=None):
        """
        `hdfs dfs -put <local_file> <hdfs_path>`
        Splits local file into 128MB block chunks and distributes 3x replicas across DataNodes.
        """
        if replication_factor is None:
            replication_factor = self.default_replication

        if not os.path.exists(local_file_path):
            raise FileNotFoundError(f"Local file not found: {local_file_path}")

        with open(local_file_path, "r", encoding="utf-8") as f:
            content = f.read()

        file_size = len(content.encode('utf-8'))
        
        # Partition content into chunks (simulated block partitioning)
        # For small demo content, partition into logical chunk blocks of 1MB or 64KB for simulation visibility
        logical_chunk_size = min(self.block_size_bytes, max(64 * 1024, file_size // 3 if file_size > 200 * 1024 else file_size))
        if logical_chunk_size == 0:
            logical_chunk_size = 1

        content_chunks = [content[i:i + logical_chunk_size] for i in range(0, len(content), logical_chunk_size)]
        
        block_ids = []
        active_dns = [dn for dn, meta in self.datanodes.items() if meta["status"] == "HEALTHY"]
        
        if len(active_dns) < replication_factor:
            replication_factor = len(active_dns)

        for idx, chunk in enumerate(content_chunks):
            self.block_counter += 1
            bid = f"blk_{self.block_counter}"
            block_ids.append(bid)

            # Round-robin or block distribution across DataNodes
            assigned_dns = active_dns[idx % len(active_dns):] + active_dns[:idx % len(active_dns)]
            replica_dns = assigned_dns[:replication_factor]

            block_obj = HDFSBlock(bid, chunk, self.block_size_bytes)
            
            self.namenode.block_metadata[bid] = {
                "size": block_obj.size_bytes,
                "checksum": block_obj.checksum,
                "replicas": replica_dns
            }

            # Write physical block replicas to DataNodes
            for dn in replica_dns:
                dn_block_path = os.path.join(self.base_dir, dn, f"{bid}.meta")
                with open(dn_block_path, "w", encoding="utf-8") as bf:
                    json.dump({"block_id": bid, "checksum": block_obj.checksum, "data": chunk}, bf)

        self.namenode.register_file(hdfs_target_path, block_ids, file_size, replication_factor)
        return {
            "hdfs_path": hdfs_target_path,
            "file_size_bytes": file_size,
            "blocks_count": len(block_ids),
            "replication_factor": replication_factor,
            "block_ids": block_ids
        }

    def get_file(self, hdfs_path, local_destination_path):
        """
        `hdfs dfs -get <hdfs_path> <local_destination>`
        Reads block replicas from available healthy DataNodes, verifies MD5 checksum, and reconstitutes local file.
        """
        file_meta = self.namenode.get_file_metadata(hdfs_path)
        if not file_meta:
            raise FileNotFoundError(f"HDFS path not found: {hdfs_path}")

        reconstituted_content = []

        for bid in file_meta["blocks"]:
            blk_meta = self.namenode.block_metadata[bid]
            block_read_success = False

            for dn in blk_meta["replicas"]:
                if self.datanodes.get(dn, {}).get("status") == "HEALTHY":
                    dn_block_path = os.path.join(self.base_dir, dn, f"{bid}.meta")
                    if os.path.exists(dn_block_path):
                        with open(dn_block_path, "r", encoding="utf-8") as bf:
                            bdata = json.load(bf)
                            
                        # MD5 Checksum Verification
                        calc_checksum = hashlib.md5(bdata["data"].encode('utf-8')).hexdigest()
                        if calc_checksum == blk_meta["checksum"]:
                            reconstituted_content.append(bdata["data"])
                            block_read_success = True
                            break

            if not block_read_success:
                raise IOError(f"HDFS Block Corruption Error: Unable to read block {bid} from any healthy DataNode!")

        full_text = "".join(reconstituted_content)
        os.makedirs(os.path.dirname(local_destination_path), exist_ok=True)
        with open(local_destination_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        return {
            "local_destination": local_destination_path,
            "file_size_bytes": len(full_text.encode('utf-8')),
            "status": "SUCCESS_CHECKSUM_VERIFIED"
        }

    def ls(self):
        """`hdfs dfs -ls /`"""
        return self.namenode.file_namespace

    def cat(self, hdfs_path):
        """`hdfs dfs -cat <hdfs_path>`"""
        tmp_target = os.path.join(self.base_dir, "temp_cat.txt")
        self.get_file(hdfs_path, tmp_target)
        with open(tmp_target, "r", encoding="utf-8") as f:
            content = f.read()
        if os.path.exists(tmp_target):
            os.remove(tmp_target)
        return content

    def report(self):
        """`hdfs dfs -report` Cluster Health & Capacity Summary."""
        total_files = len(self.namenode.file_namespace)
        total_blocks = len(self.namenode.block_metadata)
        under_replicated = 0

        for bid, bmeta in self.namenode.block_metadata.items():
            healthy_replicas = sum(1 for dn in bmeta["replicas"] if self.datanodes[dn]["status"] == "HEALTHY")
            if healthy_replicas < self.default_replication:
                under_replicated += 1

        return {
            "namenode_status": "ACTIVE",
            "active_datanodes": [dn for dn, meta in self.datanodes.items() if meta["status"] == "HEALTHY"],
            "failed_datanodes": [dn for dn, meta in self.datanodes.items() if meta["status"] == "DEAD"],
            "total_files": total_files,
            "total_blocks": total_blocks,
            "block_size_mb": self.block_size_bytes // (1024 * 1024),
            "under_replicated_blocks": under_replicated,
            "cluster_health": "HEALTHY" if under_replicated == 0 else "DEGRADED_UNDER_REPLICATED"
        }

    def simulate_datanode_failure(self, datanode_id):
        """Simulates a DataNode crash failure and triggers HDFS self-healing re-replication."""
        if datanode_id not in self.datanodes:
            raise ValueError(f"Unknown DataNode: {datanode_id}")

        self.datanodes[datanode_id]["status"] = "DEAD"
        
        # Self-Healing Auto-Re-replication Protocol
        healthy_dns = [dn for dn, meta in self.datanodes.items() if meta["status"] == "HEALTHY"]
        re_replicated_count = 0

        for bid, bmeta in self.namenode.block_metadata.items():
            if datanode_id in bmeta["replicas"]:
                bmeta["replicas"].remove(datanode_id)
                # Find surviving DataNode to copy replica to
                candidate_dns = [dn for dn in healthy_dns if dn not in bmeta["replicas"]]
                if candidate_dns:
                    new_dn = candidate_dns[0]
                    # Source replica content from a healthy node
                    src_dn = bmeta["replicas"][0]
                    src_path = os.path.join(self.base_dir, src_dn, f"{bid}.meta")
                    if os.path.exists(src_path):
                        with open(src_path, "r", encoding="utf-8") as f:
                            bcontent = f.read()
                        new_path = os.path.join(self.base_dir, new_dn, f"{bid}.meta")
                        with open(new_path, "w", encoding="utf-8") as f:
                            f.write(bcontent)
                        bmeta["replicas"].append(new_dn)
                        re_replicated_count += 1

        return {
            "failed_datanode": datanode_id,
            "status": "DATANODE_DEAD",
            "self_healing_re_replications": re_replicated_count,
            "surviving_datanodes": healthy_dns
        }

if __name__ == "__main__":
    cluster = HDFSCluster()
    sample_file = os.path.join(cluster.base_dir, "test.txt")
    with open(sample_file, "w") as f:
        f.write("Hello Hadoop HDFS Distributed Block Storage Engine!\n" * 100)
    
    put_res = cluster.put_file(sample_file, "/user/hadoop/test.txt")
    print("HDFS Put Result:", put_res)
    print("HDFS Report:", cluster.report())
