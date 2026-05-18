"""
Vector Store using ChromaDB
Stores and searches knowledge items using semantic embeddings
"""

import logging
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings as ChromaSettings
from processing.knowledge_extractor import KnowledgeItem

logger = logging.getLogger(__name__)


class VectorStore:
    """ChromaDB-based vector store for knowledge items"""
    
    def __init__(self, persist_dir: str, collection_name: str):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        logger.info(f"VectorStore initialized: {collection_name}")
    
    def initialize_store(self):
        """Initialize ChromaDB collection"""
        try:
            # Create persistent ChromaDB client
            self.client = chromadb.PersistentClient(
                path=self.persist_dir,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True
                )
            )
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "ContextBridge knowledge items"}
            )
            
            logger.info(f"✅ ChromaDB collection '{self.collection_name}' initialized")
            logger.info(f"   Persist directory: {self.persist_dir}")
            logger.info(f"   Current item count: {self.collection.count()}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize ChromaDB: {e}")
            raise
    
    def add_knowledge(self, items: List[KnowledgeItem]) -> int:
        """
        Add knowledge items to vector store
        
        Args:
            items: List of KnowledgeItem objects
            
        Returns:
            Number of items added
        """
        if not self.collection:
            raise RuntimeError("Vector store not initialized. Call initialize_store() first.")
        
        if not items:
            logger.warning("No items to add to vector store")
            return 0
        
        try:
            # Prepare data for ChromaDB
            ids = []
            documents = []
            metadatas = []
            
            for item in items:
                # Create embedding text: title + summary + key facts
                embedding_text = f"{item.title}\n\n{item.summary}\n\n"
                embedding_text += "\n".join(item.key_facts)
                
                # Prepare metadata (ChromaDB requires simple types)
                metadata = {
                    "content_type": item.content_type or "unknown",
                    "outcome": item.outcome or "unknown",
                    "importance_score": item.importance_score,
                    "source_type": item.source_type or "unknown",
                    "source_reference": item.source_reference or "",
                    "date_occurred": item.date_occurred or "unknown",
                    # Store lists as comma-separated strings
                    "topics": ",".join(item.topics) if item.topics else "",
                    "people_involved": ",".join(item.people_involved) if item.people_involved else "",
                    "teams_involved": ",".join(item.teams_involved) if item.teams_involved else "",
                }
                
                ids.append(item.id)
                documents.append(embedding_text)
                metadatas.append(metadata)
            
            # Add to ChromaDB (it will generate embeddings automatically)
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )
            
            logger.info(f"✅ Added {len(items)} knowledge items to vector store")
            return len(items)
            
        except Exception as e:
            logger.error(f"❌ Error adding knowledge items: {e}")
            raise
    
    def search_similar(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar knowledge items
        
        Args:
            query: Search query text
            top_k: Number of results to return
            filters: Optional metadata filters (e.g., {"content_type": "failure"})
            
        Returns:
            List of matching knowledge items as dictionaries
        """
        if not self.collection:
            raise RuntimeError("Vector store not initialized. Call initialize_store() first.")
        
        try:
            # Build where clause for filtering
            where_clause = None
            if filters:
                where_clause = {}
                for key, value in filters.items():
                    where_clause[key] = value
            
            # Query ChromaDB
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=where_clause
            )
            
            # Parse results
            items = []
            if results and results['ids'] and len(results['ids']) > 0:
                for i in range(len(results['ids'][0])):
                    item_data = {
                        'id': results['ids'][0][i],
                        'document': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else None
                    }
                    
                    # Parse comma-separated lists back to arrays
                    if 'topics' in item_data['metadata']:
                        topics_str = item_data['metadata']['topics']
                        item_data['metadata']['topics'] = topics_str.split(',') if topics_str else []
                    
                    if 'people_involved' in item_data['metadata']:
                        people_str = item_data['metadata']['people_involved']
                        item_data['metadata']['people_involved'] = people_str.split(',') if people_str else []
                    
                    if 'teams_involved' in item_data['metadata']:
                        teams_str = item_data['metadata']['teams_involved']
                        item_data['metadata']['teams_involved'] = teams_str.split(',') if teams_str else []
                    
                    items.append(item_data)
            
            logger.info(f"✓ Found {len(items)} similar items for query: '{query[:50]}...'")
            return items
            
        except Exception as e:
            logger.error(f"❌ Error searching vector store: {e}")
            return []
    
    def search_by_topic(self, topics: List[str]) -> List[Dict]:
        """
        Search by specific topics
        
        Args:
            topics: List of topic strings
            
        Returns:
            List of matching knowledge items as dictionaries
        """
        if not self.collection:
            raise RuntimeError("Vector store not initialized. Call initialize_store() first.")
        
        try:
            # Get all items and filter by topics
            # ChromaDB doesn't support "contains" queries on strings, so we fetch and filter
            all_results = self.collection.get()
            
            matching_items = []
            if all_results and all_results['ids']:
                for i in range(len(all_results['ids'])):
                    metadata = all_results['metadatas'][i]
                    item_topics = metadata.get('topics', '').split(',') if metadata.get('topics') else []
                    
                    # Check if any requested topic is in item topics
                    if any(topic.lower() in [t.lower() for t in item_topics] for topic in topics):
                        item_data = {
                            'id': all_results['ids'][i],
                            'document': all_results['documents'][i],
                            'metadata': metadata
                        }
                        
                        # Parse comma-separated lists
                        item_data['metadata']['topics'] = item_topics
                        if 'people_involved' in metadata:
                            people_str = metadata['people_involved']
                            item_data['metadata']['people_involved'] = people_str.split(',') if people_str else []
                        if 'teams_involved' in metadata:
                            teams_str = metadata['teams_involved']
                            item_data['metadata']['teams_involved'] = teams_str.split(',') if teams_str else []
                        
                        matching_items.append(item_data)
            
            logger.info(f"✓ Found {len(matching_items)} items for topics: {topics}")
            return matching_items
            
        except Exception as e:
            logger.error(f"❌ Error searching by topic: {e}")
            return []
    
    def get_by_id(self, item_id: str) -> Optional[Dict]:
        """
        Get knowledge item by ID
        
        Args:
            item_id: Knowledge item ID
            
        Returns:
            Knowledge item as dictionary or None
        """
        if not self.collection:
            raise RuntimeError("Vector store not initialized. Call initialize_store() first.")
        
        try:
            results = self.collection.get(ids=[item_id])
            
            if results and results['ids'] and len(results['ids']) > 0:
                item_data = {
                    'id': results['ids'][0],
                    'document': results['documents'][0],
                    'metadata': results['metadatas'][0]
                }
                
                # Parse comma-separated lists
                metadata = item_data['metadata']
                if 'topics' in metadata:
                    topics_str = metadata['topics']
                    item_data['metadata']['topics'] = topics_str.split(',') if topics_str else []
                if 'people_involved' in metadata:
                    people_str = metadata['people_involved']
                    item_data['metadata']['people_involved'] = people_str.split(',') if people_str else []
                if 'teams_involved' in metadata:
                    teams_str = metadata['teams_involved']
                    item_data['metadata']['teams_involved'] = teams_str.split(',') if teams_str else []
                
                return item_data
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error getting item by ID: {e}")
            return None
    
    def get_stats(self) -> Dict:
        """
        Get vector store statistics
        
        Returns:
            Dictionary with store statistics
        """
        if not self.collection:
            return {
                "total_items": 0,
                "items_by_type": {},
                "items_by_outcome": {}
            }
        
        try:
            # Get all items
            all_results = self.collection.get()
            
            total_items = len(all_results['ids']) if all_results['ids'] else 0
            
            # Count by type and outcome
            items_by_type = {}
            items_by_outcome = {}
            
            if all_results['metadatas']:
                for metadata in all_results['metadatas']:
                    content_type = metadata.get('content_type', 'unknown')
                    outcome = metadata.get('outcome', 'unknown')
                    
                    items_by_type[content_type] = items_by_type.get(content_type, 0) + 1
                    items_by_outcome[outcome] = items_by_outcome.get(outcome, 0) + 1
            
            return {
                "total_items": total_items,
                "items_by_type": items_by_type,
                "items_by_outcome": items_by_outcome
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting stats: {e}")
            return {
                "total_items": 0,
                "items_by_type": {},
                "items_by_outcome": {}
            }
