"""
Proactive Intelligence Engine
Detects triggers and surfaces relevant institutional memory automatically
"""

import logging
from typing import Optional, Dict, List
from datetime import datetime
import uuid
import google.generativeai as genai

logger = logging.getLogger(__name__)


class ProactiveAlert:
    """Proactive alert with context and recommendations"""
    
    def __init__(self, data: Dict):
        self.alert_id = data.get('alert_id', str(uuid.uuid4()))
        self.trigger_type = data.get('trigger_type')  # jira, document, query
        self.trigger_content = data.get('trigger_content')
        self.alert_level = data.get('alert_level')  # warning, info, expert_needed
        self.headline = data.get('headline')
        self.context_items = data.get('context_items', [])
        self.synthesized_insight = data.get('synthesized_insight')
        self.recommended_actions = data.get('recommended_actions', [])
        self.relevant_people = data.get('relevant_people', [])
        self.confidence_score = data.get('confidence_score', 0)
        self.timestamp = data.get('timestamp', datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'alert_id': self.alert_id,
            'trigger_type': self.trigger_type,
            'trigger_content': self.trigger_content,
            'alert_level': self.alert_level,
            'headline': self.headline,
            'context_items': self.context_items,
            'synthesized_insight': self.synthesized_insight,
            'recommended_actions': self.recommended_actions,
            'relevant_people': self.relevant_people,
            'confidence_score': self.confidence_score,
            'timestamp': self.timestamp
        }


