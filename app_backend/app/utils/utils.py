from typing import List, Dict, Any
from app_backend.app.core.config import gmail_auth
import base64

class GmailBase:
    def __init__(self, label: str):
        self.label = label
        self.content = []
        self.service = gmail_auth.create_service()
        if not self.service:
            raise Exception("Failed to authenticate Gmail service")

    def load_label_message(self) -> List[Dict[str, Any]]:
        try:
            messages = []
            page_token = None
            while True:
                results = self.service.users().messages().list(
                    userId='me',
                    labelIds=[self.label],
                    pageToken=page_token
                ).execute()
                messages.extend(results.get('messages', []))
                page_token = results.get('nextPageToken')
                if not page_token:
                    break
            self.content = []
            for msg in messages:
                msg_id = msg['id']
                message_details = self.get_email_message_details(msg_id)
                self.content.append(message_details)
            return self.content
        except Exception as e:
            print(f"Error loading messages: {e}")
            return []

    def extract_message_body(self, payload: Dict) -> str:
        body = []
        parts = payload.get('parts', [])
        if parts:
            for part in parts:
                part_body = self.extract_message_body(part)
                if part_body:
                    body.append(part_body)
        else:
            mime_type = payload.get('mimeType', '')
            if mime_type.startswith('text/'):
                data = payload.get('body', {}).get('data', '')
                if data:
                    try:
                        decoded = base64.urlsafe_b64decode(data).decode('utf-8')
                        body.append(decoded)
                    except Exception as e:
                        print(f"Error decoding message body: {e}")
        return '\n'.join(body)

    def get_email_message(self, msg_id: str) -> Dict:
        """Retrieve a message by ID."""
        try:
            return self.service.users().messages().get(userId='me', id=msg_id).execute()
        except Exception as e:
            print(f"Error retrieving message {msg_id}: {e}")
            return {}

    def get_email_message_details(self, msg_id: str) -> Dict[str, Any]:
        message = self.get_email_message(msg_id)
        if not message:
            return {}
        payload = message.get('payload', {})
        headers = payload.get('headers', [])
        
        return {
            'id': msg_id,
            'subject': self._get_header(headers, 'Subject'),
            'from': self._get_header(headers, 'From'),
            'date': self._get_header(headers, 'Date'),
            'body': self.extract_message_body(payload)
        }

    @staticmethod
    def _get_header(headers: List[Dict], name: str) -> str:
        return next((h['value'] for h in headers if h['name'] == name), '')