# 🏗️ Pre-Permit AI: Resurrecting "Ghost Data" for the Housing Crisis

[![Live App](https://img.shields.io/badge/Live%20App-Cloud%20Run-blue?style=for-the-badge&logo=google-cloud)](https://dadu-analyzer-app-617957523681.us-west1.run.app)
[![Hackathon](https://img.shields.io/badge/Gemini%203-API%20Hackathon-red?style=for-the-badge&logo=google-gemini)](https://gemini3.devpost.com/)
[![Confluent](https://img.shields.io/badge/Confluent-Kafka-black?style=for-the-badge&logo=confluent)](https://confluent.cloud/)
[![GitHub](https://img.shields.io/badge/Repository-Main-green?style=for-the-badge&logo=github)](https://github.com/Cloudenvy7/Gemini3Hackathon)

### *Autonomous Architectural Auditing Powered by Gemini 3 Flash & Confluent Cloud*

---

## 🧬 The Evolution: A Tale of Two Sprints

**Pre-Permit AI was conceptualized and initiated on December 25, 2025.** 

This specific timeline ensures 100% eligibility across two concurrent industry challenges:
1.  **Gemini 3 API Hackathon:** Initiated after the Dec 17 opening, leveraging the bleeding-edge reasoning of Gemini 3 Flash.
2.  **Google Cloud AI Partner Catalyst:** Finalized and submitted before the Dec 31 deadline, proving production readiness in the Google/Confluent ecosystem.

### **The "Double Down" Strategy**
*   **Sprint 1: The Foundation (Dec 25–30, 2025)**
    We architected a "Triple-Layer Hybrid Truth Engine" to standardize fragmented city records into a single source of truth.
*   **Sprint 2: The Agentic Shift (Jan 2026)**
    When we discovered "Ghost Data" (retired records) was breaking 15% of queries, we doubled down on Gemini 3. We moved beyond simple APIs to build an **autonomous forensic agent** capable of "thinking" through data conflicts and "resurrecting" records via live web search.

---

## 🚀 The Crisis: The "Digital Archipelago"
Cities aren't built on land; they are built on data. But that data is currently holding us back:
*   **Stale Labels:** 2022 zoning changes (SF 5000 → NR3) aren't updated in legacy technical databases.
*   **The Zillow Paradox:** A property is active on Zillow, but returns a `404` in City APIs because its Parcel ID (PIN) was retired during a lot adjustment.
*   **The Data Tax:** Architects waste thousands of hours manually reconciling these fragments.

---

## 🧠 Technical Innovation: The 3-Layer Hybrid Truth Engine
We do not just "read" data; we reconstruct "truth" using a three-layer taxonomy:

1.  **Layer 0 (Identity):** King County Tax Parcel Centroids provide the immutable geographic anchor—the dirt stays the same even if the ID changes.
2.  **Layer 1 (Authority):** Current Land Use Detail polygons. We use **Spatial Intersection** to determine the *actual* legal zoning, bypassing outdated text labels.
3.  **Layer 2 (Capability):** The 2016 Development Capacity Model. We "decompress" **79+ technical attributes** (Lot Area, FAR, setbacks) for high-fidelity auditing.

---

## �️ The Crown Jewel: "The Investigator"
This is the core of our Gemini 3 entry. When a standard API query fails, the system triggers **The Investigator** pattern:
*   **Agentic Search:** Gemini 3 utilizes Google Search Grounding to scan Zillow, Redfin, and the County Assessor simultaneously.
*   **Thinking Mode:** Using Gemini 3's high-level reasoning, the agent concludes: *"Zillow shows this address is active; the city record is retired. The new active PIN is XXXXXXXXXX."*
*   **Self-Healing:** The agent heals the query by injecting the resurrected PIN back into the pipeline automatically.

---

## �️ The Forensic Ledger (Confluent Cloud)
High-stakes architectural decisions cannot rely on "black box" AI. 
*   **Immutable Accountability:** Every reasoning step, search query, and audit decision is serialized and streamed to **Confluent Cloud**.
*   **Traceability:** Every audit in our Google Sheets reporting suite is stamped with a **Confluent Run ID**, allowing officials to replay the AI's "thought process" for any given permit.

---

## � Reporting: Single Source of Truth
The platform exports a **"Decompressed" Professional Site Sheet** directly to Google Sheets.
*   **Airtable Schema:** Auto-structures 79+ fields into 8 professional blocks (Identity, Dimensions, Zoning, Capacity, Stats, Valuation, Raw Tech, Audit).
*   **PIN-Tabbed Organization:** Every property is tracked by its unique 10-digit PIN for permanent record stability.

---

## 📦 Getting Started

### 1. Requirements
*   Python 3.9+
*   Google Cloud Project (Gemini 3 API enabled)
*   Confluent Cloud Cluster
*   Google Service Account (with Sheets/Drive API access)

### 2. Installation
```bash
git clone https://github.com/Cloudenvy7/Gemini3Hackathon.git
pip install -r requirements.txt
streamlit run src/ui.py
```

---

## 📄 Project Artifacts
*   [**Walkthrough**](https://github.com/Cloudenvy7/Gemini3Hackathon/blob/main/walkthrough.md): Ground Truth verification.
*   [**Technical Brief**](https://github.com/Cloudenvy7/Gemini3Hackathon/blob/main/PROJECT_BRIEF.md): Feasibility logic deep dive.
*   [**Project Bible**](https://github.com/Cloudenvy7/Gemini3Hackathon/blob/main/PROJECT_BIBLE.md): Canonical build history.

---
**Developed for the Gemini 3 API Hackathon 2026. Transforming fragmented data into actionable housing solutions.**
