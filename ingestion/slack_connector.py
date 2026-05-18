"""
Slack Data Ingestion Connector
Fetches messages from Slack channels with REAL API integration
"""

import json
import logging
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)


class SlackConnector:
    """Connector for Slack data ingestion with REAL API support"""
    
    def __init__(self, demo_mode: bool = True, slack_token: Optional[str] = None):
        self.demo_mode = demo_mode
        self.mock_data_path = Path("demo/data/slack_messages.json")
        self.slack_token = slack_token
        self.client = None
        
        if not demo_mode and slack_token:
            try:
                self.client = WebClient(token=slack_token)
                # Test the connection
                self.client.auth_test()
                logger.info("✅ Slack API connection established")
            except SlackApiError as e:
                logger.error(f"❌ Slack API connection failed: {e.response['error']}")
                raise
    
    def fetch_messages(
        self,
        channel: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Fetch messages from Slack channels
        
        Args:
            channel: Specific channel to fetch from (None = all channels)
            limit: Maximum number of messages to fetch
            
        Returns:
            List of message dictionaries
        """
        if self.demo_mode:
            return self._fetch_mock_messages(channel, limit)
        else:
            return self._fetch_real_messages(channel, limit)
    
    def _fetch_mock_messages(
        self,
        channel: Optional[str],
        limit: int
    ) -> List[Dict]:
        """Fetch messages from mock data file"""
        try:
            if not self.mock_data_path.exists():
                logger.warning(f"Mock data file not found: {self.mock_data_path}")
                return []
            
            with open(self.mock_data_path, 'r', encoding='utf-8') as f:
                messages = json.load(f)
            
            # Filter by channel if specified
            if channel:
                messages = [m for m in messages if m.get('channel') == channel]
            
            # Apply limit
            messages = messages[:limit]
            
            logger.info(f"Fetched {len(messages)} mock Slack messages")
            return messages
            
        except Exception as e:
            logger.error(f"Error fetching mock Slack messages: {e}")
            return []
    
    def _fetch_real_messages(
        self,
        channel: Optional[str],
        limit: int
    ) -> List[Dict]:
        """Fetch messages from real Slack API"""
        if not self.client:
            logger.error("Slack client not initialized. Provide slack_token.")
            return []
        
        try:
            messages = []
            
            # Get list of channels if no specific channel provided
            if not channel:
                channels_response = self.client.conversations_list(
                    types="public_channel,private_channel",
                    limit=100
                )
                channels = channels_response['channels']
            else:
                # Find the channel ID by name
                channels_response = self.client.conversations_list(
                    types="public_channel,private_channel",
                    limit=1000
                )
                channels = [c for c in channels_response['channels'] if c['name'] == channel]
            
            # Fetch messages from each channel
            for ch in channels:
                try:
                    history = self.client.conversations_history(
                        channel=ch['id'],
                        limit=min(limit, 100)
                    )
                    
                    for msg in history['messages']:
                        # Get user info
                        user_info = {}
                        if 'user' in msg:
                            try:
                                user_response = self.client.users_info(user=msg['user'])
                                user_info = user_response['user']
                            except:
                                pass
                        
                        messages.append({
                            'id': msg.get('ts', ''),
                            'channel': ch['name'],
                            'channel_id': ch['id'],
                            'author': user_info.get('real_name', user_info.get('name', 'Unknown')),
                            'author_id': msg.get('user', ''),
                            'content': msg.get('text', ''),
                            'timestamp': datetime.fromtimestamp(float(msg.get('ts', 0))).isoformat(),
                            'thread_ts': msg.get('thread_ts'),
                            'reactions': msg.get('reactions', []),
                            'source_type': 'slack',
                            'source_id': f"slack_{ch['id']}_{msg.get('ts', '')}"
                        })
                        
                        if len(messages) >= limit:
                            break
                    
                    if len(messages) >= limit:
                        break
                        
                except SlackApiError as e:
                    logger.warning(f"Error fetching messages from channel {ch['name']}: {e}")
                    continue
            
            logger.info(f"✅ Fetched {len(messages)} messages from Slack API")
            return messages[:limit]
            
        except SlackApiError as e:
            logger.error(f"❌ Slack API error: {e.response['error']}")
            return []
        except Exception as e:
            logger.error(f"❌ Error fetching Slack messages: {e}")
            return []
    
    def get_channels(self) -> List[str]:
        """Get list of available channels"""
        if self.demo_mode:
            messages = self._fetch_mock_messages(None, 1000)
            channels = list(set(m.get('channel', '') for m in messages))
            return sorted(channels)
        else:
            if not self.client:
                logger.error("Slack client not initialized")
                return []
            
            try:
                response = self.client.conversations_list(
                    types="public_channel,private_channel",
                    limit=1000
                )
                channels = [ch['name'] for ch in response['channels']]
                logger.info(f"✅ Found {len(channels)} Slack channels")
                return sorted(channels)
            except SlackApiError as e:
                logger.error(f"❌ Error fetching channels: {e}")
                return []
