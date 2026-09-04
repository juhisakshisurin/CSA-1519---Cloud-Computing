#!/usr/bin/env python3
"""
Hadoop Streaming Reducer script.
Reads sorted `key\tvalue` pairs from sys.stdin, aggregates count per key, and outputs `key\ttotal_count` to sys.stdout.
"""
import sys

def main():
    current_key = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split('\t')
        if len(parts) != 2:
            continue

        key, count_str = parts
        try:
            count = int(count_str)
        except ValueError:
            continue

        if current_key == key:
            current_count += count
        else:
            if current_key is not None:
                sys.stdout.write(f"{current_key}\t{current_count}\n")
            current_key = key
            current_count = count

    if current_key is not None:
        sys.stdout.write(f"{current_key}\t{current_count}\n")

if __name__ == "__main__":
    main()
