# 🎓 PROJECT BRIEF: The Evolution of Pre-Permit AI (v2.3.2)

## 🌟 The Vision: Unclogging the Seattle Permit Machine
Seattle's housing crisis is exacerbated by a $367M permit backlog. Our mission was to build an AI "Sidekick" that could do the heavy lifting: auditing architectural plans against complex municipal codes in seconds, not months.

## 🧠 The Narrative: Decompressing the Technical Journey

### 1. The "Hybrid Truth" Architecture (The Data Pivot)
We discovered that Seattle's municipal records are fragmented across three sources:
- **Layer 0 (Parcel Base)**: Reliable identity but legacy labels.
- **Layer 1 (Zoning Authority)**: Accurate NR* labels but lacks technical parcel data.
- **Layer 2 (Technical Capacity)**: Deep technical data (79+ attributes) but uses "Ghost Data" (SF 5000) terminology.

**The Fix:** We implemented a three-source merging engine. By performing **Spatial Intersection**—using the parcel's geometry from Layer 2 to query Layer 1 polygons—we've ensured that the professional gets current labels without losing 79 technical attributes.

### 2. The "Investigator" Resiliency Pattern
Valid addresses like *11520 Roosevelt Way NE* often return "No Data" because they were flagged as "Killed Parcels."
- **The New Way:** I taught Gemini 3 to act as an agent. If the city API fails, Gemini searches Zillow and Redfin to resolve the current 10-digit Parcel ID (PIN) and "resurrects" the data.

### 3. The "Reporting Suite" Evolution (Google Sheets Integration)
A technical JSON is useful for developers, but architects live in spreadsheets. 
- **The Upgrade:** We integrated the **Google Sheets API** to provide an automated "Airtable-style" report.
- **Decompressed Mapping:** We built a mapping engine that translates our 79+ raw fields into 8 professional blocks: Identity, Physical Dimensions, Zoning Authority, Capacity, Stats, Valuation, Raw Tech, and Audit Ledger.

### 4. The "Nervous System" (Confluent Cloud)
An AI brain is useless without a memory. We integrated **Confluent Cloud** to act as our "Run Ledger."
- **Why?** It creates an immutable, traceable record of every decision. Every Google Sheet row is now stamped with a **Confluent Run ID**, creating a forensic link back to the immutable event ledger.

### 5. The "Brain" Upgrade (Gemini 3 Flash)
We pivoted to **Gemini 3 Flash** for its **Thinking Mode**.
- **The Win:** Gemini 3 reasons through complex Major Institution Overlays (MIO) and Zoning codes with significantly higher accuracy.
- **Response Harvesting:** We implemented logic to strip out the "thinking" monologue and extract only the final, machine-readable truth for the reporting engine.

## 🛠️ The Technical "Under the Hood"

### The Agentic Architecture
- **Auditor (`src/auditor.py`):** The Brain. Uses `google-genai` SDK with built-in Google Search grounding.
- **Fetcher (`src/fetcher.py`):** The Nervous System. Connects Python logic to Seattle's ArcGIS REST servers, Confluent Kafka, and the Airtable Mapping Engine.
- **Sheets Manager (`src/sheets.py`):** The Reporting Layer. Handles API orchestration with Google Sheets and Drive.
- **UI (`src/ui.py`):** The Face. A Streamlit interface that streams the AI's "thoughts" in real-time.

## 🚀 The Result
A production-ready pipeline that intelligently handles "Killed Parcels," logs every action for accountability, and provides a professional "Decompressed" report for Seattle housing developments.

---
*Built for the Gemini 3 API Hackathon 2026. Data to Truth. Truth to Housing.*
