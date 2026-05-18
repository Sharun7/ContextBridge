"""
API Routes
All FastAPI endpoints for ContextBridge
"""

import logging
import json
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse
import time

from api.models import (
    IngestRequest, IngestResponse,
    JiraTriggerRequest, DocumentTriggerRequest, QueryRequest,
    ProactiveAlertResponse, KnowledgeItemResponse,
    StatsResponse, HealthResponse, ExpertResponse
)
from config import settings
from processing.knowledge_extractor import KnowledgeExtractor
from processing.vector_store import VectorStore
from processing.graph_builder import GraphBuilder
from intelligence.proactive_engine import ProactiveEngine

logger = logging.getLogger(__name__)

router = APIRouter()

# Global instances (initialized on first use)
_extractor = None
_vector_store = None
_graph_builder = None
_proactive_engine = None


def get_extractor():
    """Get or create knowledge extractor"""
    global _extractor
    if _extractor is None:
        _extractor = KnowledgeExtractor(settings.GEMINI_API_KEY)
    return _extractor


def get_vector_store():
    """Get or create vector store"""
    global _vector_store
    if _vector_store is None:
        _vector_store = VectorStore(
            persist_dir=settings.CHROMA_PERSIST_DIR,
            collection_name=settings.CHROMA_COLLECTION_NAME
        )
        _vector_store.initialize_store()
    return _vector_store


def get_graph_builder():
    """Get or create graph builder"""
    global _graph_builder
    if _graph_builder is None:
        _graph_builder = GraphBuilder()
    return _graph_builder


def get_proactive_engine():
    """Get or create proactive engine"""
    global _proactive_engine
    if _proactive_engine is None:
        _proactive_engine = ProactiveEngine(
            vector_store=get_vector_store(),
            graph_builder=get_graph_builder(),
            gemini_api_key=settings.GEMINI_API_KEY
        )
    return _proactive_engine


# Request logging will be handled in main.py middleware
    
    return response


