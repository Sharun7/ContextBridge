"""
API Routes
All FastAPI endpoints for ContextBridge
"""

import json
import logging
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException, Query

from api.models import (
    DocumentTriggerRequest,
    ExpertResponse,
    HealthResponse,
    IngestRequest,
    IngestResponse,
    JiraTriggerRequest,
    KnowledgeItemResponse,
    ProactiveAlertResponse,
    QueryRequest,
    StatsResponse,
)
from config import settings
from intelligence.proactive_engine import ProactiveEngine
from processing.graph_builder import GraphBuilder
from processing.knowledge_extractor import KnowledgeExtractor, KnowledgeItem
from processing.vector_store import VectorStore

logger = logging.getLogger(__name__)

router = APIRouter()
DEMO_DATA_DIR = Path(__file__).resolve().parents[1] / "demo" / "data"

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
            collection_name=settings.CHROMA_COLLECTION_NAME,
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
            gemini_api_key=settings.GEMINI_API_KEY,
        )
    return _proactive_engine


def _as_list(value: Any) -> List[str]:
    """Normalize stored metadata values to a clean list of strings."""
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return []


def _split_document(document: str) -> tuple[str, str, List[str]]:
    """Recover title, summary, and key facts from the stored embedding text."""
    blocks = [block.strip() for block in document.split("\n\n") if block.strip()]

    title = blocks[0] if blocks else "Untitled knowledge item"
    summary = blocks[1] if len(blocks) > 1 else title

    key_facts: List[str] = []
    if len(blocks) > 2:
        facts_blob = "\n".join(blocks[2:])
        key_facts = [
            line.lstrip("- ").strip()
            for line in facts_blob.splitlines()
            if line.strip()
        ]

    return title[:100], summary[:500], key_facts[:10]


def _record_to_knowledge_item(record: Dict[str, Any]) -> KnowledgeItem:
    """Convert a vector store record back into a KnowledgeItem for graph rebuilds."""
    metadata = record.get("metadata", {})
    title, summary, key_facts = _split_document(record.get("document", ""))

    return KnowledgeItem(
        {
            "id": record.get("id"),
            "content_type": metadata.get("content_type", "unknown"),
            "title": title,
            "summary": summary,
            "key_facts": key_facts,
            "people_involved": _as_list(metadata.get("people_involved")),
            "teams_involved": _as_list(metadata.get("teams_involved")),
            "date_occurred": metadata.get("date_occurred"),
            "topics": _as_list(metadata.get("topics")),
            "outcome": metadata.get("outcome", "unknown"),
            "importance_score": metadata.get("importance_score", 0),
            "source_type": metadata.get("source_type", "unknown"),
            "source_reference": metadata.get("source_reference", ""),
        }
    )


def _record_to_response(record: Dict[str, Any]) -> KnowledgeItemResponse:
    """Convert a vector store record into the frontend-facing API response."""
    metadata = record.get("metadata", {})
    title, summary, key_facts = _split_document(record.get("document", ""))

    return KnowledgeItemResponse(
        id=record["id"],
        content_type=metadata.get("content_type", "unknown"),
        title=title,
        summary=summary,
        key_facts=key_facts,
        people_involved=_as_list(metadata.get("people_involved")),
        teams_involved=_as_list(metadata.get("teams_involved")),
        date_occurred=metadata.get("date_occurred"),
        topics=_as_list(metadata.get("topics")),
        outcome=metadata.get("outcome", "unknown"),
        importance_score=metadata.get("importance_score", 0),
        source_type=metadata.get("source_type", "unknown"),
        source_reference=metadata.get("source_reference", ""),
    )


