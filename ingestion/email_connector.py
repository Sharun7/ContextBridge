"""
Email (Gmail) Ingestion Connector
Fetches emails from Gmail with REAL API integration
"""

import json
import logging
from typing import List, Dict, Optional
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
import base64
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


class EmailConnector:
    """Connector for Gmail email ingestion with REAL API support"""
    
    def __init__(
        self, 
        demo_mode: bool = True,
        credentials_path: Optional[str] = None,
        service_account_path: Optional[str] = None
    ):
        self.demo_mode = demo_mode
        self.mock_data_path = Path("demo/data/emails.json")
        self.gmail_service = None
        
        if not demo_mode:
            try:
                # Try service account first, then user credentials
                if service_account_path:
                    creds = service_account.Credentials.from_service_account_file(
                        service_account_path,
                        scopes=['https://www.googleapis.com/auth/gmail.readonly']
                    )
                elif credentials_path:
                    creds = Credentials.from_authorized_user_file(
                        credentials_path,
                        ['https://www.googleapis.com/auth/gmail.readonly']
                    )
                else:
                    logger.error("No credentials provided for Gmail")
                    return
                
                self.gmail_service = build('gmail', 'v1', credentials=creds)
                logger.info("✅ Gmail API connection established")
            except Exception as e:
                logger.error(f"❌ Gmail API connection failed: {e}")
                raise
    
    def fetch_emails(
        self,
        query: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Fetch emails from Gmail
        
        Args:
            query: Gmail search query (None = all emails)
            limit: Maximum number of emails to fetch
            
        Returns:
            List of email dictionaries
        """
        if self.demo_mode:
            return self._fetch_mock_emails(query, limit)
        else:
            return self._fetch_real_emails(query, limit)
    
    def _fetch_mock_emails(
        self,
        query: Optional[str],
        limit: int
    ) -> List[Dict]:
        """Fetch emails from mock data file"""
        try:
            if not self.mock_data_path.exists():
                logger.warning(f"Mock data file not found: {self.mock_data_path}")
                return []
            
            with open(self.mock_data_path, 'r', encoding='utf-8') as f:
                emails = json.load(f)
            
            # Simple query filtering (if needed)
            if query:
                emails = [e for e in emails if query.lower() in str(e).lower()]
            
            # Apply limit
            emails = emails[:limit]
            
            logger.info(f"Fetched {len(emails)} mock emails")
            return emails
            
        except Exception as e:
            logger.error(f"Error fetching mock emails: {e}")
            return []
    
    def _fetch_real_emails(
        self,
        query: Optional[str],
        limit: int
    ) -> List[Dict]:
        """Fetch emails from real Gmail API"""
        if not self.gmail_service:
            logger.error("Gmail service not initialized")
            return []
        
        try:
            emails = []
            
            # Fetch message list
            results = self.gmail_service.users().messages().list(
                userId='me',
                q=query if query else '',
                maxResults=limit
            ).execute()
            
            messages = results.get('messages', [])
            
            for msg in messages:
                try:
                    # Get full message details
                    message = self.gmail_service.users().messages().get(
                        userId='me',
                        id=msg['id'],
                        format='full'
                    ).execute()
                    
                    # Extract headers
                    headers = message['payload']['headers']
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                    from_email = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                    to_email = next((h['value'] for h in headers if h['name'] == 'To'), 'Unknown')
                    date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
                    
                    # Extract body
                    body = ""
                    if 'parts' in message['payload']:
                        for part in message['payload']['parts']:
                            if part['mimeType'] == 'text/plain':
                                if 'data' in part['body']:
                                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                                    break
                    elif 'body' in message['payload'] and 'data' in message['payload']['body']:
                        body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8', errors='ignore')
                    
                    emails.append({
                        'id': message['id'],
                        'thread_id': message['threadId'],
                        'subject': subject,
                        'from': from_email,
                        'to': to_email,
                        'date': date,
                        'body': body,
                        'snippet': message.get('snippet', ''),
                        'labels': message.get('labelIds', []),
                        'source_type': 'gmail',
                        'source_id': f"gmail_{message['id']}"
                    })
                    
                except Exception as e:
                    logger.warning(f"Error fetching email {msg['id']}: {e}")
                    continue
            
            logger.info(f"✅ Fetched {len(emails)} emails from Gmail API")
            return emails
            
        except HttpError as e:
            logger.error(f"❌ Gmail API error: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Error fetching Gmail emails: {e}")
            return []
