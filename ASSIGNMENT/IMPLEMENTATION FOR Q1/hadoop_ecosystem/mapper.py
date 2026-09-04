#!/usr/bin/env python3
"""
Hadoop Streaming Mapper script.
Reads text lines from sys.stdin, tokenizes words/fields, and outputs tab-separated `key\tvalue` pairs to sys.stdout.
"""
import sys
import re

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        # Tokenize into clean words
        words = re.findall(r'\w+', line.lower())
        for word in words:
            if len(word) > 1:
                # Output key\tvalue pair (e.g. word \t 1)
                sys.stdout.write(f"{word}\t1\n")

if __name__ == "__main__":
    main()
