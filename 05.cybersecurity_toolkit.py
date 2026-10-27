"""
05. Defensive Cybersecurity Audit & Hygiene Verification Toolkit
Provides defensive utilities for password entropy auditing, SHA-256 file integrity
verification, and log anomaly rate inspection.
"""

import hashlib
import math
import string
from collections import Counter

def calculate_password_entropy(password: str) -> dict:
    """Calculates Shannon and pool entropy bits for defensive password strength auditing."""
    pool_size = 0
    if any(c in string.ascii_lowercase for c in password):
        pool_size += 26
    if any(c in string.ascii_uppercase for c in password):
        pool_size += 26
    if any(c in string.digits for c in password):
        pool_size += 10
    if any(c in string.punctuation for c in password):
        pool_size += 32

    entropy_bits = len(password) * math.log2(max(pool_size, 1))
    rating = "Weak" if entropy_bits < 50 else ("Moderate" if entropy_bits < 75 else "Strong")
    return {"length": len(password), "entropy_bits": round(entropy_bits, 2), "rating": rating}

def compute_sha256_digest(content: bytes) -> str:
    """Computes SHA-256 hash for file integrity verification."""
    return hashlib.sha256(content).hexdigest()

def analyze_auth_logs(log_entries: list[dict], failure_threshold: int = 3) -> list[str]:
    """Identifies IP addresses with repeated authentication failures for defensive review."""
    failed_counts = Counter(
        entry["ip"] for entry in log_entries if entry.get("status") == "FAILED"
    )
    return [ip for ip, count in failed_counts.items() if count >= failure_threshold]

if __name__ == "__main__":
    print("=== Defensive Security Hygiene Audit ===")
    sample_pw = "Tr0ub4dor&3_Secure#2026"
    audit = calculate_password_entropy(sample_pw)
    print(f"Password Audit -> Length: {audit['length']}, Entropy: {audit['entropy_bits']} bits, Rating: {audit['rating']}")

    digest = compute_sha256_digest(b"configuration_v1.0_verified")
    print(f"Integrity SHA-256 Digest: {digest}")

    sample_logs = [
        {"ip": "192.0.2.10", "status": "SUCCESS"},
        {"ip": "198.51.100.42", "status": "FAILED"},
        {"ip": "198.51.100.42", "status": "FAILED"},
        {"ip": "198.51.100.42", "status": "FAILED"},
        {"ip": "203.0.113.5", "status": "SUCCESS"},
    ]
    flagged_ips = analyze_auth_logs(sample_logs, failure_threshold=3)
    print(f"Flagged IPs exceeding failed login threshold: {flagged_ips}")
