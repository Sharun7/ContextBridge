"""
Jira Ticket Ingestion Connector
Fetches tickets and comments from Jira with REAL API integration
"""

import json
import logging
from typing import List, Dict, Optional
from pathlib import Path
from jira import JIRA
from jira.exceptions import JIRAError

logger = logging.getLogger(__name__)


class JiraConnector:
    """Connector for Jira ticket ingestion with REAL API support"""
    
    def __init__(
        self, 
        demo_mode: bool = True,
        jira_url: Optional[str] = None,
        jira_email: Optional[str] = None,
        jira_api_token: Optional[str] = None
    ):
        self.demo_mode = demo_mode
        self.mock_data_path = Path("demo/data/jira_tickets.json")
        self.jira_client = None
        
        if not demo_mode and jira_url and jira_email and jira_api_token:
            try:
                self.jira_client = JIRA(
                    server=jira_url,
                    basic_auth=(jira_email, jira_api_token)
                )
                # Test the connection
                self.jira_client.myself()
                logger.info("✅ Jira API connection established")
            except JIRAError as e:
                logger.error(f"❌ Jira API connection failed: {e}")
                raise
    
    def fetch_tickets(
        self,
        project: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """
        Fetch tickets from Jira
        
        Args:
            project: Specific project to fetch from (None = all projects)
            limit: Maximum number of tickets to fetch
            
        Returns:
            List of ticket dictionaries
        """
        if self.demo_mode:
            return self._fetch_mock_tickets(project, limit)
        else:
            return self._fetch_real_tickets(project, limit)
    
    def _fetch_mock_tickets(
        self,
        project: Optional[str],
        limit: int
    ) -> List[Dict]:
        """Fetch tickets from mock data file"""
        try:
            if not self.mock_data_path.exists():
                logger.warning(f"Mock data file not found: {self.mock_data_path}")
                return []
            
            with open(self.mock_data_path, 'r', encoding='utf-8') as f:
                tickets = json.load(f)
            
            # Filter by project if specified
            if project:
                tickets = [t for t in tickets if t.get('project') == project]
            
            # Apply limit
            tickets = tickets[:limit]
            
            logger.info(f"Fetched {len(tickets)} mock Jira tickets")
            return tickets
            
        except Exception as e:
            logger.error(f"Error fetching mock Jira tickets: {e}")
            return []
    
    def _fetch_real_tickets(
        self,
        project: Optional[str],
        limit: int
    ) -> List[Dict]:
        """Fetch tickets from real Jira API"""
        if not self.jira_client:
            logger.error("Jira client not initialized. Provide jira_url, jira_email, and jira_api_token.")
            return []
        
        try:
            tickets = []
            
            # Build JQL query
            jql = f"project = {project}" if project else "ORDER BY created DESC"
            
            # Fetch issues
            issues = self.jira_client.search_issues(
                jql,
                maxResults=limit,
                fields='summary,description,status,priority,created,updated,assignee,reporter,comment'
            )
            
            for issue in issues:
                # Get comments
                comments = []
                for comment in issue.fields.comment.comments:
                    comments.append({
                        'author': comment.author.displayName if hasattr(comment.author, 'displayName') else 'Unknown',
                        'body': comment.body,
                        'created': comment.created
                    })
                
                tickets.append({
                    'id': issue.key,
                    'project': issue.fields.project.key,
                    'title': issue.fields.summary,
                    'description': issue.fields.description or '',
                    'status': issue.fields.status.name,
                    'priority': issue.fields.priority.name if issue.fields.priority else 'None',
                    'created': issue.fields.created,
                    'updated': issue.fields.updated,
                    'assignee': issue.fields.assignee.displayName if issue.fields.assignee else 'Unassigned',
                    'reporter': issue.fields.reporter.displayName if issue.fields.reporter else 'Unknown',
                    'comments': comments,
                    'source_type': 'jira',
                    'source_id': f"jira_{issue.key}"
                })
            
            logger.info(f"✅ Fetched {len(tickets)} tickets from Jira API")
            return tickets
            
        except JIRAError as e:
            logger.error(f"❌ Jira API error: {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Error fetching Jira tickets: {e}")
            return []
    
    def get_projects(self) -> List[str]:
        """Get list of available projects"""
        if self.demo_mode:
            tickets = self._fetch_mock_tickets(None, 1000)
            projects = list(set(t.get('project', '') for t in tickets))
            return sorted(projects)
        else:
            if not self.jira_client:
                logger.error("Jira client not initialized")
                return []
            
            try:
                projects = self.jira_client.projects()
                project_keys = [p.key for p in projects]
                logger.info(f"✅ Found {len(project_keys)} Jira projects")
                return sorted(project_keys)
            except JIRAError as e:
                logger.error(f"❌ Error fetching projects: {e}")
                return []