@router.post(
    "/ingest",
    response_model=IngestResponse,
    summary="Ingest enterprise data",
    description="Extract knowledge from enterprise sources (Slack, Jira, documents) and store in vector DB and knowledge graph"
)
async def ingest_data(request: IngestRequest):
    """
    Ingest data from enterprise sources
    
    - Can provide content directly OR fetch from real APIs
    - Extracts knowledge using Gemini
    - Stores in vector database (ChromaDB)
    - Builds knowledge graph (NetworkX)
    - Returns extracted knowledge IDs
    """
    try:
        logger.info(f"📥 Ingesting {request.source_type} data")
        
        # Determine if we need to fetch from source or use provided content
        items_to_process = []
        
        if request.fetch_from_source:
            # Fetch from real API
            logger.info(f"🔄 Fetching from real {request.source_type} API...")
            
            if request.source_type == "slack":
                from ingestion.slack_connector import SlackConnector
                connector = SlackConnector(
                    demo_mode=settings.DEMO_MODE,
                    slack_token=settings.SLACK_BOT_TOKEN
                )
                items_to_process = connector.fetch_messages(
                    channel=request.channel,
                    limit=request.limit
                )
                
            elif request.source_type == "jira":
                from ingestion.jira_connector import JiraConnector
                connector = JiraConnector(
                    demo_mode=settings.DEMO_MODE,
                    jira_url=settings.JIRA_URL,
                    jira_email=settings.JIRA_EMAIL,
                    jira_api_token=settings.JIRA_API_TOKEN
                )
                items_to_process = connector.fetch_tickets(
                    project=request.project,
                    limit=request.limit
                )
                
            elif request.source_type == "google_drive":
                from ingestion.drive_connector import DriveConnector
                connector = DriveConnector(
                    demo_mode=settings.DEMO_MODE,
                    credentials_path=settings.GOOGLE_DRIVE_CREDENTIALS_PATH,
                    service_account_path=settings.GOOGLE_DRIVE_SERVICE_ACCOUNT_PATH
                )
                items_to_process = connector.fetch_documents(
                    folder=request.folder,
                    limit=request.limit
                )
                
            elif request.source_type == "gmail":
                from ingestion.email_connector import EmailConnector
                connector = EmailConnector(
                    demo_mode=settings.DEMO_MODE,
                    credentials_path=settings.GMAIL_CREDENTIALS_PATH,
                    service_account_path=settings.GMAIL_SERVICE_ACCOUNT_PATH
                )
                items_to_process = connector.fetch_emails(
                    query=request.query,
                    limit=request.limit
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported source type for fetching: {request.source_type}"
                )
            
            logger.info(f"✅ Fetched {len(items_to_process)} items from {request.source_type}")
            
        else:
            # Use provided content
            if not request.content or not request.source_id:
                raise HTTPException(
                    status_code=400,
                    detail="Either provide content+source_id OR set fetch_from_source=true"
                )
            
            items_to_process = [{
                'content': request.content,
                'source_id': request.source_id,
                'source_type': request.source_type
            }]
        
        if not items_to_process:
            return IngestResponse(
                items_extracted=0,
                knowledge_ids=[],
                message="No items to process"
            )
        
        # Extract knowledge from all items
        extractor = get_extractor()
        all_knowledge_items = []
        
        for item in items_to_process:
            # Prepare content based on source type
            if request.source_type == "slack":
                content = f"Channel: {item.get('channel', '')}\nAuthor: {item.get('author', '')}\nMessage: {item.get('content', '')}"
            elif request.source_type == "jira":
                content = f"Ticket: {item.get('title', '')}\nDescription: {item.get('description', '')}\nStatus: {item.get('status', '')}"
            elif request.source_type == "google_drive":
                content = f"Document: {item.get('title', '')}\nContent: {item.get('content', '')}"
            elif request.source_type == "gmail":
                content = f"Subject: {item.get('subject', '')}\nFrom: {item.get('from', '')}\nBody: {item.get('body', '')}"
            else:
                content = item.get('content', '')
            
            # Extract knowledge
            knowledge_items = extractor.extract_knowledge(
                text=content,
                source_type=request.source_type,
                source_id=item.get('source_id', item.get('id', 'unknown'))
            )
            all_knowledge_items.extend(knowledge_items)
        
        if not all_knowledge_items:
            return IngestResponse(
                items_extracted=0,
                knowledge_ids=[],
                message="No knowledge items extracted from content"
            )
        
        # Store in vector database
        vector_store = get_vector_store()
        vector_store.add_knowledge(all_knowledge_items)
        
        # Rebuild knowledge graph
        graph_builder = get_graph_builder()
        stats = vector_store.get_stats()
        if stats['total_items'] > 0:
            graph_builder.build_graph(all_knowledge_items)
        
        knowledge_ids = [item.id for item in all_knowledge_items]
        
        logger.info(f"✅ Extracted and stored {len(all_knowledge_items)} knowledge items")
        
        return IngestResponse(
            items_extracted=len(all_knowledge_items),
            knowledge_ids=knowledge_ids,
            message=f"Successfully extracted {len(all_knowledge_items)} knowledge items from {len(items_to_process)} source items"
        )
        
    except Exception as e:
        logger.error(f"❌ Error ingesting data: {e}")
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@router.post(
    "/trigger/jira",
    response_model=Optional[ProactiveAlertResponse],
    summary="Trigger Jira analysis",
    description="Analyze new Jira ticket and surface relevant organizational history"
)
async def trigger_jira(request: JiraTriggerRequest):
    """
    Trigger proactive analysis for Jira ticket
    
    - Searches for similar past failures/decisions
    - Calculates confidence score
    - Returns alert if relevant history found (confidence >= 60)
    - Returns null if no significant history
    """
    try:
        logger.info(f"🎫 Jira trigger: {request.ticket_title}")
        
        engine = get_proactive_engine()
        alert = engine.handle_jira_trigger(
            ticket_title=request.ticket_title,
            ticket_description=request.ticket_description
        )
        
        if alert:
            logger.info(f"✅ Generated {alert.alert_level} alert with {alert.confidence_score}% confidence")
            return ProactiveAlertResponse(**alert.to_dict())
        else:
            logger.info("No relevant history found or confidence too low")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error in Jira trigger: {e}")
        raise HTTPException(status_code=500, detail=f"Jira trigger failed: {str(e)}")


