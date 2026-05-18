"""
API Request/Response Models
Pydantic models for API validation
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


# Request Models

class IngestRequest(BaseModel):
    """Request to ingest data - supports both direct content and fetching from sources"""
    source_type: str = Field(..., description="Type of source: slack, jira, google_drive, gmail, transcript")
    
    # Option 1: Provide content directly
    content: Optional[str] = Field(None, description="Content to ingest (if providing directly)")
    source_id: Optional[str] = Field(None, description="Unique identifier for the source")
    
    # Option 2: Fetch from real source
    fetch_from_source: bool = Field(False, description="If true, fetch data from real API")
    channel: Optional[str] = Field(None, description="Slack channel name (for slack source)")
    project: Optional[str] = Field(None, description="Jira project key (for jira source)")
    folder: Optional[str] = Field(None, description="Google Drive folder name (for google_drive source)")
    query: Optional[str] = Field(None, description="Search query (for gmail source)")
    limit: int = Field(100, description="Maximum number of items to fetch")
    
    metadata: Optional[Dict[str, Any]] = Field(default={}, description="Additional metadata")


class JiraTriggerRequest(BaseModel):
    """Request to trigger Jira analysis"""
    ticket_title: str = Field(..., description="Title of the Jira ticket")
    ticket_description: str = Field(..., description="Description of the ticket")
    created_by: Optional[str] = Field(None, description="User who created the ticket")


class DocumentTriggerRequest(BaseModel):
    """Request to trigger document analysis"""
    document_title: str = Field(..., description="Title of the document")
    content: str = Field(..., description="Document content")


class QueryRequest(BaseModel):
    """Request to query knowledge base"""
    question: str = Field(..., description="Natural language question")
    user_id: Optional[str] = Field(None, description="User making the query")
    context: Optional[str] = Field(None, description="Additional context")


# Response Models

class IngestResponse(BaseModel):
    """Response from ingestion"""
    items_extracted: int = Field(..., description="Number of knowledge items extracted")
    knowledge_ids: List[str] = Field(..., description="IDs of extracted knowledge items")
    message: str = Field(..., description="Status message")


class KnowledgeItemResponse(BaseModel):
    """Knowledge item response"""
    id: str
    content_type: str
    title: str
    summary: str
    key_facts: List[str]
    people_involved: List[str]
    teams_involved: List[str]
    date_occurred: Optional[str]
    topics: List[str]
    outcome: str
    importance_score: int
    source_type: str
    source_reference: str


class ProactiveAlertResponse(BaseModel):
    """Proactive alert response"""
    alert_id: str
    trigger_type: str
    trigger_content: str
    alert_level: str
    headline: str
    context_items: List[Dict[str, Any]]
    synthesized_insight: str
    recommended_actions: List[str]
    relevant_people: List[str]
    confidence_score: int
    timestamp: str


class StatsResponse(BaseModel):
    """Statistics response"""
    total_knowledge_items: int
    items_by_type: Dict[str, int]
    items_by_outcome: Dict[str, int]
    recent_alerts: int
    top_topics: List[Dict[str, Any]]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    knowledge_items: int
    vector_store: str
    demo_mode: bool


class ExpertResponse(BaseModel):
    """Expert search response"""
    name: str
    expertise_areas: List[str]
    evidence: List[Dict[str, Any]]
    relevance_score: float
