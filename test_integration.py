import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Ensure src is in the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fetcher import ArchitecturalFetcher
from auditor import analyze_parcel

class TestPrePermitIntegration(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_architectural_data_success(self, mock_get):
        # Mocking the Seattle API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "features": [{
                "attributes": {
                    "PIN": "1234567890",
                    "Zoning": "SF 5000"
                }
            }]
        }
        mock_get.return_value = mock_response

        fetcher = ArchitecturalFetcher()
        data = fetcher.fetch_architectural_data("1234567890")

        self.assertEqual(data['pin'], "1234567890")
        self.assertEqual(data['zoning'], "SF 5000")

    @patch('auditor.get_client')
    def test_analyze_parcel_success(self, mock_get_client):
        # Mocking Gemini response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Audit Passed"
        mock_client.models.generate_content.return_value = mock_response
        mock_get_client.return_value = mock_client

        data = {"pin": "1234567890", "zoning": "SF 5000"}
        result = analyze_parcel(data)

        self.assertEqual(result, "Audit Passed")

    @patch('fetcher.Producer')
    def test_publish_audit_event(self, mock_producer_class):
        # Mocking Kafka Producer
        mock_producer = mock_producer_class.return_value
        
        with patch.dict(os.environ, {
            'BOOTSTRAP_SERVERS': 'test_server',
            'SASL_USERNAME': 'test_user',
            'SASL_PASSWORD': 'test_password'
        }):
            fetcher = ArchitecturalFetcher()
            # Manually set producer since it won't init without env vars in real code
            fetcher.producer = mock_producer
            
            test_data = {"test": "data"}
            fetcher.publish_audit_event(test_data)
            
            mock_producer.produce.assert_called_once()
            args, kwargs = mock_producer.produce.call_args
            self.assertEqual(kwargs['topic'], "site.fetch.completed")
            payload = json.loads(kwargs['value'])
            self.assertEqual(payload['data'], test_data)

if __name__ == '__main__':
    unittest.main()
