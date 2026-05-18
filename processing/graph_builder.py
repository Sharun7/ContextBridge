"""
Knowledge Graph Builder
Builds a NetworkX graph from extracted knowledge items
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime
import networkx as nx
from processing.knowledge_extractor import KnowledgeItem

logger = logging.getLogger(__name__)


class GraphBuilder:
    """Build and query knowledge graph using NetworkX"""
    
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        self.knowledge_items = {}  # Store KnowledgeItem objects by ID
        logger.info("GraphBuilder initialized")
    
    def build_graph(self, items: List[KnowledgeItem]) -> nx.MultiDiGraph:
        """
        Build knowledge graph from KnowledgeItems
        
        Creates nodes for:
        - KnowledgeItem nodes (decisions, failures, lessons)
        - Person nodes (people involved)
        - Topic nodes (subjects)
        - Team nodes (engineering, product, etc.)
        
        Creates edges for:
        - PERSON_INVOLVED_IN (person → knowledge item)
        - ITEM_HAS_TOPIC (knowledge item → topic)
        - TEAM_INVOLVED_IN (team → knowledge item)
        - RELATED_TO (knowledge item → knowledge item, when topics overlap)
        
        Args:
            items: List of KnowledgeItem objects
            
        Returns:
            NetworkX MultiDiGraph
        """
        logger.info(f"🔨 Building knowledge graph from {len(items)} items...")
        
        # Clear existing graph
        self.graph.clear()
        self.knowledge_items.clear()
        
        # Store items for later retrieval
        for item in items:
            self.knowledge_items[item.id] = item
        
        # Step 1: Add KnowledgeItem nodes
        for item in items:
            self.graph.add_node(
                item.id,
                node_type='knowledge_item',
                content_type=item.content_type,
                title=item.title,
                summary=item.summary,
                outcome=item.outcome,
                importance_score=item.importance_score,
                date_occurred=item.date_occurred,
                source_type=item.source_type
            )
        
        # Step 2: Add Person nodes and PERSON_INVOLVED_IN edges
        for item in items:
            for person in item.people_involved:
                person_id = f"person:{person.lower().replace(' ', '_')}"
                
                # Add person node if not exists
                if not self.graph.has_node(person_id):
                    self.graph.add_node(
                        person_id,
                        node_type='person',
                        name=person
                    )
                
                # Add edge: person → knowledge item
                self.graph.add_edge(
                    person_id,
                    item.id,
                    edge_type='PERSON_INVOLVED_IN'
                )
        
        # Step 3: Add Topic nodes and ITEM_HAS_TOPIC edges
        for item in items:
            for topic in item.topics:
                topic_id = f"topic:{topic.lower().replace(' ', '_')}"
                
                # Add topic node if not exists
                if not self.graph.has_node(topic_id):
                    self.graph.add_node(
                        topic_id,
                        node_type='topic',
                        name=topic
                    )
                
                # Add edge: knowledge item → topic
                self.graph.add_edge(
                    item.id,
                    topic_id,
                    edge_type='ITEM_HAS_TOPIC'
                )
        
        # Step 4: Add Team nodes and TEAM_INVOLVED_IN edges
        for item in items:
            for team in item.teams_involved:
                team_id = f"team:{team.lower().replace(' ', '_')}"
                
                # Add team node if not exists
                if not self.graph.has_node(team_id):
                    self.graph.add_node(
                        team_id,
                        node_type='team',
                        name=team
                    )
                
                # Add edge: team → knowledge item
                self.graph.add_edge(
                    team_id,
                    item.id,
                    edge_type='TEAM_INVOLVED_IN'
                )
        
        # Step 5: Add RELATED_TO edges between knowledge items with overlapping topics
        for i, item1 in enumerate(items):
            for item2 in items[i+1:]:
                # Find common topics
                common_topics = set(item1.topics) & set(item2.topics)
                
                if common_topics:
                    # Add bidirectional edges
                    self.graph.add_edge(
                        item1.id,
                        item2.id,
                        edge_type='RELATED_TO',
                        common_topics=list(common_topics)
                    )
                    self.graph.add_edge(
                        item2.id,
                        item1.id,
                        edge_type='RELATED_TO',
                        common_topics=list(common_topics)
                    )
        
        # Log statistics
        node_counts = {}
        for node, data in self.graph.nodes(data=True):
            node_type = data.get('node_type', 'unknown')
            node_counts[node_type] = node_counts.get(node_type, 0) + 1
        
        edge_counts = {}
        for u, v, data in self.graph.edges(data=True):
            edge_type = data.get('edge_type', 'unknown')
            edge_counts[edge_type] = edge_counts.get(edge_type, 0) + 1
        
        logger.info(f"✅ Knowledge graph built successfully!")
        logger.info(f"   Nodes: {self.graph.number_of_nodes()} ({node_counts})")
        logger.info(f"   Edges: {self.graph.number_of_edges()} ({edge_counts})")
        
        return self.graph
    
    def find_related_items(
        self,
        item_id: str,
        max_hops: int = 2
    ) -> List[Dict]:
        """
        Find items related to a given item using graph traversal
        
        Args:
            item_id: ID of the knowledge item
            max_hops: Maximum graph distance to search
            
        Returns:
            List of related knowledge items with distance
        """
        if not self.graph.has_node(item_id):
            logger.warning(f"Item {item_id} not found in graph")
            return []
        
        try:
            # Find all nodes within max_hops distance
            related = []
            
            # Use BFS to find nodes within max_hops
            visited = {item_id: 0}  # node -> distance
            queue = [(item_id, 0)]
            
            while queue:
                current_node, distance = queue.pop(0)
                
                if distance >= max_hops:
                    continue
                
                # Get neighbors
                for neighbor in self.graph.neighbors(current_node):
                    if neighbor not in visited:
                        visited[neighbor] = distance + 1
                        queue.append((neighbor, distance + 1))
                        
                        # If neighbor is a knowledge item, add to results
                        node_data = self.graph.nodes[neighbor]
                        if node_data.get('node_type') == 'knowledge_item':
                            related.append({
                                'id': neighbor,
                                'distance': distance + 1,
                                'title': node_data.get('title', ''),
                                'content_type': node_data.get('content_type', ''),
                                'importance_score': node_data.get('importance_score', 0)
                            })
            
            # Sort by distance, then by importance
            related.sort(key=lambda x: (x['distance'], -x['importance_score']))
            
            logger.info(f"✓ Found {len(related)} related items for {item_id}")
            return related
            
        except Exception as e:
            logger.error(f"❌ Error finding related items: {e}")
            return []
    
    def find_expert(self, topic: str) -> List[Dict]:
        """
        Find experts on a given topic
        
        Args:
            topic: Topic to search for
            
        Returns:
            List of people with expertise and evidence (sorted by expertise)
        """
        topic_id = f"topic:{topic.lower().replace(' ', '_')}"
        
        if not self.graph.has_node(topic_id):
            logger.warning(f"Topic '{topic}' not found in graph")
            return []
        
        try:
            # Find all people connected to this topic through knowledge items
            experts = {}  # person_name -> {count, items, importance_sum}
            
            # Get all knowledge items with this topic
            for pred in self.graph.predecessors(topic_id):
                node_data = self.graph.nodes[pred]
                if node_data.get('node_type') == 'knowledge_item':
                    item_id = pred
                    importance = node_data.get('importance_score', 0)
                    
                    # Find people involved in this item
                    for person_node in self.graph.predecessors(item_id):
                        person_data = self.graph.nodes[person_node]
                        if person_data.get('node_type') == 'person':
                            person_name = person_data.get('name', '')
                            
                            if person_name not in experts:
                                experts[person_name] = {
                                    'name': person_name,
                                    'item_count': 0,
                                    'items': [],
                                    'total_importance': 0
                                }
                            
                            experts[person_name]['item_count'] += 1
                            experts[person_name]['total_importance'] += importance
                            experts[person_name]['items'].append({
                                'id': item_id,
                                'title': node_data.get('title', ''),
                                'content_type': node_data.get('content_type', ''),
                                'importance_score': importance
                            })
            
            # Convert to list and sort by total importance
            expert_list = list(experts.values())
            expert_list.sort(key=lambda x: (-x['total_importance'], -x['item_count']))
            
            logger.info(f"✓ Found {len(expert_list)} experts for topic '{topic}'")
            return expert_list
            
        except Exception as e:
            logger.error(f"❌ Error finding experts: {e}")
            return []
    
    def get_item_history(self, topic: str) -> List[Dict]:
        """
        Get chronological history of items related to a topic
        
        Args:
            topic: Topic to search for
            
        Returns:
            Chronologically sorted list of knowledge items
        """
        topic_id = f"topic:{topic.lower().replace(' ', '_')}"
        
        if not self.graph.has_node(topic_id):
            logger.warning(f"Topic '{topic}' not found in graph")
            return []
        
        try:
            # Get all knowledge items with this topic
            items = []
            
            for pred in self.graph.predecessors(topic_id):
                node_data = self.graph.nodes[pred]
                if node_data.get('node_type') == 'knowledge_item':
                    items.append({
                        'id': pred,
                        'title': node_data.get('title', ''),
                        'content_type': node_data.get('content_type', ''),
                        'outcome': node_data.get('outcome', ''),
                        'importance_score': node_data.get('importance_score', 0),
                        'date_occurred': node_data.get('date_occurred', 'unknown'),
                        'summary': node_data.get('summary', '')
                    })
            
            # Sort chronologically (items with dates first, then by importance)
            def sort_key(item):
                date_str = item['date_occurred']
                if date_str and date_str != 'unknown':
                    try:
                        # Parse YYYY-MM format
                        return (0, date_str)
                    except:
                        pass
                return (1, -item['importance_score'])
            
            items.sort(key=sort_key)
            
            logger.info(f"✓ Found {len(items)} items in history for topic '{topic}'")
            return items
            
        except Exception as e:
            logger.error(f"❌ Error getting item history: {e}")
            return []
    
    def export_graph_json(self) -> Dict:
        """
        Export graph in D3.js compatible JSON format
        
        Returns:
            Dictionary with 'nodes' and 'links' arrays
        """
        try:
            # Define colors for different node types
            color_map = {
                'knowledge_item': '#3b82f6',  # Blue
                'person': '#10b981',           # Green
                'topic': '#f59e0b',            # Orange
                'team': '#8b5cf6'              # Purple
            }
            
            # Build nodes array
            nodes = []
            for node_id, node_data in self.graph.nodes(data=True):
                node_type = node_data.get('node_type', 'unknown')
                
                # Determine label based on node type
                if node_type == 'knowledge_item':
                    label = node_data.get('title', node_id)[:50]
                else:
                    label = node_data.get('name', node_id)
                
                nodes.append({
                    'id': node_id,
                    'label': label,
                    'type': node_type,
                    'color': color_map.get(node_type, '#6b7280'),
                    'data': node_data
                })
            
            # Build links array
            links = []
            for source, target, edge_data in self.graph.edges(data=True):
                links.append({
                    'source': source,
                    'target': target,
                    'type': edge_data.get('edge_type', 'unknown')
                })
            
            logger.info(f"✓ Exported graph: {len(nodes)} nodes, {len(links)} links")
            
            return {
                'nodes': nodes,
                'links': links
            }
            
        except Exception as e:
            logger.error(f"❌ Error exporting graph: {e}")
            return {'nodes': [], 'links': []}
