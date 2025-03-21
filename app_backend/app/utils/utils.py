from typing import List, Dict, Any, Tuple
from app_backend.app.core.config import gmail_auth
import base64
from googleapiclient.errors import HttpError 
import os
import json

class GmailBase:
    def __init__(self, label: str, max_results: int = 5):
        self.label = label
        self.content = []
        self.service = gmail_auth.create_service()
        self.max_results = max_results
        self.cache_dir = "gmail_cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        if not self.service:
            raise Exception("Failed to authenticate Gmail service")

    def load_label_message(self) -> List[Dict[str, Any]]:
        try:
            
            if not self.label:
                return []
            cache_file = os.path.join(self.cache_dir, f"{self.label}_messages.json")
            if os.path.exists(cache_file):
                with open(cache_file, "r") as f:
                    return json.load(f)

            results = self.service.users().labels().list(userId='me').execute()
            labels = results.get('labels', [])
            
            folder_label_id = next(
                (label['id'] for label in labels 
                 if label.get('name', '').lower() == self.label.lower()), 
                None
            )
            
            if not folder_label_id:
                raise ValueError(f"Label '{self.label}' not found in Gmail")
            
            self.label_id = [folder_label_id]
            batch_size = 20
            messages = []
            page_token = None
            
            while True:
                max_results_value = (
                    min(500, self.max_results - len(messages)) 
                    if self.max_results else 500
                )
                max_results_value = max(1, max_results_value)
                results = self.service.users().messages().list(
                    userId='me',
                    labelIds=self.label_id,
                    maxResults= batch_size,
                    pageToken=page_token
                ).execute()
                
                messages.extend(results.get('messages', []))
                page_token = results.get('nextPageToken')
                if not page_token or (self.max_results and len(messages) >= self.max_results):
                    break

            self.content = [self.get_email_message_details(msg['id'])
                            for msg in messages
                             ]
            with open(cache_file, "w") as f:
                json.dump(self.content, f, indent=4)            
            return self.content
        except HttpError as http_err:
            print(f"API error: {http_err}")
            return []
        except ValueError as ve:
            print(f"Configuration error: {ve}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []

    def extract_message_content(self, payload: Dict) -> Tuple[str, List[Dict]]:
        body_parts = []
        attachments = []
        self._process_parts(payload.get('parts', []), body_parts, attachments)
        
        if not payload.get('parts') and 'body' in payload:
            body_data = payload['body'].get('data')
            if body_data:
                body_parts.append(base64.urlsafe_b64decode(body_data).decode('utf-8'))
        
        return '\n'.join(body_parts), attachments

    def _process_parts(self, parts: List[Dict], 
                      body_parts: List[str], 
                      attachments: List[Dict]) -> None:
        for part in parts:
            mime_type = part.get('mimeType', '')
            filename = part.get('filename', '')
            
            if filename:  
                attachments.append({
                    'filename': filename,
                    'size': part['body'].get('size', 0),
                    'attachment_id': part['body'].get('attachmentId')
                })
            elif mime_type == 'text/plain' and 'data' in part.get('body', {}):
                body_parts.append(base64.urlsafe_b64decode(
                    part['body']['data']).decode('utf-8'))
            elif mime_type.startswith('multipart/'):
                self._process_parts(part.get('parts', []), body_parts, attachments)

    def get_email_message_details(self, msg_id: str) -> Dict[str, Any]:
        message = self.get_email_message(msg_id)
        if not message:
            return {}
            
        payload = message.get('payload', {})
        headers = payload.get('headers', [])
        body_content, attachments = self.extract_message_content(payload)
        
        return {
            'id': msg_id,
            'subject': self._get_header(headers, 'Subject'),
            'from': self._get_header(headers, 'From'),
            'date': self._get_header(headers, 'Date'),
            'body': body_content,
            'has_attachment': len(attachments) > 0,
            'attachments': attachments
        }

    def get_email_message(self, msg_id: str) -> Dict:
        try:
            return self.service.users().messages().get(
                userId='me', 
                id=msg_id
            ).execute()
        except HttpError as http_err:
            print(f"API error retrieving message {msg_id}: {http_err}")
            return {}
        except Exception as e:
            print(f"Unexpected error retrieving message {msg_id}: {e}")
            return {}

    @staticmethod
    def _get_header(headers: List[Dict], name: str) -> str:
        return next((h['value'] for h in headers 
                     if h['name'].lower() == name.lower()), '')