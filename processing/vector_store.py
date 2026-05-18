"""
Lightweight persisted knowledge store.

This replaces the original ChromaDB dependency with a JSON-backed store so the
project can run locally without native vector database build steps.
"""

import json
import logging
import math
import re
from pathlib import Path
from typing import Dict, List, Optional

from processing.knowledge_extractor import KnowledgeItem

logger = logging.getLogger(__name__)

TOKEN_PATTERN = re.compile(r"[a-z0-9][a-z0-9_\-+#.]{1,}")


class VectorStore:
    """Persist and search knowledge items without external vector DB dependencies."""

    def __init__(self, persist_dir: str, collection_name: str):
        self.persist_dir = Path(persist_dir)
        self.collection_name = collection_name
        self.store_path = self.persist_dir / f"{collection_name}.json"
        self.records: List[Dict] = []
        self.collection = self
        logger.info("VectorStore initialized: %s", collection_name)

    def initialize_store(self):
        """Load persisted records if they exist."""
        self.persist_dir.mkdir(parents=True, exist_ok=True)

        if self.store_path.exists():
            try:
                with self.store_path.open("r", encoding="utf-8") as file:
                    payload = json.load(file)
                self.records = payload.get("records", [])
            except Exception as exc:
                logger.warning("Failed to load persisted knowledge store: %s", exc)
                self.records = []

        logger.info("✅ Knowledge store initialized")
        logger.info("   Persist path: %s", self.store_path)
        logger.info("   Current item count: %s", len(self.records))

    def add_knowledge(self, items: List[KnowledgeItem]) -> int:
        """Upsert knowledge items into the persisted store."""
        if not items:
            logger.warning("No items to add to vector store")
            return 0

        existing = {record["id"]: record for record in self.records}

        for item in items:
            existing[item.id] = self._record_from_item(item)

        self.records = list(existing.values())
        self._save()
        logger.info("✅ Added %s knowledge items to vector store", len(items))
        return len(items)

    def search_similar(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict] = None,
    ) -> List[Dict]:
        """Search using lightweight lexical and metadata scoring."""
        filters = filters or {}
        query = (query or "").strip()
        query_tokens = self._tokenize(query)

        scored_records = []
        for record in self.records:
            metadata = record.get("metadata", {})
            if any(metadata.get(key) != value for key, value in filters.items()):
                continue

            score = self._score_record(record, query, query_tokens)
            if query and score <= 0:
                continue

            scored_records.append((score, record))

        scored_records.sort(
            key=lambda item: (
                -item[0],
                -item[1]["metadata"].get("importance_score", 0),
                item[1]["metadata"].get("date_occurred") or "",
            )
        )

        if not query:
            scored_records = [
                (0, record)
                for record in sorted(
                    [record for _, record in scored_records] if scored_records else self.records,
                    key=lambda record: (
                        -record["metadata"].get("importance_score", 0),
                        record["metadata"].get("date_occurred") or "",
                    ),
                )
            ]

        results = []
        for score, record in scored_records[:top_k]:
            result = self._clone_record(record)
            result["distance"] = self._distance_from_score(score)
            results.append(result)

        logger.info("✓ Found %s similar items for query '%s'", len(results), query[:50])
        return results

    def search_by_topic(self, topics: List[str]) -> List[Dict]:
        """Return records matching any of the requested topics."""
        normalized_topics = {topic.strip().lower() for topic in topics if topic.strip()}
        matches = []

        for record in self.records:
            item_topics = {
                topic.lower() for topic in record.get("metadata", {}).get("topics", [])
            }
            if normalized_topics & item_topics:
                matches.append(self._clone_record(record))

        matches.sort(
            key=lambda record: (
                -record["metadata"].get("importance_score", 0),
                record["metadata"].get("date_occurred") or "",
            )
        )

        logger.info("✓ Found %s items for topics: %s", len(matches), topics)
        return matches

    def get_by_id(self, item_id: str) -> Optional[Dict]:
        """Return one record by id."""
        for record in self.records:
            if record["id"] == item_id:
                return self._clone_record(record)
        return None

    def get_stats(self) -> Dict:
        """Aggregate basic knowledge store statistics."""
        items_by_type: Dict[str, int] = {}
        items_by_outcome: Dict[str, int] = {}

        for record in self.records:
            metadata = record.get("metadata", {})
            content_type = metadata.get("content_type", "unknown")
            outcome = metadata.get("outcome", "unknown")
            items_by_type[content_type] = items_by_type.get(content_type, 0) + 1
            items_by_outcome[outcome] = items_by_outcome.get(outcome, 0) + 1

        return {
            "total_items": len(self.records),
            "items_by_type": items_by_type,
            "items_by_outcome": items_by_outcome,
        }

    def get_all(self) -> List[Dict]:
        """Return all records."""
        return [self._clone_record(record) for record in self.records]

    def get(self, include: Optional[List[str]] = None) -> Dict:
        """Compatibility helper for previous collection-style access."""
        include = include or ["documents", "metadatas"]
        payload: Dict[str, List] = {"ids": [record["id"] for record in self.records]}

        if "documents" in include:
            payload["documents"] = [record["document"] for record in self.records]
        if "metadatas" in include:
            payload["metadatas"] = [self._clone_metadata(record["metadata"]) for record in self.records]

        return payload

    def count(self) -> int:
        """Compatibility helper for collection count."""
        return len(self.records)

    def _record_from_item(self, item: KnowledgeItem) -> Dict:
        document = f"{item.title}\n\n{item.summary}\n\n" + "\n".join(item.key_facts)
        metadata = {
            "content_type": item.content_type or "unknown",
            "outcome": item.outcome or "unknown",
            "importance_score": item.importance_score,
            "source_type": item.source_type or "unknown",
            "source_reference": item.source_reference or "",
            "date_occurred": item.date_occurred or "unknown",
            "topics": list(item.topics or []),
            "people_involved": list(item.people_involved or []),
            "teams_involved": list(item.teams_involved or []),
        }

        searchable_text = " ".join(
            [
                item.title or "",
                item.summary or "",
                " ".join(item.key_facts or []),
                " ".join(item.topics or []),
                " ".join(item.people_involved or []),
                " ".join(item.teams_involved or []),
                item.raw_excerpt or "",
            ]
        )

        return {
            "id": item.id,
            "document": document.strip(),
            "metadata": metadata,
            "search_tokens": sorted(self._tokenize(searchable_text)),
        }

    def _score_record(self, record: Dict, query: str, query_tokens: set[str]) -> float:
        if not query:
            return 0

        metadata = record.get("metadata", {})
        record_tokens = set(record.get("search_tokens", []))
        overlap = query_tokens & record_tokens

        score = float(len(overlap) * 4)

        topic_tokens = {topic.lower() for topic in metadata.get("topics", [])}
        topic_overlap = query_tokens & topic_tokens
        score += float(len(topic_overlap) * 7)

        content_type = metadata.get("content_type", "")
        if content_type and content_type.lower() in query.lower():
            score += 3.5

        document = record.get("document", "").lower()
        if query.lower() in document:
            score += 8

        if any(topic in query.lower() for topic in topic_tokens):
            score += 5

        score += metadata.get("importance_score", 0) * 0.35
        return score

    def _distance_from_score(self, score: float) -> float:
        if score <= 0:
            return 2.0
        return round(min(2.0, 1.0 / math.sqrt(score + 1)), 4)

    def _save(self):
        payload = {"records": self.records}
        with self.store_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)

    def _clone_record(self, record: Dict) -> Dict:
        return {
            "id": record["id"],
            "document": record["document"],
            "metadata": self._clone_metadata(record["metadata"]),
        }

    def _clone_metadata(self, metadata: Dict) -> Dict:
        return {
            **metadata,
            "topics": list(metadata.get("topics", [])),
            "people_involved": list(metadata.get("people_involved", [])),
            "teams_involved": list(metadata.get("teams_involved", [])),
        }

    def _tokenize(self, text: str) -> set[str]:
        return {
            token.lower()
            for token in TOKEN_PATTERN.findall(text.lower())
            if len(token) > 2
        }
