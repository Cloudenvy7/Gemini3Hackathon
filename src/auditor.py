import os, json, re
from google import genai
from google.genai import types

MODEL_ID = "gemini-3-flash-preview"
_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key or api_key == "DEBUG": # Support debug/mocking
            return None
        _client = genai.Client(api_key=api_key)
    return _client

def confirm_parcel_id_stream(address):
    prompt = (
        f"Search the web for the 10-digit King County Parcel Number (PIN) for {address}. "
        "Check Zillow and Redfin. Explain your reasoning. "
        "End with 'FINAL_PIN: [10-digits]'."
    )
    client = get_client()
    if not client:
        return None
    try:
        # Request stream with Thinking enabled
        return client.models.generate_content_stream(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())],
                thinking_config=types.ThinkingConfig(thinking_level="HIGH"),
                temperature=1.0
            )
        )
    except Exception as e:
        print(f"CRITICAL SDK ERROR: {e}")
        return None

def analyze_parcel(data):
    prompt = f"Perform a Pre-Permit DADU audit: {json.dumps(data)}."
    client = get_client()
    if not client:
        return "Gemini API Key missing."
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt,
            config=types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_level="HIGH"))
        )
        return response.text
    except:
        return "Analysis failed."