def _filter_records(
    records: List[Dict[str, Any]],
    content_type: Optional[str] = None,
    outcome: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Apply lightweight metadata filters to vector store records."""
    filtered: List[Dict[str, Any]] = []

    for record in records:
        metadata = record.get("metadata", {})

        if content_type and metadata.get("content_type") != content_type:
            continue
        if outcome and metadata.get("outcome") != outcome:
            continue

        filtered.append(record)

    return filtered


def _ensure_graph_built(force_rebuild: bool = False) -> GraphBuilder:
    """Rebuild the in-memory graph from persisted vector data when needed."""
    graph_builder = get_graph_builder()

    if not force_rebuild and graph_builder.graph.number_of_nodes() > 0:
        return graph_builder

    vector_store = get_vector_store()
    records = vector_store.get_all()

    if not records:
        graph_builder.graph.clear()
        graph_builder.knowledge_items.clear()
        return graph_builder

    graph_items = [_record_to_knowledge_item(record) for record in records]
    graph_builder.build_graph(graph_items)
    return graph_builder


@router.post(
    "/ingest",
    response_model=IngestResponse,
    summary="Ingest enterprise data",
    description="Extract knowledge from enterprise sources (Slack, Jira, documents) and store in vector DB and knowledge graph",
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
        logger.info("📥 Ingesting %s data", request.source_type)

        items_to_process = []

        if request.fetch_from_source:
            logger.info("🔄 Fetching from real %s API...", request.source_type)

            if request.source_type == "slack":
                from ingestion.slack_connector import SlackConnector

                connector = SlackConnector(
                    demo_mode=settings.DEMO_MODE,
                    slack_token=settings.SLACK_BOT_TOKEN,
                )
                items_to_process = connector.fetch_messages(
                    channel=request.channel,
                    limit=request.limit,
                )

            elif request.source_type == "jira":
                from ingestion.jira_connector import JiraConnector

                connector = JiraConnector(
                    demo_mode=settings.DEMO_MODE,
                    jira_url=settings.JIRA_URL,
                    jira_email=settings.JIRA_EMAIL,
                    jira_api_token=settings.JIRA_API_TOKEN,
                )
                items_to_process = connector.fetch_tickets(
                    project=request.project,
                    limit=request.limit,
                )

            elif request.source_type == "google_drive":
                from ingestion.drive_connector import DriveConnector

                connector = DriveConnector(
                    demo_mode=settings.DEMO_MODE,
                    credentials_path=settings.GOOGLE_DRIVE_CREDENTIALS_PATH,
                    service_account_path=settings.GOOGLE_DRIVE_SERVICE_ACCOUNT_PATH,
                )
                items_to_process = connector.fetch_documents(
                    folder=request.folder,
                    limit=request.limit,
                )

            elif request.source_type == "gmail":
                from ingestion.email_connector import EmailConnector

                connector = EmailConnector(
                    demo_mode=settings.DEMO_MODE,
                    credentials_path=settings.GMAIL_CREDENTIALS_PATH,
                    service_account_path=settings.GMAIL_SERVICE_ACCOUNT_PATH,
                )
                items_to_process = connector.fetch_emails(
                    query=request.query,
                    limit=request.limit,
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported source type for fetching: {request.source_type}",
                )

            logger.info(
                "✅ Fetched %s items from %s",
                len(items_to_process),
                request.source_type,
            )

        else:
            if not request.content or not request.source_id:
                raise HTTPException(
                    status_code=400,
                    detail="Either provide content+source_id OR set fetch_from_source=true",
                )

            items_to_process = [
                {
                    "content": request.content,
                    "source_id": request.source_id,
                    "source_type": request.source_type,
                }
            ]

        if not items_to_process:
            return IngestResponse(
                items_extracted=0,
                knowledge_ids=[],
                message="No items to process",
            )

        extractor = get_extractor()
        all_knowledge_items = []

        for item in items_to_process:
            if request.source_type == "slack":
                content = (
                    f"Channel: {item.get('channel', '')}\n"
                    f"Author: {item.get('author', '')}\n"
                    f"Message: {item.get('content', '')}"
                )
            elif request.source_type == "jira":
                content = (
                    f"Ticket: {item.get('title', '')}\n"
                    f"Description: {item.get('description', '')}\n"
                    f"Status: {item.get('status', '')}"
                )
            elif request.source_type == "google_drive":
                content = (
                    f"Document: {item.get('title', '')}\n"
                    f"Content: {item.get('content', '')}"
                )
            elif request.source_type == "gmail":
                content = (
                    f"Subject: {item.get('subject', '')}\n"
                    f"From: {item.get('from', '')}\n"
                    f"Body: {item.get('body', '')}"
                )
            else:
                content = item.get("content", "")

            knowledge_items = extractor.extract_knowledge(
                text=content,
                source_type=request.source_type,
                source_id=item.get("source_id", item.get("id", "unknown")),
            )
            all_knowledge_items.extend(knowledge_items)

        if not all_knowledge_items:
            return IngestResponse(
                items_extracted=0,
                knowledge_ids=[],
                message="No knowledge items extracted from content",
            )

        vector_store = get_vector_store()
        vector_store.add_knowledge(all_knowledge_items)
        _ensure_graph_built(force_rebuild=True)

        knowledge_ids = [item.id for item in all_knowledge_items]

        logger.info(
            "✅ Extracted and stored %s knowledge items",
            len(all_knowledge_items),
        )

        return IngestResponse(
            items_extracted=len(all_knowledge_items),
            knowledge_ids=knowledge_ids,
            message=(
                f"Successfully extracted {len(all_knowledge_items)} knowledge items "
                f"from {len(items_to_process)} source items"
            ),
        )

    except Exception as e:
        logger.error("❌ Error ingesting data: %s", e)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@router.post(
    "/trigger/jira",
    response_model=Optional[ProactiveAlertResponse],
    summary="Trigger Jira analysis",
    description="Analyze new Jira ticket and surface relevant organizational history",
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
        logger.info("🎫 Jira trigger: %s", request.ticket_title)

        alert = get_proactive_engine().handle_jira_trigger(
            ticket_title=request.ticket_title,
            ticket_description=request.ticket_description,
        )

        if alert:
            logger.info(
                "✅ Generated %s alert with %s%% confidence",
                alert.alert_level,
                alert.confidence_score,
            )
            return ProactiveAlertResponse(**alert.to_dict())

        logger.info("No relevant history found or confidence too low")
        return None

    except Exception as e:
        logger.error("❌ Error in Jira trigger: %s", e)
        raise HTTPException(status_code=500, detail=f"Jira trigger failed: {str(e)}")


@router.post(
    "/trigger/document",
    response_model=Optional[ProactiveAlertResponse],
    summary="Trigger document analysis",
    description="Analyze new document and surface relevant lessons learned",
)
async def trigger_document(request: DocumentTriggerRequest):
    """
    Trigger proactive analysis for document

    - Searches for similar past experiences
    - Returns alert if relevant lessons found
    - Returns null if no significant history
    """
    try:
        logger.info("📄 Document trigger: %s", request.document_title)

        alert = get_proactive_engine().handle_document_trigger(
            document_title=request.document_title,
            document_content=request.content,
        )

        if alert:
            logger.info(
                "✅ Generated %s alert with %s%% confidence",
                alert.alert_level,
                alert.confidence_score,
            )
            return ProactiveAlertResponse(**alert.to_dict())

        logger.info("No relevant history found or confidence too low")
        return None

    except Exception as e:
        logger.error("❌ Error in document trigger: %s", e)
        raise HTTPException(
            status_code=500,
            detail=f"Document trigger failed: {str(e)}",
        )


@router.post(
    "/query",
    response_model=ProactiveAlertResponse,
    summary="Query knowledge base",
    description="Natural language query over organizational knowledge with AI-synthesized answer",
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
        logger.info("💬 Query: %s", request.question)

        alert = get_proactive_engine().handle_query_trigger(request.question)

        logger.info(
            "✅ Generated query response with %s%% confidence",
            alert.confidence_score,
        )
        return ProactiveAlertResponse(**alert.to_dict())

    except Exception as e:
        logger.error("❌ Error in query: %s", e)
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@router.get(
    "/knowledge/search",
    response_model=List[KnowledgeItemResponse],
    summary="Search knowledge base",
    description="Search for knowledge items with optional filters",
)
async def search_knowledge(
    q: str = Query("", description="Search query"),
    type: Optional[str] = Query(
        None,
        description="Filter by content type (decision, failure, success, lesson, expertise, context)",
    ),
    topics: Optional[str] = Query(
        None,
        description="Comma-separated topics to filter by",
    ),
    outcome: Optional[str] = Query(
        None,
        description="Filter by outcome (success, failure, ongoing, unknown)",
    ),
    limit: int = Query(10, ge=1, le=100, description="Maximum results (1-100)"),
):
    """
    Search knowledge base

    - Semantic search using vector embeddings
    - Optional filtering by type, outcome, and topics
    - Empty query returns recent stored items for page load
    """
    try:
        logger.info(
            "🔍 Search: q=%s (type=%s, topics=%s, outcome=%s, limit=%s)",
            q,
            type,
            topics,
            outcome,
            limit,
        )

        vector_store = get_vector_store()

        if topics:
            topic_list = [topic.strip() for topic in topics.split(",") if topic.strip()]
            results = vector_store.search_by_topic(topic_list)
        elif q.strip():
            filters = {"content_type": type} if type else None
            results = vector_store.search_similar(
                q,
                top_k=limit,
                filters=filters,
            )
        else:
            results = vector_store.get_all()

        results = _filter_records(results, content_type=type, outcome=outcome)
        items = [_record_to_response(result) for result in results[:limit]]

        logger.info("✅ Found %s items", len(items))
        return items

    except Exception as e:
        logger.error("❌ Error searching: %s", e)
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get(
    "/knowledge/{item_id}",
    response_model=KnowledgeItemResponse,
    summary="Get knowledge item by ID",
    description="Retrieve full knowledge item with related items",
)
async def get_knowledge_item(item_id: str):
    """
    Get knowledge item by ID

    - Returns full item details
    - Includes related items from graph
    """
    try:
        logger.info("📖 Get item: %s", item_id)

        result = get_vector_store().get_by_id(item_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Knowledge item {item_id} not found",
            )

        item = _record_to_response(result)
        logger.info("✅ Retrieved item %s", item_id)
        return item

    except HTTPException:
        raise
    except Exception as e:
        logger.error("❌ Error getting item: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to get item: {str(e)}")


@router.get(
    "/graph",
    summary="Get knowledge graph",
    description="Get knowledge graph in D3.js format for visualization",
)
async def get_graph(
    focus_topic: Optional[str] = Query(
        None,
        description="Filter graph to specific topic",
    )
):
    """
    Get knowledge graph in D3.js format

    - Returns nodes and links for visualization
    - Optional topic filtering
    - Rehydrates the in-memory graph from Chroma when needed
    """
    try:
        logger.info("🕸️ Get graph (focus_topic=%s)", focus_topic)

        graph_json = _ensure_graph_built().export_graph_json()

        if focus_topic:
            topic_id = f"topic:{focus_topic.lower().replace(' ', '_')}"
            relevant_node_ids = {topic_id}

            for link in graph_json["links"]:
                if link["source"] == topic_id or link["target"] == topic_id:
                    relevant_node_ids.add(link["source"])
                    relevant_node_ids.add(link["target"])

            graph_json["nodes"] = [
                node for node in graph_json["nodes"] if node["id"] in relevant_node_ids
            ]
            graph_json["links"] = [
                link
                for link in graph_json["links"]
                if link["source"] in relevant_node_ids
                and link["target"] in relevant_node_ids
            ]

        logger.info(
            "✅ Exported graph: %s nodes, %s links",
            len(graph_json["nodes"]),
            len(graph_json["links"]),
        )
        return graph_json

    except Exception as e:
        logger.error("❌ Error getting graph: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to get graph: {str(e)}")


@router.get(
    "/experts",
    response_model=List[ExpertResponse],
    summary="Find experts",
    description="Find people with expertise on a specific topic",
)
async def get_experts(topic: str = Query(..., description="Topic to find experts for")):
    """
    Find experts on a topic

    - Uses knowledge graph to find people
    - Returns evidence of expertise
    - Ranked by relevance
    """
    try:
        logger.info("👥 Find experts: %s", topic)

        experts = _ensure_graph_built().find_expert(topic)
        expert_responses = [
            ExpertResponse(
                name=expert["name"],
                expertise_areas=[topic],
                evidence=expert["items"],
                relevance_score=expert["total_importance"],
            )
            for expert in experts
        ]

        logger.info("✅ Found %s experts", len(expert_responses))
        return expert_responses

    except Exception as e:
        logger.error("❌ Error finding experts: %s", e)
        raise HTTPException(status_code=500, detail=f"Failed to find experts: {str(e)}")


@router.get(
    "/stats",
    response_model=StatsResponse,
    summary="Get system statistics",
    description="Get statistics about knowledge base and recent activity",
)
async def get_stats():
    """
    Get system statistics

    - Total knowledge items
    - Items by type and outcome
    - Top topics aggregated from persisted vector metadata
    """
    try:
        logger.info("📊 Get stats")

        vector_store = get_vector_store()
        stats = vector_store.get_stats()
        all_items = vector_store.get_all()

        topic_counts = Counter()
        for item in all_items:
            topic_counts.update(_as_list(item.get("metadata", {}).get("topics")))

        top_topics = [
            {"topic": topic, "count": count}
            for topic, count in topic_counts.most_common(10)
        ]

        response = StatsResponse(
            total_knowledge_items=stats["total_items"],
            items_by_type=stats["items_by_type"],
            items_by_outcome=stats["items_by_outcome"],
            recent_alerts=0,
            top_topics=top_topics,
        )

        logger.info(
            "✅ Stats: %s items, %s top topics",
            stats["total_items"],
            len(top_topics),
        )
        return response

    except Exception as e:
        logger.error("❌ Error getting stats: %s", e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get stats: {str(e)}",
        )


@router.post(
    "/demo/seed",
    summary="Seed demo data",
    description="Load demo data from JSON files and run extraction pipeline",
)
async def seed_demo_data():
    """
    Load demo data and run extraction pipeline

    - Loads data from demo/data JSON files
    - Extracts knowledge from the demo stories
    - Stores in vector DB and rebuilds the graph from persisted state
    """
    try:
        logger.info("🌱 Seeding demo data...")

        with open(DEMO_DATA_DIR / "slack_messages.json", encoding="utf-8") as file:
            messages = json.load(file)

        extractor = get_extractor()
        all_knowledge = []

        key_message_ids = [
            "ff4adc79-d389-49ac-bf18-d0bfcf299efa",
            "28866bb8-ed13-4400-820b-3d5331dd781e",
            "e2361904-7cbb-4d81-a841-34110cea2c70",
        ]

        for msg in messages:
            if msg["id"] in key_message_ids:
                items = extractor.extract_knowledge(
                    text=msg["text"],
                    source_type="slack",
                    source_id=msg["id"],
                )
                all_knowledge.extend(items)
                logger.info("  ✓ Extracted %s items from Slack message", len(items))

        vector_store = get_vector_store()
        vector_store.add_knowledge(all_knowledge)

        graph_builder = _ensure_graph_built(force_rebuild=True)
        graph_nodes = graph_builder.graph.number_of_nodes()
        graph_rebuilt = graph_nodes > 0

        logger.info("✅ Seeded %s knowledge items", len(all_knowledge))

        return {
            "status": "success",
            "items_seeded": len(all_knowledge),
            "graph_rebuilt": graph_rebuilt,
            "graph_nodes": graph_nodes,
            "message": (
                f"Successfully seeded {len(all_knowledge)} knowledge items from demo data"
            ),
        }

    except Exception as e:
        logger.error("❌ Error seeding demo data: %s", e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to seed demo data: {str(e)}",
        )


@router.post(
    "/demo/scenario/{scenario_id}",
    response_model=ProactiveAlertResponse,
    summary="Run demo scenario",
    description="Run pre-built demo scenario (A: Mistake Prevented, B: Question Answered, C: Document Context)",
)
async def run_demo_scenario(scenario_id: str):
    """
    Run pre-built demo scenario

    - A: The Mistake Prevented (PostgreSQL migration)
    - B: The Question Answered (React vs Vue)
    - C: Document Context (Migration guide)
    """
    try:
        logger.info("🎬 Running demo scenario %s", scenario_id)

        engine = get_proactive_engine()

        if scenario_id.upper() == "A":
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
                """,
            )

        elif scenario_id.upper() == "B":
            alert = engine.handle_query_trigger(
                "Why do we use React instead of Vue for our frontend?"
            )

        elif scenario_id.upper() == "C":
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
                """,
            )

        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid scenario ID: {scenario_id}. Must be A, B, or C",
            )

        if alert:
            logger.info("✅ Scenario %s completed", scenario_id)
            return ProactiveAlertResponse(**alert.to_dict())

        raise HTTPException(status_code=404, detail="No alert generated for this scenario")

    except HTTPException:
        raise
    except Exception as e:
        logger.error("❌ Error running scenario: %s", e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to run scenario: {str(e)}",
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check system health and status",
)
async def health_check():
    """
    Health check endpoint

    - Returns system status
    - Knowledge item count
    - Vector store status
    """
    try:
        stats = get_vector_store().get_stats()

        return HealthResponse(
            status="ok",
            knowledge_items=stats["total_items"],
            vector_store="connected",
            demo_mode=settings.DEMO_MODE,
        )
    except Exception as e:
        logger.error("Health check failed: %s", e)
        return HealthResponse(
            status="degraded",
            knowledge_items=0,
            vector_store="error",
            demo_mode=settings.DEMO_MODE,
        )
