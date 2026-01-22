import streamlit as st
import re
from fetcher import ArchitecturalFetcher
from auditor import confirm_parcel_id_stream, analyze_parcel
from sheets import GoogleSheetsManager

st.set_page_config(page_title="Pre Permit AI", page_icon="🏠")
st.title("🏠 Pre Permit AI")

# --- Persistent State ---
if 'pin' not in st.session_state: st.session_state.pin = None
if 'city_data' not in st.session_state: st.session_state.city_data = None
if 'audit_result' not in st.session_state: st.session_state.audit_result = None

addr = st.text_input("Property Address", value="11520 Roosevelt Way NE")

if st.button("Run Analysis"):
    full_response = ""
    st.session_state.pin = None
    
    with st.status("🤖 Gemini 3 Agent is reasoning...", expanded=True) as status:
        thought_placeholder = st.empty()
        try:
            stream = confirm_parcel_id_stream(addr)
            if stream:
                for chunk in stream:
                    if chunk.candidates:
                        for part in chunk.candidates[0].content.parts:
                            if hasattr(part, 'text') and part.text:
                                full_response += part.text
                            elif hasattr(part, 'thought'):
                                full_response += f"\n(Thinking: {part.thought})\n"
                            thought_placeholder.markdown(full_response)
                
                match = re.search(r'\b\d{10}\b', full_response)
                if match:
                    st.session_state.pin = match.group(0)
                    status.update(label=f"✅ Found PIN: {st.session_state.pin}", state="complete")
                else:
                    status.update(label="❌ PIN Not Found", state="error")
            else:
                st.error("Failed to initialize stream. Verify API Key.")
        except Exception as e:
            st.error(f"Stream Error: {str(e)}")

    if st.session_state.pin:
        fetcher = ArchitecturalFetcher()
        with st.spinner("📊 Pulling City Records..."):
            st.session_state.city_data = fetcher.fetch_architectural_data(st.session_state.pin)
        
        with st.spinner("🧠 Auditing Neighborhood Residential Codes..."):
            st.session_state.audit_result = analyze_parcel(st.session_state.city_data)

# Display results if they exist in state
if st.session_state.pin and st.session_state.city_data:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("City Data")
        st.json(st.session_state.city_data)
    with col2:
        st.subheader("Gemini 3 Audit")
        st.write(st.session_state.audit_result)
    
    # 📡 Sync to Confluent
    if st.button("📡 Sync to Run Ledger"):
        fetcher = ArchitecturalFetcher()
        audit_payload = {
            "address": addr,
            "pin": st.session_state.pin,
            "city_data": st.session_state.city_data,
            "audit_result": st.session_state.audit_result
        }
        fetcher.publish_audit_event(audit_payload)
        st.success("Audit Logged to Confluent.")

    # --- Google Sheets Export Section ---
    st.divider()
    st.subheader("🏁 Finalize & Export")
    
    colA, colB = st.columns([2,1])
    with colA:
        spreadsheet_input = st.text_input("Master Google Sheet ID", help="Paste the ID or the full URL. Leave blank to create a new one.")
        
        # Auto-extract ID if full URL is pasted
        spreadsheet_id = spreadsheet_input
        if "spreadsheets/d/" in spreadsheet_input:
            spreadsheet_id = spreadsheet_input.split("spreadsheets/d/")[1].split("/")[0]

    with colB:
        if st.button("🚀 Export to Site Sheet"):
            sheets_mgr = GoogleSheetsManager()
            if not sheets_mgr.service:
                st.error("Google Sheets API not configured. Please ensure `service_account.json` exists.")
            else:
                with st.spinner("📑 Organizing Airtable Schema..."):
                    # 1. Create if missing
                    if not spreadsheet_id:
                        new_sheet = sheets_mgr.create_site_database()
                        if "spreadsheet_id" in new_sheet:
                            spreadsheet_id = new_sheet["spreadsheet_id"]
                            st.info(f"Created New Master Sheet! ID: {spreadsheet_id}")
                        else:
                            st.error(f"Creation Failed: {new_sheet.get('error')}")
                            st.stop()
                    
                    # 2. Map data
                    fetcher = ArchitecturalFetcher()
                    data_blocks, run_id = fetcher.map_to_airtable_schema(st.session_state.city_data)
                    
                    # 3. Export
                    result = sheets_mgr.upsert_parcel_tab(spreadsheet_id, st.session_state.pin, data_blocks)
                    if "success" in result:
                        st.success(f"Exported Successfully! Run ID: {run_id}")
                        st.link_button("📂 View Record in Google Sheets", result["tab_url"])
                    else:
                        st.error(f"Export Failed: {result.get('error')}")

st.divider()
st.caption("🚀 Version: Pre Permit AI v2.3.2 (Decompressed) | SDK: 1.47.0 | Model: Gemini 3 Flash")
