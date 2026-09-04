# CSA1519 Cloud Computing & Big Data Analytics - Assignment Solutions

This directory contains the complete source code, distributed system implementations, datasets, test suites, and academic reports for the **CSA1519 Assignment: Design and Implement a Secure Big Data Analytics System**.

---

## 📂 Subdirectory Structure

### 1. [`IMPLEMENTATION/`](./IMPLEMENTATION/)
**Design and Implement a Big Data Analytics System (HealthPulse)**
- **Domain**: Healthcare EHR & Telemetry Big Data Analytics
- **Key Modules**:
  - Interactive React 18 / Vite 5Vs Matrix & Analytics Dashboard
  - Live Real-Time Ingestion Streamer (36,143 rec/s)
  - HDFS Distributed File System Block Visualizer (Replication Factor 3, simulated node failure recovery)
  - MapReduce Regional Disease Hotspot Analytics & 30-Day Hospital Readmission ML Risk Predictor
  - Interactive 6-Case Test Suite (TC-01 to TC-06)
  - Full 13-Part Academic Submission Report Viewer

### 2. [`IMPLEMENTATION FOR Q2/`](./IMPLEMENTATION%20FOR%20Q2/)
**Design and Implement a Big Data Processing Solution using Apache Hadoop**
- HDFS distributed data storage configuration, Hadoop streaming, MapReduce mapper/reducer scripts, and storage efficiency analysis.

### 3. [`IMPLEMENTATION FOR Q3/`](./IMPLEMENTATION%20FOR%20Q3/)
**Develop a Big Data Security Mechanism for a Distributed Data Processing Environment**
- Cryptographic vault (AES-256-GCM envelope encryption, Merkle Tree tamper detection, 5-role fine-grained RBAC column masking, and real-time Intrusion Detection System).

---

## 🚀 How to Run the Implementation Web Application

```bash
# Navigate to frontend
cd "ASSIGNMENT/IMPLEMENTATION/frontend"

# Install dependencies and launch local web application
npm install
npm run dev
```

Open `http://localhost:5173/` in Google Chrome to access the system.
