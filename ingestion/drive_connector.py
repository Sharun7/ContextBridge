"""
Google Drive Document Ingestion Connector
Fetches documents from Google Drive with REAL API integration
"""

import json
import logging
from typing import List, Dict, Optional
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
import io
from googleapiclient.http import MediaIoBaseDownload

logger = logging.getLogger(__name__)


class DriveConnector:
    """Connector for Google Drive document ingestion with REAL API support"""
    
    def __init__(
        self, 
        demo_mode: bool = True,
        credentials_path: Optional[str] = None,
        service_account_path: Optional[str] = None
    ):
        self.demo_mode = demo_mode
        self.mock_data_path = Path("demo/data/documents.json")
        self.drive_service = None
        
        if not demo_mode:
            try:
                # Try service account first, then user credentials
                if service_account_path:
                    creds = service_account.Credentials.from_service_account_file(
                        service_account_path,
                        scopes=['https://www.googleapis.com/auth/drive.readonly']
                    )
                elif credentials_path:
                    creds = Credentials.from_authorized_user_file(
                        credentials_path,
                        ['https://www.googleapis.com/auth/drive.readonly']
                    )
                else:
                    logger.error("No credentials provided for Google Drive")
                    return
                
                self.drive_service = build('drive', 'v3', credentials=creds)
                logger.info("✅ Google Drive API connection established")
            except Exception as e:
                logger.error(f"❌ Google Drive API connection failed: {e}")
                raise
    
    def fetch_documents(
        self,
        folder: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Fetch documents from Google Drive
        
        Args:
            folder: Specific folder to fetch from (None = all folders)
            limit: Maximum number of documents to fetch
            
        Returns:
            List of document dictionaries
        """
        if self.demo_mode:
            return self._fetch_mock_documents(folder, limit)
        else:
            return self._fetch_real_documents(folder, limit)
    
    def _fetch_mock_documents(
        self,
        folder: Optional[str],
        limit: int
    ) -> List[Dict]:
        """Fetch documents from mock data file"""
        try:
            if not self.mock_data_path.exists():
                logger.warning(f"Mock data file not found: {self.mock_data_path}")
                return []
            
            with open(self.mock_data_path, 'r', encoding='utf-8') as f:
                documents = json.load(f)
            
            # Filter by folder if specified
            if folder:
                documents = [d for d in documents if d.get('folder') == folder]
            
            # Apply limit
            documents = documents[:limit]
            
            logger.info(f"Fetched {len(documents)} mock Drive documents")
            return documents
            
        except Exception as e:
            logger.error(f"Error fetching mock Drive documents: {e}")
            return []
    
    def _fetch_real_documents(
        self,
        folder: Optional[str],
        limit: int
    ) -> List[Dict]:
        """Fetch documents from real Google Drive API"""
        if not self.drive_service:
            logger.error("Google Drive service not initialized")
            return []
        
        try:
            documents = []
            
            # Build query
            query = "mimeType='application/vnd.google-apps.document' or mimeType='application/pdf' or mimeType='text/plain'"
            if folder:
                # Find folder ID by name
                folder_results = self.drive_service.files().list(
                    q=f"name='{folder}' and mimeType='application/vnd.google-apps.folder'",
                    fields="files(id, name)"
                ).execute()
                
                if folder_results.get('files'):
                    folder_id = folder_results['files'][0]['id']
                    query += f" and '{folder_id}' in parents"
            
            # Fetch files
            results = self.drive_service.files().list(
                q=query,
                pageSize=limit,
                fields="files(id, name, mimeType, createdTime, modifiedTime, owners, description, webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            
            for file in files:
                # Get file content
                content = ""
                try:
                    if file['mimeType'] == 'application/vnd.google-apps.document':
                        # Export Google Doc as plain text
                        request = self.drive_service.files().export_media(
                            fileId=file['id'],
                            mimeType='text/plain'
                        )
                    else:
                        # Download other file types
                        request = self.drive_service.files().get_media(fileId=file['id'])
                    
                    fh = io.BytesIO()
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                    
                    content = fh.getvalue().decode('utf-8', errors='ignore')
                except Exception as e:
                    logger.warning(f"Could not fetch content for {file['name']}: {e}")
                
                documents.append({
                    'id': file['id'],
                    'title': file['name'],
                    'content': content,
                    'type': file['mimeType'],
                    'created': file.get('createdTime', ''),
                    'modified': file.get('modifiedTime', ''),
                    'author': file['owners'][0]['displayName'] if file.get('owners') else 'Unknown',
                    'url': file.get('webViewLink', ''),
                    'source_type': 'google_drive',
                    'source_id': f"drive_{file['id']}"
                })
            
            logger.info(f"✅ Fetched {len(documents)} documents from Google Drive API")
            return documents
            
        except HttpError as e:
            logger.error(f"❌ Google Drive API error: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Error fetching Google Drive documents: {e}")
            return []
