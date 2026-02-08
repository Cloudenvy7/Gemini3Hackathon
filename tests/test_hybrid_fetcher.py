import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from fetcher import ArchitecturalFetcher

class TestHybridFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = ArchitecturalFetcher()

    @patch('requests.get')
    def test_hybrid_merge_success(self, mock_get):
        # Mock Layer 2 response (Outdated Zoning + Geometry)
        mock_res2 = MagicMock()
        mock_res2.json.return_value = {
            "features": [{
                "attributes": {"PIN": "123", "ZONING": "SF5000", "LOTAREA": 5000, "FAR_FACTOR": 0.5},
                "geometry": {"rings": [[[0,0], [0,1], [1,1], [1,0], [0,0]]]}
            }]
        }
        
        # Mock Layer 0 response (Current Authoritative Zoning via spatial lookup)
        mock_res0 = MagicMock()
        mock_res0.json.return_value = {
            "features": [{"attributes": {"ZONING": "NR3"}}]
        }
        
        mock_get.side_effect = [mock_res2, mock_res0]

        result = self.fetcher.fetch_architectural_data("123")
        
        # Verify Hybrid Truth
        self.assertEqual(result["zoning_current"], "NR3")
        self.assertEqual(result["lotarea"], 5000)
        
    @patch('requests.get')
    def test_investigator_fallback(self, mock_get):
        # Mock initial failure (Killed Parcel)
        mock_fail = MagicMock()
        mock_fail.json.return_value = {"features": []}
        
        # Mock success after resolving PIN (0609000105 -> 0609000106)
        mock_success = MagicMock()
        mock_success.json.return_value = {
            "features": [{"attributes": {"PIN": "0609000106", "ZONING": "NR3"}}]
        }
        
        mock_get.side_effect = [mock_fail, mock_success, mock_success]

        result = self.fetcher.fetch_architectural_data("0609000105")
        
        self.assertIn("provenance_note", result)
        self.assertIn("Original PIN 0609000105 was killed/retired", result["provenance_note"])
        self.assertEqual(result["pin"], "0609000106")

if __name__ == '__main__':
    unittest.main()