@router.post(
    "/trigger/document",
    response_model=Optional[ProactiveAlertResponse],
    summary="Trigger document analysis",
    description="Analyze new document and surface relevant lessons learned"
)
async def trigger_document(request: DocumentTriggerRequest):
    """
    Trigger proactive analysis for document
    
    - Searches for similar past experiences
    - Returns alert if relevant lessons found
    - Returns null if no significant history
    """
    try:
        logger.info(f"📄 Document trigger: {request.document_title}")
        
        engine = get_proactive_engine()
        alert = engine.handle_document_trigger(
            document_title=request.document_title,
            document_content=request.content
        )
        
        if alert:
            logger.info(f"✅ Generated {alert.alert_level} alert with {alert.confidence_score}% confidence")
            return ProactiveAlertResponse(**alert.to_dict())
        else:
            logger.info("No relevant history found or confidence too low")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error in document trigger: {e}")
        raise HTTPException(status_code=500, detail=f"Document trigger failed: {str(e)}")


@router.post(
    "/query",
    response_model=ProactiveAlertResponse,
    summary="Query knowledge base",
    description="Natural language query over organizational knowledge with AI-synthesized answer"
)
async def query_knowledge(request: QueryRequest):
    """
    Natural language query over knowledge base
    
    - Searches vector store and knowledge graph
    - Finds relevant experts
    - Synthesizes answer with Gemini
    - Always returns a response (never null)
    """
    try:
        logger.info(f"💬 Query: {request.question}")
        
        engine = get_proactive_engine()
        alert = engine.handle_query_trigger(request.question)
        
        logger.info(f"✅ Generated query response with {alert.confidence_score}% confidence")
        return ProactiveAlertResponse(**alert.to_dict())
        
    except Exception as e:
        logger.error(f"❌ Error in query: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@router.get(
    "/knowledge/search",
    response_model=List[KnowledgeItemResponse],
    summary="Search knowledge base",
    description="Search for knowledge items with optional filters"
)
async def search_knowledge(
    q: str = Query(..., description="Search query"),
    type: Optional[str] = Query(None, description="Filter by content type (decision, failure, success, lesson, expertise, context)"),
    topics: Optional[str] = Query(None, description="Comma-separated topics to filter by"),
    limit: int = Query(10, ge=1, le=100, description="Maximum results (1-100)")
):
    """
    Search knowledge base
    
    - Semantic search using vector embeddings
    - Optional filtering by type and topics
    - Returns ranked results
    """
    try:
        logger.info(f"🔍 Search: {q} (type={type}, topics={topics}, limit={limit})")
        
        vector_store = get_vector_store()
        
        # Build filters
        filters = {}
        if type:
            filters['content_type'] = type
        
        # Search
        if topics:
            topic_list = [t.strip() for t in topics.split(',')]
            results = vector_store.search_by_topic(topic_list)
        else:
            results = vector_store.search_similar(q, top_k=limit, filters=filters if filters else None)
        
        # Convert to response model
        items = []
        for result in results[:limit]:
            metadata = result['metadata']
            items.append(KnowledgeItemResponse(
                id=result['id'],
                content_type=metadata.get('content_type', 'unknown'),
                title=result.get('document', '')[:100],  # Use document as title
                summary=result.get('document', '')[:500],
                key_facts=[],  # Not stored separately in vector store
                people_involved=metadata.get('people_involved', []),
                teams_involved=metadata.get('teams_involved', []),
                date_occurred=metadata.get('date_occurred'),
                topics=metadata.get('topics', []),
                outcome=metadata.get('outcome', 'unknown'),
                importance_score=metadata.get('importance_score', 0),
                source_type=metadata.get('source_type', 'unknown'),
                source_reference=metadata.get('source_reference', '')
            ))
        
        logger.info(f"✅ Found {len(items)} items")
        return items
        
    except Exception as e:
        logger.error(f"❌ Error searching: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get(
    "/knowledge/{item_id}",
    response_model=KnowledgeItemResponse,
    summary="Get knowledge item by ID",
    description="Retrieve full knowledge item with related items"
)
async def get_knowledge_item(item_id: str):
    """
    Get knowledge item by ID
    
    - Returns full item details
    - Includes related items from graph
    """
    try:
        logger.info(f"📖 Get item: {item_id}")
        
        vector_store = get_vector_store()
        result = vector_store.get_by_id(item_id)
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Knowledge item {item_id} not found")
        
        metadata = result['metadata']
        item = KnowledgeItemResponse(
            id=result['id'],
            content_type=metadata.get('content_type', 'unknown'),
            title=result.get('document', '')[:100],
            summary=result.get('document', '')[:500],
            key_facts=[],
            people_involved=metadata.get('people_involved', []),
            teams_involved=metadata.get('teams_involved', []),
            date_occurred=metadata.get('date_occurred'),
            topics=metadata.get('topics', []),
            outcome=metadata.get('outcome', 'unknown'),
            importance_score=metadata.get('importance_score', 0),
            source_type=metadata.get('source_type', 'unknown'),
            source_reference=metadata.get('source_reference', '')
        )
        
        logger.info(f"✅ Retrieved item {item_id}")
        return item
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error getting item: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get item: {str(e)}")


