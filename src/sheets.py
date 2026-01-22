import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleSheetsManager:
    def __init__(self, credentials_path='service_account.json'):
        self.credentials_path = credentials_path
        self.scopes = ['https://www.googleapis.com/auth/spreadsheets']
        self.service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticates using a service account JSON file."""
        if not os.path.exists(self.credentials_path):
            print(f"⚠️ Warning: {self.credentials_path} not found. Google Sheets integration disabled.")
            return

        try:
            creds = service_account.Credentials.from_service_account_file(
                self.credentials_path, scopes=self.scopes + ['https://www.googleapis.com/auth/drive.file'])
            self.service = build('sheets', 'v4', credentials=creds)
            self.drive_service = build('drive', 'v3', credentials=creds)
            print("✅ Google Sheets & Drive API Authenticated.")
        except Exception as e:
            print(f"❌ Authentication Failed: {e}")

    def upsert_parcel_tab(self, spreadsheet_id, pin, data_blocks):
        """
        Creates or updates a tab named by PIN with structured data blocks.
        data_blocks: List of dicts {'section': str, 'rows': [[field, value, source, updated_at]]}
        """
        if not self.service:
            return {"error": "Google Sheets service not initialized."}

        try:
            # 1. Ensure the tab exists
            self._ensure_tab_exists(spreadsheet_id, pin)

            # 2. Prepare the update body
            all_values = []
            for block in data_blocks:
                all_values.append([f"--- {block['section']} ---"])
                all_values.extend(block['rows'])
                all_values.append([]) # Spacer row

            body = {'values': all_values}
            range_name = f"PIN_{pin}!A1"

            # 3. Write data to the sheet (Overwrite)
            self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()

            return {"success": True, "tab_url": f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={self._get_sheet_id(spreadsheet_id, f'PIN_{pin}')}"}

        except HttpError as err:
            return {"error": f"API Error: {err}"}

    def _ensure_tab_exists(self, spreadsheet_id, pin):
        """Creates a new tab if it doesn't exist."""
        sheet_name = f"PIN_{pin}"
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = spreadsheet.get('sheets', [])
        
        exists = any(s.get('properties', {}).get('title') == sheet_name for s in sheets)
        
        if not exists:
            requests = [{
                'addSheet': {
                    'properties': {'title': sheet_name}
                }
            }]
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={'requests': requests}
            ).execute()
            print(f"Created new tab: {sheet_name}")

    def _get_sheet_id(self, spreadsheet_id, title):
        """Helper to get the gid for a specific sheet title."""
        spreadsheet = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        for s in spreadsheet.get('sheets', []):
            if s.get('properties', {}).get('title') == title:
                return s.get('properties', {}).get('sheetId')
        return 0

    def create_site_database(self, title="Pre-Permit AI: Master Site Database"):
        """Creates a new spreadsheet for all project tracking."""
        if not self.service:
            return {"error": "Service not initialized"}
        try:
            spreadsheet = {'properties': {'title': title}}
            spreadsheet = self.service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()
            sheet_id = spreadsheet.get('spreadsheetId')
            return {"success": True, "spreadsheet_id": sheet_id, "url": f"https://docs.google.com/spreadsheets/d/{sheet_id}"}
        except Exception as e:
            return {"error": str(e)}
