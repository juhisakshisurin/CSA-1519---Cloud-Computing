# HEALTHPULSE: DESIGN & IMPLEMENTATION OF A SECURE BIG DATA ANALYTICS SYSTEM

**Course / Assignment Submission**: Big Data Analytics Systems  
**Domain Selected**: Healthcare & Medical Telemetry Analytics  
**Platform Name**: HealthPulse Secure Big Data Platform  
**Location / Repository**: `C:\Users\ashis\.gemini\antigravity-ide\scratch\secure-bigdata-analytics-system`  

---

## 1. Executive Summary & Problem Statement

Modern healthcare organizations generate massive volumes of structured, semi-structured, and unstructured data daily from Electronic Health Record (EHR) systems, real-time patient vital sensors, diagnostic laboratories, and medical imaging. Traditional monolithic database architectures fail to process these datasets with acceptable throughput, lack scalable distributed storage, and fail to ensure strict privacy regulations (HIPAA/GDPR).

To solve these challenges, this project designs and implements **HealthPulse**, an end-to-end, high-throughput, secure Big Data analytics system. HealthPulse incorporates:
1. **Parallel MapReduce Processing**: A chunked in-memory distributed processing pipeline built with Python worker pools and DuckDB/Pandas acceleration.
2. **Distributed File System Concepts**: Partitioned data layout matching HDFS/S3 storage paradigms (`year=YYYY/month=MM/region=REGION`).
3. **Comprehensive Security Architecture**: AES-256 field encryption, SHA-256 salted PII pseudonymization, Role-Based Access Control (RBAC) dynamic data masking, Merkle Tree tamper detection, and structured audit logs.
4. **Advanced Machine Learning & Analytics**: Predictive 30-day hospital readmission risk scoring, real-time sliding-window vital anomaly detection, clinical doctor notes NLP text mining, and regional disease outbreak hotspot clustering.

---

## 2. System Architecture & Component Design

![System Architecture](healthpulse_bigdata_architecture_1788449712052.jpg)

```
+-----------------------------------------------------------------------------------+
|                            HEALTHPULSE DASHBOARD UI                               |
| (Real-time Monitoring | 5Vs Benchmarks | RBAC Masking View | Security Audit Logs) |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                        SECURITY & CRYPTOGRAPHY SUBSYSTEM                          |
|  - AES-256 Field Encryption      - SHA-256 Salted PII Anonymization             |
|  - Role-Based Access Control     - Merkle Tree Data Integrity Hashing             |
|  - Structured Security Audit Log                                                  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                    DISTRIBUTED PROCESSING & ANALYTICS ENGINE                      |
|  - Multi-Core Parallel MapReduce / Chunked Partition Execution Pipeline          |
|  - Sliding-Window Streaming Engine (Velocity - Vitals Anomaly Detection)          |
|  - NLP Clinical Text Miner (Variety - Unstructured Medical Notes Processing)      |
|  - Data Cleansing & Schema Validator (Veracity - Noise & Outlier Filter)          |
|  - ML Risk Predictor & BI Aggregator (Value - Readmission & Outbreak Analytics)   |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                      DISTRIBUTED FILE SYSTEM STORAGE (HDFS/S3 SIM)                 |
|  - Partitioned Storage Structure (`year=YYYY/month=MM/region=REGION/data.json`)  |
+-----------------------------------------------------------------------------------+
```

---

## 3. Demonstration of Big Data 5Vs

| Dimension | Characteristic in HealthPulse System | Implementation Detail |
| :--- | :--- | :--- |
| **VOLUME** | Handling massive scale datasets | Batch pipeline processes **100,000+ EHR records** (53.96 MB raw) with partitioned chunk storage on disk. |
| **VELOCITY** | High-frequency telemetry streams | **StreamWindowProcessor** computes sliding-window averages over patient ICU vitals (heart rate, SpO2) every 2-10 seconds to flag critical cardiac/respiratory spikes. |
| **VARIETY** | Multi-format heterogeneous data | Ingests **Structured CSV** (vitals, costs), **Semi-Structured FHIR JSON** (LOINC lab observations), and **Unstructured Clinical Notes** (doctor observations). |
| **VERACITY** | Cleaning noisy, corrupted data | Cleansing validator automatically filters out-of-range BP values, imputes missing patient ages, and eliminates duplicates (**489 corrupt entries cleaned**). |
| **VALUE** | Business intelligence & ML insights | Computes **30-day Readmission Risk Scores**, isolates **Cost Anomaly Outliers**, extracts **Top Symptoms via NLP**, and identifies **Regional Outbreak Hotspots**. |

---

## 4. Distributed File System & Execution Model

