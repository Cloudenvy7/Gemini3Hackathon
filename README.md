# 🏠 Pre-Permit AI: Three-Layer Hybrid Truth
### *Autonomous Architectural Auditing & Professional Reporting Suite*

[![Live App](https://img.shields.io/badge/Live%20App-Cloud%20Run-blue?style=for-the-badge&logo=google-cloud)](https://gemini3-seattle-permits-617957523681.us-west1.run.app)
[![Hackathon](https://img.shields.io/badge/Gemini%203-API%20Hackathon-red?style=for-the-badge&logo=google-gemini)](https://gemini3.devpost.com/)

---

## 🚀 The Challenge: "Ghost Data" in Urban Planning
In Seattle, zoning terminology changed in 2022 (e.g., SF 5000 → NR3). However, municipal data remains fragmented:
- **Current Zoning Authority** layers have the right labels but lack parcel-specific technical data.
- **Historical Capacity Models** have deep technical data (65+ attributes) but still use "Ghost Data" (outdated zoning labels).
- **Killed Parcels**: Many Parcel IDs (PINs) are retired/retired, breaking direct API lookups.

**Pre-Permit AI** solves this using an autonomous **Hybrid Truth** engine powered by **Gemini 3 Flash**, evolving from a simple auditor into a professional reporting suite.

---

## 🧠 Technical Architecture: The Three-Layer Hybrid Truth
We standardize fragmented city records into a single, deterministic record using a three-layer taxonomy:

### 1. Layer 0: PARCEL-BASE-FS0 (Identity)
The anchor for parcel identity (PIN, Address, Geometry).
- **Source**: King County Tax Parcel Centroids.
- **Role**: Ensures we are querying the correct geographic entity.

### 2. Layer 1: ZONING-AUTH-FS0 (Zoning Authority)
The source for authoritative current zoning labels (NR1, NR2, NR3).
- **Source**: Current Land Use Zoning Detail.
- **Innovation**: Queried via **Spatial Intersection**. we fetch geometry from Layer 2 and intersect it with Layer 1 polygons to resolve "Ghost Data" labels.

### 3. Layer 2: CAPACITY-LEGACY-FSx (Attributes)
The engine room for feasibility math.
- **Source**: Zoned Development Capacity Model.
- **Role**: Provides **79+ technical attributes** (Lot Area, FAR, Building Area, setbacks, etc.).

---

## 📊 New: Google Sheets "Single Source of Truth"
The platform now exports a **"Decompressed" Professional Site Sheet** directly to Google Sheets, mapping our technical dataset into a human-readable Airtable-style schema.

### Key Features:
- **PIN-Tabbed Organization**: Every property gets its own permanent tab keyed by the 10-digit PIN.
- **Forensic Traceability**: Every row is stamped with a **Confluent Run ID**, linking reports to the immutable back-end ledger.
- **Airtable Mapping**: Auto-structures 79+ fields into 8 professional blocks (Identity, Dimensions, Zoning, Capacity, Stats, Valuation, Raw Tech, Audit).

---

## 🛠️ Resiliency: "The Investigator"
When a PIN lookup fails due to a "Killed Parcel," the system triggers **The Investigator** pattern:
- **Agentic Search**: Gemini 3 searches Zillow and Redfin to resolve the current 10-digit Parcel ID (PIN) and "resurrects" the data.
- **Thinking Mode**: Utilizes Gemini 3's high-level reasoning to resolve complex institutional overlays (MIO) and recent rezone events.

---

## 🚦 System Snapshot
- **Model**: `gemini-3-flash-preview`
- **Data Engine**: Confluent Cloud (Immutable Audit Stream)
- **Infrastructure**: Google Cloud Run (Dockerized)
- **Reporting**: Google Sheets API (V4) / Google Drive API (V3)
- **Merged Fields**: 79+ technical attributes per query

---

## 📦 Setup & Installation

### 1. Mirror the Environment
Create a `.env` file from the following template:
```bash
GEMINI_API_KEY=your_google_key
BOOTSTRAP_SERVERS=your_confluent_servers
SASL_USERNAME=your_confluent_key
SASL_PASSWORD=your_confluent_secret
```

### 2. Google Sheets API setup
- Place your `service_account.json` in the project root.
- Enable Google Sheets and Drive APIs in your Google Cloud Console.
- Share your master Google Sheet with the client email found in your JSON file.

### 3. Run Locally
```bash
# Clone the repository
git clone https://github.com/Cloudenvy7/Gemini3Hackathon.git
cd Gemini3Hackathon

# Install dependencies
pip install -r requirements.txt

# Launch UI
streamlit run src/ui.py
```

---

## 📄 Project Artifacts
- [**Walkthrough**](https://github.com/Cloudenvy7/Gemini3Hackathon/blob/main/walkthrough.md): Detailed proof of work and "Ground Truth" verification.
- [**Technical Brief**](https://github.com/Cloudenvy7/Gemini3Hackathon/blob/main/PROJECT_BRIEF.md): Deep dive into the architectural feasibility logic and reporting suite evolution.
- [**Project Bible**](https://github.com/Cloudenvy7/Gemini3Hackathon/blob/main/PROJECT_BIBLE.md): Canonical build history and change logs.

---

**Developed for the Gemini 3 API Hackathon 2026. Transforming fragmented data into actionable housing solutions.**