class ProactiveEngine:
    """Proactive context surfacing engine - THE MAGIC FEATURE"""
    
    def __init__(self, vector_store, graph_builder, gemini_api_key: str):
        self.vector_store = vector_store
        self.graph_builder = graph_builder
        self.api_key = gemini_api_key
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Generation config for synthesis
        self.generation_config = {
            'temperature': 0.3,  # Slightly higher for more natural synthesis
            'top_p': 0.9,
            'top_k': 40,
            'max_output_tokens': 2048,
        }
        
        logger.info("✅ ProactiveEngine initialized with Gemini 2.5 Flash")
    
    def handle_jira_trigger(
        self,
        ticket_title: str,
        ticket_description: str
    ) -> Optional[ProactiveAlert]:
        """
        Handle Jira ticket creation trigger
        
        Detects when someone is about to work on something that has relevant history.
        
        Args:
            ticket_title: Title of the Jira ticket
            ticket_description: Description of the ticket
            
        Returns:
            ProactiveAlert if relevant history found with importance >= 6, None otherwise
        """
        logger.info(f"🔍 Handling Jira trigger: {ticket_title}")
        
        try:
            # Combine title and description for search
            trigger_text = f"{ticket_title}\n\n{ticket_description}"
            
            # Search vector store for similar past items
            search_results = self.vector_store.search_similar(
                query=trigger_text,
                top_k=5
            )
            
            if not search_results:
                logger.info("No relevant history found")
                return None
            
            # Filter by importance score >= 6
            significant_items = [
                item for item in search_results 
                if item['metadata'].get('importance_score', 0) >= 6
            ]
            
            if not significant_items:
                logger.info("No significant history found (importance < 6)")
                return None
            
            # Calculate confidence
            confidence = self.calculate_confidence(significant_items, trigger_text)
            
            # Only alert if confidence >= 60
            if confidence < 60:
                logger.info(f"Confidence too low ({confidence}), not alerting")
                return None
            
            # Determine alert level
            alert_level = self._determine_alert_level(significant_items)
            
            # Find relevant people from graph
            relevant_people = self._find_relevant_people(significant_items)
            
            # Generate synthesized insight using Gemini
            synthesized_insight = self._synthesize_insight(
                trigger_type='jira',
                trigger_text=trigger_text,
                context_items=significant_items
            )
            
            # Extract recommended actions from insight
            recommended_actions = self._extract_actions(synthesized_insight, significant_items)
            
            # Create headline
            headline = self._create_headline(significant_items, alert_level)
            
            # Create alert
            alert = ProactiveAlert({
                'trigger_type': 'jira',
                'trigger_content': trigger_text,
                'alert_level': alert_level,
                'headline': headline,
                'context_items': significant_items,
                'synthesized_insight': synthesized_insight,
                'recommended_actions': recommended_actions,
                'relevant_people': relevant_people,
                'confidence_score': confidence
            })
            
            logger.info(f"✅ Generated {alert_level} alert with {confidence}% confidence")
            return alert
            
        except Exception as e:
            logger.error(f"❌ Error handling Jira trigger: {e}")
            return None
    
    def handle_document_trigger(
        self,
        document_title: str,
        document_content: str
    ) -> Optional[ProactiveAlert]:
        """
        Handle document creation trigger
        
        Detects when someone is writing about something with relevant history.
        
        Args:
            document_title: Title of the document
            document_content: Content of the document
            
        Returns:
            ProactiveAlert if relevant history found with importance >= 6, None otherwise
        """
        logger.info(f"🔍 Handling document trigger: {document_title}")
        
        try:
            # Combine title and content for search
            trigger_text = f"{document_title}\n\n{document_content}"
            
            # Search vector store for similar past items
            search_results = self.vector_store.search_similar(
                query=trigger_text,
                top_k=5
            )
            
            if not search_results:
                logger.info("No relevant history found")
                return None
            
            # Filter by importance score >= 6
            significant_items = [
                item for item in search_results 
                if item['metadata'].get('importance_score', 0) >= 6
            ]
            
            if not significant_items:
                logger.info("No significant history found (importance < 6)")
                return None
            
            # Calculate confidence
            confidence = self.calculate_confidence(significant_items, trigger_text)
            
            # Only alert if confidence >= 60
            if confidence < 60:
                logger.info(f"Confidence too low ({confidence}), not alerting")
                return None
            
            # Determine alert level
            alert_level = self._determine_alert_level(significant_items)
            
            # Find relevant people from graph
            relevant_people = self._find_relevant_people(significant_items)
            
            # Generate synthesized insight using Gemini
            synthesized_insight = self._synthesize_insight(
                trigger_type='document',
                trigger_text=trigger_text,
                context_items=significant_items
            )
            
            # Extract recommended actions
            recommended_actions = self._extract_actions(synthesized_insight, significant_items)
            
            # Create headline
            headline = self._create_headline(significant_items, alert_level)
            
            # Create alert
            alert = ProactiveAlert({
                'trigger_type': 'document',
                'trigger_content': trigger_text,
                'alert_level': alert_level,
                'headline': headline,
                'context_items': significant_items,
                'synthesized_insight': synthesized_insight,
                'recommended_actions': recommended_actions,
                'relevant_people': relevant_people,
                'confidence_score': confidence
            })
            
            logger.info(f"✅ Generated {alert_level} alert with {confidence}% confidence")
            return alert
            
        except Exception as e:
            logger.error(f"❌ Error handling document trigger: {e}")
            return None
    
    def handle_query_trigger(self, query: str) -> ProactiveAlert:
        """
        Handle direct user query
        
        Always returns a response (never None) since user explicitly asked.
        
        Args:
            query: User's question
            
        Returns:
            ProactiveAlert with answer and citations
        """
        logger.info(f"🔍 Handling query: {query}")
        
        try:
            # Search vector store
            vector_results = self.vector_store.search_similar(
                query=query,
                top_k=5
            )
            
            # Also search graph for related items and experts
            # Extract potential topics from query
            query_lower = query.lower()
            topics = []
            for word in query_lower.split():
                if len(word) > 4:  # Simple heuristic for topic words
                    topics.append(word)
            
            # Get experts if topics found
            relevant_people = []
            if topics:
                for topic in topics[:3]:  # Limit to first 3 topics
                    experts = self.graph_builder.find_expert(topic)
                    for expert in experts[:2]:  # Top 2 experts per topic
                        if expert['name'] not in relevant_people:
                            relevant_people.append(expert['name'])
            
            # Calculate confidence
            confidence = self.calculate_confidence(vector_results, query) if vector_results else 30
            
            # Determine alert level (queries are usually info or expert_needed)
            if relevant_people:
                alert_level = 'expert_needed'
            elif vector_results:
                alert_level = 'info'
            else:
                alert_level = 'info'
            
            # Generate synthesized insight
            if vector_results:
                synthesized_insight = self._synthesize_insight(
                    trigger_type='query',
                    trigger_text=query,
                    context_items=vector_results
                )
            else:
                synthesized_insight = "I couldn't find specific institutional knowledge related to your query. This might be a new topic for the organization, or the information hasn't been captured yet."
            
            # Extract recommended actions
            recommended_actions = self._extract_actions(synthesized_insight, vector_results)
            
            # Create headline
            if vector_results:
                headline = f"Found {len(vector_results)} relevant items from organizational history"
            else:
                headline = "No specific organizational history found for this query"
            
            # Create alert
            alert = ProactiveAlert({
                'trigger_type': 'query',
                'trigger_content': query,
                'alert_level': alert_level,
                'headline': headline,
                'context_items': vector_results,
                'synthesized_insight': synthesized_insight,
                'recommended_actions': recommended_actions,
                'relevant_people': relevant_people,
                'confidence_score': confidence
            })
            
            logger.info(f"✅ Generated query response with {confidence}% confidence")
            return alert
            
        except Exception as e:
            logger.error(f"❌ Error handling query: {e}")
            # Return a fallback alert
            return ProactiveAlert({
                'trigger_type': 'query',
                'trigger_content': query,
                'alert_level': 'info',
                'headline': 'Error processing query',
                'synthesized_insight': f'An error occurred while processing your query: {str(e)}',
                'confidence_score': 0
            })
    
    def calculate_confidence(
        self,
        context_items: List[Dict],
        trigger_text: str
    ) -> int:
        """
        Calculate confidence score for an alert
        
        Factors:
        - Distance/similarity scores from vector search
        - Importance scores of found items
        - Content type (failures are high confidence)
        - Number of matching items
        
        Args:
            context_items: List of relevant knowledge items
            trigger_text: Original trigger text
            
        Returns:
            Confidence score (0-100)
        """
        if not context_items:
            return 0
        
        confidence = 50  # Base confidence
        
        # Factor 1: Distance scores (lower distance = higher confidence)
        if context_items[0].get('distance') is not None:
            avg_distance = sum(item.get('distance', 2.0) for item in context_items) / len(context_items)
            # Distance typically ranges from 0-2, convert to confidence boost
            distance_boost = max(0, int((2.0 - avg_distance) * 15))
            confidence += distance_boost
        
        # Factor 2: Importance scores
        avg_importance = sum(
            item['metadata'].get('importance_score', 0) 
            for item in context_items
        ) / len(context_items)
        importance_boost = int(avg_importance * 2)  # Scale 0-10 to 0-20
        confidence += importance_boost
        
        # Factor 3: Content type (failures are high priority)
        has_failure = any(
            item['metadata'].get('content_type') == 'failure' 
            for item in context_items
        )
        if has_failure:
            confidence += 15
        
        # Factor 4: Number of matching items
        if len(context_items) >= 3:
            confidence += 10
        elif len(context_items) >= 2:
            confidence += 5
        
        # Cap at 100
        confidence = min(confidence, 100)
        
        return confidence
    
    def _determine_alert_level(self, context_items: List[Dict]) -> str:
        """Determine alert level based on context items"""
        # Check for failures
        has_failure = any(
            item['metadata'].get('content_type') == 'failure' 
            for item in context_items
        )
        
        # Check for high importance
        has_high_importance = any(
            item['metadata'].get('importance_score', 0) >= 8 
            for item in context_items
        )
        
        # Check for people involvement
        has_people = any(
            item['metadata'].get('people_involved') 
            for item in context_items
        )
        
        if has_failure and has_high_importance:
            return 'warning'
        elif has_people:
            return 'expert_needed'
        else:
            return 'info'
    
    def _find_relevant_people(self, context_items: List[Dict]) -> List[str]:
        """Extract relevant people from context items"""
        people = set()
        for item in context_items:
            people_list = item['metadata'].get('people_involved', [])
            if isinstance(people_list, list):
                people.update(people_list)
            elif isinstance(people_list, str) and people_list:
                people.update(people_list.split(','))
        return list(people)
    
    def _synthesize_insight(
        self,
        trigger_type: str,
        trigger_text: str,
        context_items: List[Dict]
    ) -> str:
        """
        Use Gemini to synthesize insight from context items
        
        Args:
            trigger_type: Type of trigger (jira, document, query)
            trigger_text: Original trigger text
            context_items: Relevant knowledge items
            
        Returns:
            Synthesized insight (3-5 sentences)
        """
        try:
            # Build context summary
            context_summary = ""
            for i, item in enumerate(context_items[:3], 1):  # Limit to top 3
                metadata = item['metadata']
                context_summary += f"\n{i}. [{metadata.get('content_type', 'unknown')}] "
                context_summary += f"Topics: {', '.join(metadata.get('topics', []))}\n"
                context_summary += f"   Outcome: {metadata.get('outcome', 'unknown')}\n"
                context_summary += f"   Importance: {metadata.get('importance_score', 0)}/10\n"
                context_summary += f"   Content: {item.get('document', '')[:300]}...\n"
            
            # Build prompt based on trigger type
            if trigger_type == 'query':
                action_desc = f"asking: '{trigger_text[:200]}'"
            elif trigger_type == 'jira':
                action_desc = f"creating a Jira ticket about: '{trigger_text[:200]}'"
            else:  # document
                action_desc = f"writing a document about: '{trigger_text[:200]}'"
            
            prompt = f"""You are an AI assistant helping surface institutional knowledge.

Someone is {action_desc}

Here is relevant historical context from the organization:
{context_summary}

Write a concise 3-5 sentence insight explaining what they should know from the organization's history before proceeding. Be specific about:
- What happened in the past
- When it occurred (if dates available)
- Who was involved
- What the outcome was
- A concrete recommendation based on this history

Be direct and actionable. Focus on the most important lessons learned.
"""
            
            # Call Gemini
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            if response and response.text:
                return response.text.strip()
            else:
                return "Unable to synthesize insight from the available context."
                
        except Exception as e:
            logger.error(f"Error synthesizing insight: {e}")
            return f"Found {len(context_items)} relevant items from organizational history. Review the context items for details."
    
    def _extract_actions(
        self,
        synthesized_insight: str,
        context_items: List[Dict]
    ) -> List[str]:
        """Extract recommended actions from insight and context"""
        actions = []
        
        # Extract from context items
        for item in context_items[:2]:  # Top 2 items
            metadata = item['metadata']
            content_type = metadata.get('content_type', '')
            
            if content_type == 'failure':
                actions.append(f"Review past failure: {metadata.get('topics', ['this topic'])[0]}")
            elif content_type == 'decision':
                actions.append(f"Consider previous decision on {metadata.get('topics', ['this topic'])[0]}")
            elif content_type == 'lesson':
                actions.append("Apply lessons learned from similar situations")
        
        # Add people-related actions
        people = []
        for item in context_items:
            people_list = item['metadata'].get('people_involved', [])
            if isinstance(people_list, list):
                people.extend(people_list)
            elif isinstance(people_list, str) and people_list:
                people.extend(people_list.split(','))
        
        if people:
            unique_people = list(set(people))[:2]
            actions.append(f"Consult with {', '.join(unique_people)} who have relevant experience")
        
        # Limit to 3 actions
        return actions[:3] if actions else ["Review the context items for relevant information"]
    
    def _create_headline(self, context_items: List[Dict], alert_level: str) -> str:
        """Create a concise headline for the alert"""
        if not context_items:
            return "No relevant history found"
        
        first_item = context_items[0]['metadata']
        content_type = first_item.get('content_type', 'item')
        
        if alert_level == 'warning':
            return f"⚠️ Warning: Similar {content_type} found in organizational history"
        elif alert_level == 'expert_needed':
            return f"💡 Relevant expertise available: {len(context_items)} related {content_type}(s) found"
        else:
            return f"ℹ️ Context available: {len(context_items)} related item(s) from organizational history"
