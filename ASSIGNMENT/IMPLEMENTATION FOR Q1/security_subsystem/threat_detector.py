import os
import json
import time
from datetime import datetime
from collections import defaultdict

class SecurityIntrusionDetector:
    """
    Real-Time Security Intrusion Detection System (IDS) & Threat Monitoring Engine.
    Detects unauthorized access attempts, high-velocity PII exfiltration spikes, and data tampering attacks.
    """

    def __init__(self, audit_file=None, pii_exfiltration_threshold=500, time_window_seconds=10):
        if audit_file is None:
            self.audit_file = os.path.join(os.path.dirname(__file__), "..", "data", "security_threat_audit.jsonl")
        else:
            self.audit_file = audit_file
        os.makedirs(os.path.dirname(self.audit_file), exist_ok=True)
        
        self.exfiltration_threshold = pii_exfiltration_threshold
        self.time_window = time_window_seconds
        self.user_access_history = defaultdict(list)
        self.active_blocked_users = set()

    def log_security_event(self, action, user_id, role, records_count=1, status="PERMITTED", details=""):
        """Logs structured immutable security event to JSONL audit log."""
        timestamp = datetime.utcnow().isoformat() + "Z"
        event = {
            "timestamp": timestamp,
            "action": action,
            "user_id": user_id,
            "role": role,
            "records_count": records_count,
            "status": status,
            "details": details
        }
        with open(self.audit_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event) + "\n")
        return event

    def inspect_request(self, user_id, role, action, records_requested=1):
        """
        Inspects incoming data request against security intrusion rules.
        Triggers defensive block if exfiltration spike or unauthorized access is detected.
        """
        now = time.time()

        # Check if user is already blocked due to threat detection
        if user_id in self.active_blocked_users:
            self.log_security_event(action, user_id, role, records_requested, "BLOCKED", "Session blocked by IDS threat response.")
            raise PermissionError(f"Security IDS Denial: User session '{user_id}' is BLOCKED due to suspicious activity!")

        # Rule 1: Role Clearance Check
        if role not in ["SuperAdmin", "ChiefComplianceOfficer", "LeadDoctor", "DataScientist", "ThirdPartyResearcher"]:
            self.log_security_event(action, user_id, role, records_requested, "THREAT_ALERT", "INVALID_ROLE_ATTEMPT")
            raise PermissionError(f"Security Alert: Invalid security clearance role '{role}'!")

        # Track query access history for velocity monitoring
        self.user_access_history[user_id].append((now, records_requested))
        
        # Purge access entries outside sliding time window
        recent_requests = [req for req in self.user_access_history[user_id] if now - req[0] <= self.time_window]
        self.user_access_history[user_id] = recent_requests

        total_records_window = sum(req[1] for req in recent_requests)

        # Rule 2: PII Exfiltration Spike Threshold Check
        if total_records_window > self.exfiltration_threshold:
            self.active_blocked_users.add(user_id)
            self.log_security_event(
                action="EXFILTRATION_SPIKE_DETECTED",
                user_id=user_id,
                role=role,
                records_count=total_records_window,
                status="THREAT_ALERT_BLOCKED",
                details=f"ALERT: User requested {total_records_window} records in {self.time_window}s, exceeding threshold {self.exfiltration_threshold}!"
            )
            raise PermissionError(f"CRITICAL SECURITY INTRUSION ALERT: High-velocity PII exfiltration spike detected! User '{user_id}' session BLOCKED.")

        # Log clean permitted event
        return self.log_security_event(action, user_id, role, records_requested, "PERMITTED", "Passed IDS rules.")

if __name__ == "__main__":
    ids = SecurityIntrusionDetector(pii_exfiltration_threshold=100)
    print("Normal Request:", ids.inspect_request("user_alice", "DataScientist", "QUERY_EHR", records_requested=10))
    try:
        # Exfiltration attack simulation
        ids.inspect_request("user_alice", "DataScientist", "BULK_EXPORT", records_requested=150)
    except PermissionError as e:
        print("IDS Block Triggered:", e)