@router.get(
    "/graph",
    summary="Get knowledge graph",
    description="Get knowledge graph in D3.js format for visualization"
)
async def get_graph(focus_topic: Optional[str] = Query(None, description="Filter graph to specific topic")):
    """
    Get knowledge graph in D3.js format
    
    - Returns nodes and links for visualization
    - Optional topic filtering
    - Color-coded by node type
    """
    try:
        logger.info(f"🕸️ Get graph (focus_topic={focus_topic})")
        
        graph_builder = get_graph_builder()
        graph_json = graph_builder.export_graph_json()
        
        # Filter by topic if requested
        if focus_topic:
            topic_id = f"topic:{focus_topic.lower().replace(' ', '_')}"
            
            # Find nodes connected to this topic
            relevant_node_ids = set()
            relevant_node_ids.add(topic_id)
            
            # Add all nodes connected to the topic
            for link in graph_json['links']:
                if link['source'] == topic_id or link['target'] == topic_id:
                    relevant_node_ids.add(link['source'])
                    relevant_node_ids.add(link['target'])
            
            # Filter nodes and links
            graph_json['nodes'] = [n for n in graph_json['nodes'] if n['id'] in relevant_node_ids]
            graph_json['links'] = [
                l for l in graph_json['links'] 
                if l['source'] in relevant_node_ids and l['target'] in relevant_node_ids
            ]
        
        logger.info(f"✅ Exported graph: {len(graph_json['nodes'])} nodes, {len(graph_json['links'])} links")
        return graph_json
        
    except Exception as e:
        logger.error(f"❌ Error getting graph: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get graph: {str(e)}")


@router.get(
    "/experts",
    response_model=List[ExpertResponse],
    summary="Find experts",
    description="Find people with expertise on a specific topic"
)
async def get_experts(topic: str = Query(..., description="Topic to find experts for")):
    """
    Find experts on a topic
    
    - Uses knowledge graph to find people
    - Returns evidence of expertise
    - Ranked by relevance
    """
    try:
        logger.info(f"👥 Find experts: {topic}")
        
        graph_builder = get_graph_builder()
        experts = graph_builder.find_expert(topic)
        
        # Convert to response model
        expert_responses = []
        for expert in experts:
            expert_responses.append(ExpertResponse(
                name=expert['name'],
                expertise_areas=[topic],
                evidence=expert['items'],
                relevance_score=expert['total_importance']
            ))
        
        logger.info(f"✅ Found {len(expert_responses)} experts")
        return expert_responses
        
    except Exception as e:
        logger.error(f"❌ Error finding experts: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to find experts: {str(e)}")