HealthPulse simulates Hadoop Distributed File System (HDFS) and Amazon S3 storage layout through regional directory partitioning:

```
data/hdfs_storage/
├── year=2026/
│   └── month=09/
│       ├── region=East/data_chunk.json
│       ├── region=North/data_chunk.json
│       ├── region=South/data_chunk.json
│       ├── region=West/data_chunk.json
│       └── region=Central/data_chunk.json
```

### MapReduce Execution Paradigm
1. **Partitioning & Ingestion**: Input records are partitioned across regional chunk files.
2. **Parallel Map Phase**: Multi-core worker processes (`ProcessPoolExecutor`) read chunk blocks concurrently, validate records, impute noise, and compute local cost/diagnosis aggregates.
3. **Reduce Phase**: Main driver aggregates local chunk dictionaries into global totals, calculating global treatment costs ($231,983,096.39) and regional disease distributions.

---

## 5. Security & Cryptography Architecture

HealthPulse implements a multi-layered security model compliant with HIPAA Safe Harbor and GDPR standards:

1. **AES-256 Symmetric Encryption**: Sensitive clinical diagnosis names are encrypted at rest using AES-256 (`Fernet` cipher).
2. **SHA-256 Salted PII Hashing**: Personally Identifiable Information (PII) such as SSN and Patient Names are hashed with a cryptographic salt (`HealthPulseSecureSalt2026`) producing irreversible tokens.
3. **Role-Based Access Control (RBAC) & Dynamic Data Masking**:
   - `Doctor`: Views patient name and diagnosis; SSN is masked (`***-**-1234`).
   - `Data Scientist`: PII is redacted (`[REDACTED_NAME]`, `[REDACTED_SSN]`); analytical metrics (age, cost, diagnosis code) remain unmasked.
   - `Auditor`: Views hashed patient IDs and audit metadata; clinical notes are encrypted (`[ENCRYPTED_TEXT]`).
   - `Admin`: Full system access.
4. **Merkle Tree Data Integrity**: Computes a binary Merkle tree root hash across data blocks. Any unauthorized alteration of a record changes the Merkle root, immediately detecting data tampering.
5. **Immutable Audit Logging**: Logs all read/write operations to `security_audit.jsonl`.

---

## 6. Verification & Automated Test Cases

The system includes a PyTest test suite (`tests/test_system.py`) covering all subsystems:

```bash
============================= test session starts =============================
platform win32 -- Python 3.13.15, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\ashis\.gemini\antigravity-ide\scratch\secure-bigdata-analytics-system
collected 6 items

tests\test_system.py::test_security_encryption_and_hashing PASSED       [ 16%]
tests\test_system.py::test_rbac_data_masking PASSED                      [ 33%]
tests\test_system.py::test_merkle_tamper_detection PASSED                [ 50%]
tests\test_system.py::test_distributed_mapreduce PASSED                  [ 66%]
tests\test_system.py::test_stream_vitals_processor PASSED                [ 83%]
tests\test_system.py::test_readmission_risk_scoring PASSED               [100%]

============================== 6 passed in 1.61s ==============================
```

---

## 7. Empirical Performance & Scalability Evaluation

The system was evaluated across multiple dataset scale tiers using 4 worker parallel processes:

| Scale Tier (Records) | Raw Size (MB) | Total Latency (sec) | MapReduce Time (sec) | Throughput (Records/sec) | RAM Memory Used (MB) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1,000** | 0.54 MB | 0.968 s | 0.839 s | 1,032.9 rec/s | 5.00 MB |
| **5,000** | 2.70 MB | 1.416 s | 0.836 s | 3,530.9 rec/s | 5.99 MB |
| **25,000** | 13.49 MB | 3.953 s | 1.130 s | **6,324.6 rec/s** | 33.69 MB |
| **100,000** | 53.96 MB | 16.817 s | 1.810 s | **5,946.5 rec/s** | 123.88 MB |

### Key Scalability Insights:
- **Linear Scaling**: Total execution time scales linearly with dataset size.
- **High Throughput**: Peak processing throughput reaches **~6,324 records/sec**.
- **Low Memory Overhead**: Memory usage remains lightweight (~123.88 MB for 100k records), demonstrating efficient chunked buffer management.

---

## 8. Conclusion

The **HealthPulse Secure Big Data Analytics System** successfully demonstrates the core principles of Big Data engineering:
1. Efficient multi-format data handling (Structured, FHIR JSON, Unstructured Notes).
2. Distributed storage partitioning and multi-core MapReduce processing.
3. Strict enterprise security with AES-256 encryption, SHA-256 PII hashing, RBAC data masking, and Merkle tree integrity verification.
4. Comprehensive empirical evaluation proving high throughput and linear scalability.
