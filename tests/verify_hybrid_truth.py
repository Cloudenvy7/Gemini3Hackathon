import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from fetcher import ArchitecturalFetcher
import json

def test_examples():
    fetcher = ArchitecturalFetcher()
    examples = [
        {"name": "NR3 Primary Case Study", "pin": "9906000090"},
        {"name": "2026 Rezone Case Study", "pin": "6821102135"}
    ]
    
    for ex in examples:
        print(f"\n--- Fetching Hybrid Truth for {ex['name']} (PIN: {ex['pin']}) ---")
        result = fetcher.fetch_architectural_data(ex['pin'])
        
        if "error" in result:
            print(f"Error: {result['error']}")
            continue

        print(f"Current Zoning (Layer 1 Authority): {result.get('zoning_current')}")
        print(f"Base Zoning (Layer 0 Centroid): {result.get('zoning_base')}")
        print(f"Legacy Zoning (Layer 2 Capacity): {result.get('zoning_legacy')}")
        print(f"Data Provenance: {result.get('zoning_provenance')}")
        
        # Check for technical attributes
        attr_count = len(result)
        print(f"Total Attributes Merged: {attr_count}")
        print(f"Sample - Max Res Floor Area: {result.get('max_res_fl_area')}")

if __name__ == "__main__":
    test_examples()