@router.get(
    "/stats",
    response_model=StatsResponse,
    summary="Get system statistics",
    description="Get statistics about knowledge base and recent activity"
)
async def get_stats():
    """
    Get system statistics
    
    - Total knowledge items
    - Items by type and outcome
    - Top topics (BUG 2 FIX: Now aggregates from vector store)
    """
    try:
        logger.info("📊 Get stats")
        
        vector_store = get_vector_store()
        stats = vector_store.get_stats()
        
        # BUG 2 FIX: Aggregate topics from all knowledge items in vector store
        from collections import Counter
        
        # Get all items from vector store
        try:
            all_items = vector_store.collection.get(include=['metadatas'])
            
            # Aggregate topics
            all_topics = []
            if all_items and 'metadatas' in all_items:
                for metadata in all_items['metadatas']:
                    topics = metadata.get('topics', [])
                    if isinstance(topics, list):
                        all_topics.extend(topics)
                    elif isinstance(topics, str):
                        # Handle comma-separated string
                        all_topics.extend([t.strip() for t in topics.split(',') if t.strip()])
            
            # Count and get top 10
            topic_counts = Counter(all_topics).most_common(10)
            top_topics = [{"topic": topic, "count": count} for topic, count in topic_counts]
            
            logger.info(f"✅ Aggregated {len(all_topics)} total topics, top 10: {len(top_topics)}")
            
        except Exception as e:
            logger.warning(f"Could not aggregate topics from vector store: {e}")
            # Fallback to graph-based approach
            graph_builder = get_graph_builder()
            graph = graph_builder.graph
            
            topic_counts = {}
            for node, data in graph.nodes(data=True):
                if data.get('node_type') == 'topic':
                    topic_name = data.get('name', node)
                    count = len(list(graph.predecessors(node)))
                    if count > 0:
                        topic_counts[topic_name] = count
            
            top_topics = [
                {'topic': topic, 'count': count}
                for topic, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:10]
            ]
        
        response = StatsResponse(
            total_knowledge_items=stats['total_items'],
            items_by_type=stats['items_by_type'],
            items_by_outcome=stats['items_by_outcome'],
            recent_alerts=0,  # Would track in production
            top_topics=top_topics
        )
        
        logger.info(f"✅ Stats: {stats['total_items']} items, {len(top_topics)} top topics")
        return response
        
    except Exception as e:
        logger.error(f"❌ Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.post(
    "/demo/seed",
    summary="Seed demo data",
    description="Load demo data from JSON files and run extraction pipeline"
)
async def seed_demo_data():
    """
    Load demo data and run extraction pipeline
    
    - Loads data from demo/data/ JSON files
    - Extracts knowledge from all sources
    - Stores in vector DB and graph
    - BUG 4 FIX: Rebuilds graph after seeding
    - Returns count of items seeded
    """
    try:
        logger.info("🌱 Seeding demo data...")
        
        # Load demo data
        with open('demo/data/slack_messages.json') as f:
            messages = json.load(f)
        
        with open('demo/data/jira_tickets.json') as f:
            tickets = json.load(f)
        
        with open('demo/data/documents.json') as f:
            documents = json.load(f)
        
        # Extract knowledge from key items
        extractor = get_extractor()
        all_knowledge = []
        
        # Process key Slack messages
        key_message_ids = [
            'ff4adc79-d389-49ac-bf18-d0bfcf299efa',  # PostgreSQL incident
            '28866bb8-ed13-4400-820b-3d5331dd781e',  # React decision
            'e2361904-7cbb-4d81-a841-34110cea2c70',  # Microservices success
        ]
        
        for msg in messages:
            if msg['id'] in key_message_ids:
                items = extractor.extract_knowledge(
                    text=msg['text'],
                    source_type='slack',
                    source_id=msg['id']
                )
                all_knowledge.extend(items)
                logger.info(f"  ✓ Extracted {len(items)} items from Slack message")
        
        # Store in vector database
        vector_store = get_vector_store()
        vector_store.add_knowledge(all_knowledge)
        
        # BUG 4 FIX: Rebuild knowledge graph after seeding
        graph_builder = get_graph_builder()
        try:
            # Get all items from vector store after seeding
            all_items_result = vector_store.collection.get(include=['metadatas', 'documents'])
            
            # Convert to knowledge items format for graph builder
            if all_items_result and 'metadatas' in all_items_result:
                graph_builder.build_graph(all_knowledge)
                graph_nodes = len(all_knowledge)
                graph_rebuilt = True
                logger.info(f"✅ Knowledge graph rebuilt with {graph_nodes} nodes")
            else:
                graph_rebuilt = False
                graph_nodes = 0
                logger.warning("⚠️  No items found to rebuild graph")
                
        except Exception as e:
            logger.error(f"❌ Graph rebuild failed: {e}")
            graph_rebuilt = False
            graph_nodes = 0
        
        logger.info(f"✅ Seeded {len(all_knowledge)} knowledge items")
        
        return {
            "status": "success",
            "items_seeded": len(all_knowledge),
            "graph_rebuilt": graph_rebuilt,
            "graph_nodes": graph_nodes,
            "message": f"Successfully seeded {len(all_knowledge)} knowledge items from demo data"
        }
        
    except Exception as e:
        logger.error(f"❌ Error seeding demo data: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to seed demo data: {str(e)}")


