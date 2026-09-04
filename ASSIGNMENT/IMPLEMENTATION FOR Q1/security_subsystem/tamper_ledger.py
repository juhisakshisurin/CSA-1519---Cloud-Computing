import hashlib
import json
import os
from datetime import datetime

class MerkleTamperLedger:
    """
    Cryptographic Merkle Tree Ledger for Big Data Storage Integrity.
    Computes binary Merkle tree root hashes across data blocks and validates integrity against unauthorized alterations.
    """

    def __init__(self, ledger_file=None):
        if ledger_file is None:
            self.ledger_file = os.path.join(os.path.dirname(__file__), "..", "data", "block_merkle_ledger.json")
        else:
            self.ledger_file = ledger_file
        os.makedirs(os.path.dirname(self.ledger_file), exist_ok=True)
        self.ledger_history = self._load_ledger()

    def _load_ledger(self):
        if os.path.exists(self.ledger_file):
            with open(self.ledger_file, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except Exception:
                    return []
        return []

    def compute_record_hash(self, record):
        """Computes SHA-256 hash of a single record JSON."""
        serialized = json.dumps(record, sort_keys=True).encode('utf-8')
        return hashlib.sha256(serialized).hexdigest()

    def build_merkle_tree(self, records):
        """Builds a binary Merkle Tree over a list of records and returns the Root Hash."""
        if not records:
            return ""

        leaf_hashes = [self.compute_record_hash(r) for r in records]
        current_level = leaf_hashes

        while len(current_level) > 1:
            if len(current_level) % 2 != 0:
                current_level.append(current_level[-1])
            
            next_level = []
            for i in range(0, len(current_level), 2):
                combined = (current_level[i] + current_level[i+1]).encode('utf-8')
                parent_hash = hashlib.sha256(combined).hexdigest()
                next_level.append(parent_hash)

            current_level = next_level

        merkle_root = current_level[0]
        return merkle_root, leaf_hashes

    def commit_block_to_ledger(self, block_id, records):
        """Commits a data block Merkle root hash into the append-only cryptographic ledger."""
        root_hash, leaf_hashes = self.build_merkle_tree(records)
        entry = {
            "block_id": block_id,
            "merkle_root": root_hash,
            "record_count": len(records),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "previous_ledger_hash": self.ledger_history[-1]["merkle_root"] if self.ledger_history else "0000000000000000"
        }
        self.ledger_history.append(entry)
        
        with open(self.ledger_file, "w", encoding="utf-8") as f:
            json.dump(self.ledger_history, f, indent=2)

        return entry

    def verify_block_integrity(self, block_id, current_records):
        """
        Verifies current records against committed Merkle ledger entry.
        Returns detailed tamper diagnostic report if corruption/tampering occurs.
        """
        committed_entry = next((item for item in self.ledger_history if item["block_id"] == block_id), None)
        if not committed_entry:
            return {
                "status": "UNREGISTERED_BLOCK",
                "is_valid": False,
                "message": f"Block ID {block_id} not found in cryptographic ledger!"
            }

        current_root, current_leafs = self.build_merkle_tree(current_records)
        expected_root = committed_entry["merkle_root"]

        if current_root == expected_root:
            return {
                "status": "INTEGRITY_VERIFIED_OK",
                "is_valid": True,
                "merkle_root": current_root,
                "records_verified": len(current_records)
            }
        else:
            return {
                "status": "TAMPERING_DETECTED",
                "is_valid": False,
                "expected_merkle_root": expected_root,
                "current_merkle_root": current_root,
                "records_affected": len(current_records),
                "alert": f"CRITICAL: Cryptographic Merkle Root Mismatch for Block {block_id}!"
            }

if __name__ == "__main__":
    ledger = MerkleTamperLedger()
    sample = [{"id": 1, "val": "A"}, {"id": 2, "val": "B"}]
    entry = ledger.commit_block_to_ledger("block_test_01", sample)
    print("Committed Entry:", entry)
    print("Verification OK:", ledger.verify_block_integrity("block_test_01", sample))
    
    # Tamper test
    tampered_sample = [{"id": 1, "val": "A"}, {"id": 2, "val": "MODIFIED_ILLEGAL_VAL"}]
    print("Verification Tampered:", ledger.verify_block_integrity("block_test_01", tampered_sample))
