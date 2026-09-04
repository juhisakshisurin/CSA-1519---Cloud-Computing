import os
import sys
import subprocess
import time
import json

class HadoopStreamingRunner:
    """
    Hadoop Streaming MapReduce Execution Engine.
    Simulates `hadoop jar hadoop-streaming.jar -input <in> -output <out> -mapper <m> -reducer <r>`
    using stdin/stdout subprocess pipes.
    """

    def __init__(self, hdfs_cluster=None):
        from hdfs_manager import HDFSCluster
        if hdfs_cluster is None:
            self.hdfs = HDFSCluster()
        else:
            self.hdfs = hdfs_cluster

    def run_streaming_job(self, input_hdfs_path, output_hdfs_path, mapper_script=None, reducer_script=None):
        """
        Executes a Hadoop Streaming MapReduce job.
        Pipeline: Read HDFS Input -> Pipe to Mapper -> Sort Keys -> Pipe to Reducer -> Write to HDFS Output
        """
        curr_dir = os.path.dirname(__file__)
        if mapper_script is None:
            mapper_script = os.path.join(curr_dir, "mapper.py")
        if reducer_script is None:
            reducer_script = os.path.join(curr_dir, "reducer.py")

        start_time = time.time()

        # Step 1: Read input text from HDFS
        input_text = self.hdfs.cat(input_hdfs_path)

        # Step 2: Execute Mapper Subprocess (stdin -> stdout)
        mapper_proc = subprocess.Popen(
            [sys.executable, mapper_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        map_out, map_err = mapper_proc.communicate(input=input_text)
        if mapper_proc.returncode != 0:
            raise RuntimeError(f"Hadoop Streaming Mapper Failed: {map_err}")

        # Step 3: Hadoop Shuffle & Sort Phase (Sort lines by key)
        map_lines = [line for line in map_out.strip().split('\n') if line]
        sorted_map_lines = sorted(map_lines, key=lambda x: x.split('\t')[0] if '\t' in x else x)
        sorted_map_text = "\n".join(sorted_map_lines) + "\n"

        # Step 4: Execute Reducer Subprocess (stdin -> stdout)
        reducer_proc = subprocess.Popen(
            [sys.executable, reducer_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        red_out, red_err = reducer_proc.communicate(input=sorted_map_text)
        if reducer_proc.returncode != 0:
            raise RuntimeError(f"Hadoop Streaming Reducer Failed: {red_err}")

        elapsed_time = time.time() - start_time

        # Step 5: Save Hadoop Streaming Output into HDFS directory
        local_tmp_out = os.path.join(self.hdfs.base_dir, "temp_part_r_00000.txt")
        with open(local_tmp_out, "w", encoding="utf-8") as f:
            f.write(red_out)

        put_meta = self.hdfs.put_file(local_tmp_out, output_hdfs_path)
        if os.path.exists(local_tmp_out):
            os.remove(local_tmp_out)

        output_records = [line for line in red_out.strip().split('\n') if line]

        return {
            "job_id": f"job_streaming_{int(time.time())}",
            "status": "SUCCEEDED",
            "execution_time_seconds": round(elapsed_time, 4),
            "input_file": input_hdfs_path,
            "output_file": output_hdfs_path,
            "map_output_records": len(map_lines),
            "reduce_output_records": len(output_records),
            "top_aggregated_results": [r.split('\t') for r in output_records[:10] if '\t' in r]
        }

if __name__ == "__main__":
    from hdfs_manager import HDFSCluster
    cl = HDFSCluster()
    sample_text = os.path.join(cl.base_dir, "text_input.txt")
    with open(sample_text, "w") as f:
        f.write("hadoop hdfs mapreduce streaming hadoop streaming hadoop hdfs\n" * 50)
    cl.put_file(sample_text, "/input/sample.txt")
    
    runner = HadoopStreamingRunner(cl)
    res = runner.run_streaming_job("/input/sample.txt", "/output/part-00000")
    print("Hadoop Streaming Job Summary:", json.dumps(res, indent=2))