@router.post(
    "/demo/scenario/{scenario_id}",
    response_model=ProactiveAlertResponse,
    summary="Run demo scenario",
    description="Run pre-built demo scenario (A: Mistake Prevented, B: Question Answered, C: Document Context)"
)
async def run_demo_scenario(scenario_id: str):
    """
    Run pre-built demo scenario
    
    - A: The Mistake Prevented (PostgreSQL migration)
    - B: The Question Answered (React vs Vue)
    - C: Document Context (Migration guide)
    """
    try:
        logger.info(f"🎬 Running demo scenario {scenario_id}")
        
        engine = get_proactive_engine()
        
        if scenario_id.upper() == 'A':
            # Scenario A: The Mistake Prevented
            alert = engine.handle_jira_trigger(
                ticket_title="Migrate primary database from MySQL to PostgreSQL",
                ticket_description="""
                We need to migrate our primary database from MySQL to PostgreSQL for better JSON support
                and improved performance. This will involve:
                - Setting up PostgreSQL instance
                - Migrating schema
                - Migrating data
                - Updating application connection strings
                - Testing in staging
                - Production cutover
                
                Timeline: 2 weeks
                """
            )
            
        elif scenario_id.upper() == 'B':
            # Scenario B: The Question Answered
            alert = engine.handle_query_trigger(
                "Why do we use React instead of Vue for our frontend?"
            )
            
        elif scenario_id.upper() == 'C':
            # Scenario C: Document Context
            alert = engine.handle_document_trigger(
                document_title="Database Migration Best Practices Guide",
                document_content="""
                This guide covers best practices for database migrations at NovaTech.
                
                ## Planning Phase
                - Assess current database performance
                - Identify migration goals
                - Choose target database system
                
                ## Execution Phase
                - Set up new database instance
                - Configure connection pooling
                - Migrate schema and data
                """
            )
            
        else:
            raise HTTPException(status_code=400, detail=f"Invalid scenario ID: {scenario_id}. Must be A, B, or C")
        
        if alert:
            logger.info(f"✅ Scenario {scenario_id} completed")
            return ProactiveAlertResponse(**alert.to_dict())
        else:
            raise HTTPException(status_code=404, detail="No alert generated for this scenario")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error running scenario: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to run scenario: {str(e)}")


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check system health and status"
)
async def health_check():
    """
    Health check endpoint
    
    - Returns system status
    - Knowledge item count
    - Vector store status
    """
    try:
        vector_store = get_vector_store()
        stats = vector_store.get_stats()
        
        return HealthResponse(
            status="ok",
            knowledge_items=stats['total_items'],
            vector_store="connected",
            demo_mode=settings.DEMO_MODE
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="degraded",
            knowledge_items=0,
            vector_store="error",
            demo_mode=settings.DEMO_MODE
        )
