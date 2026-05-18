"""
Knowledge Extraction Engine
Uses Google Gemini to extract structured knowledge from raw enterprise data
"""

import logging
import json
import time
import uuid
from typing import List, Dict, Optional
from datetime import datetime
import google.generativeai as genai

logger = logging.getLogger(__name__)


class KnowledgeItem:
    """Structured knowledge item extracted from enterprise data"""
    
    def __init__(self, data: Dict):
        self.id = data.get('id', str(uuid.uuid4()))
        self.content_type = data.get('content_type')  # decision, failure, success, lesson, expertise, context
        self.title = data.get('title', '')
        self.summary = data.get('summary', '')
        self.key_facts = data.get('key_facts', [])
        self.people_involved = data.get('people_involved', [])
        self.teams_involved = data.get('teams_involved', [])
        self.date_occurred = data.get('date_occurred')
        self.topics = data.get('topics', [])
        self.outcome = data.get('outcome', 'unknown')  # success, failure, ongoing, unknown
        self.importance_score = data.get('importance_score', 5)
        self.source_type = data.get('source_type')  # slack, jira, document, email, transcript
        self.source_reference = data.get('source_reference', '')
        self.raw_excerpt = data.get('raw_excerpt', '')
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'id': self.id,
            'content_type': self.content_type,
            'title': self.title,
            'summary': self.summary,
            'key_facts': self.key_facts,
            'people_involved': self.people_involved,
            'teams_involved': self.teams_involved,
            'date_occurred': self.date_occurred,
            'topics': self.topics,
            'outcome': self.outcome,
            'importance_score': self.importance_score,
            'source_type': self.source_type,
            'source_reference': self.source_reference,
            'raw_excerpt': self.raw_excerpt
        }


class KnowledgeExtractor:
    """Extract structured knowledge using Gemini AI"""
    
    def __init__(self, gemini_api_key: str):
        self.api_key = gemini_api_key
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')  # Using gemini-2.5-flash (available model)
        
        # Generation config for consistent JSON output
        self.generation_config = {
            'temperature': 0.2,  # Lower temperature for more consistent extraction
            'top_p': 0.8,
            'top_k': 40,
            'max_output_tokens': 8192,
        }
        
        logger.info("✅ KnowledgeExtractor initialized with Gemini 1.5 Pro")
    
    def _build_extraction_prompt(self, text: str, source_type: str) -> str:
        """Build the Gemini prompt for knowledge extraction"""
        
        prompt = f"""You are an expert at extracting institutional knowledge from enterprise communications.

Your task: Analyze the following {source_type} content and extract ALL significant knowledge items.

WHAT TO EXTRACT:
- Decisions made (with rationale)
- Failures and incidents (with root causes)
- Successes and achievements
- Lessons learned
- Expertise signals (who knows what)
- Important context about projects, systems, or processes

WHAT TO IGNORE:
- Casual greetings or small talk
- Meeting scheduling
- Simple status updates without context
- Trivial conversations

OUTPUT FORMAT:
Return a JSON array of knowledge items. Each item must have this exact structure:
{{
  "content_type": "decision|failure|success|lesson|expertise|context",
  "title": "Short descriptive title (max 100 chars)",
  "summary": "2-3 sentence summary of the knowledge",
  "key_facts": ["fact 1", "fact 2", "fact 3"],
  "people_involved": ["Name1", "Name2"],
  "teams_involved": ["engineering", "product", "design"],
  "date_occurred": "YYYY-MM or null",
  "topics": ["topic1", "topic2"],
  "outcome": "success|failure|ongoing|unknown",
  "raw_excerpt": "Most relevant quote from the original text"
}}

EXAMPLES:

Example 1 - Failure:
{{
  "content_type": "failure",
  "title": "PostgreSQL Migration Failed Due to Connection Pool Issues",
  "summary": "Database migration from MySQL to PostgreSQL failed in production causing 45-minute outage. Root cause was pgBouncer connection pool misconfigured with max_connections=100 instead of 500+. Cost $500K and 3 months of work.",
  "key_facts": [
    "Connection pool exhaustion caused cascading failures",
    "pgBouncer max_connections set too low (100 vs 500+ needed)",
    "Never load tested with production traffic levels",
    "Rollback completed successfully with no data loss"
  ],
  "people_involved": ["Sarah Chen", "Maria Garcia", "David Thompson"],
  "teams_involved": ["engineering", "devops"],
  "date_occurred": "2023-09",
  "topics": ["database", "postgresql", "migration", "connection-pooling", "incident"],
  "outcome": "failure",
  "raw_excerpt": "Connection pool exhaustion is causing cascading failures. We're seeing 500 errors in production. Rolling back now."
}}

Example 2 - Decision:
{{
  "content_type": "decision",
  "title": "Standardized on React for Frontend Development",
  "summary": "After evaluating React and Vue, team decided to standardize on React. Key reasons: better TypeScript support, larger ecosystem, easier hiring, React Native for mobile, and existing team knowledge.",
  "key_facts": [
    "React has superior TypeScript integration",
    "Larger talent pool for hiring",
    "React Native provides mobile development path",
    "80% of team already knows React"
  ],
  "people_involved": ["James Wilson", "Lisa Park", "David Thompson"],
  "teams_involved": ["engineering", "architecture"],
  "date_occurred": "2022-03",
  "topics": ["frontend", "react", "vue", "architecture", "technology-choice"],
  "outcome": "success",
  "raw_excerpt": "Decision: React. Reasons: 1) Better TypeScript support 2) Larger talent pool 3) More third-party libraries 4) Better mobile story with React Native"
}}

Now analyze this {source_type} content:

---
{text}
---

Return ONLY a valid JSON array of knowledge items. No markdown, no explanation, just the JSON array.
If no significant knowledge is found, return an empty array: []
"""
        return prompt
    
    def extract_knowledge(
        self,
        text: str,
        source_type: str,
        source_id: str
    ) -> List[KnowledgeItem]:
        """
        Extract knowledge items from text using Gemini
        
        Args:
            text: Raw text content to analyze
            source_type: Type of source (slack, jira, document, etc.)
            source_id: Unique identifier for the source
            
        Returns:
            List of extracted KnowledgeItem objects
        """
        if not text or len(text.strip()) < 20:
            logger.debug(f"Skipping extraction for {source_id}: text too short")
            return []
        
        try:
            # Build prompt
            prompt = self._build_extraction_prompt(text, source_type)
            
            # Call Gemini with retry logic
            response_text = self._call_gemini_with_retry(prompt)
            
            # Parse JSON response
            knowledge_items = self._parse_gemini_response(response_text, source_type, source_id)
            
            # Score importance for each item
            for item in knowledge_items:
                item.importance_score = self.score_importance(item)
            
            logger.info(f"✓ Extracted {len(knowledge_items)} knowledge items from {source_id}")
            return knowledge_items
            
        except Exception as e:
            logger.error(f"❌ Error extracting knowledge from {source_id}: {e}")
            return []
    
    def _call_gemini_with_retry(self, prompt: str, max_retries: int = 3) -> str:
        """Call Gemini API with exponential backoff retry logic"""
        
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config=self.generation_config
                )
                
                if response and response.text:
                    return response.text
                else:
                    raise Exception("Empty response from Gemini")
                    
            except Exception as e:
                wait_time = (2 ** attempt) * 0.5  # Exponential backoff: 0.5s, 1s, 2s
                
                if attempt < max_retries - 1:
                    logger.warning(f"Gemini API error (attempt {attempt + 1}/{max_retries}): {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Gemini API failed after {max_retries} attempts: {e}")
                    raise
        
        raise Exception("Failed to get response from Gemini")
    
    def _parse_gemini_response(
        self,
        response_text: str,
        source_type: str,
        source_id: str
    ) -> List[KnowledgeItem]:
        """Parse Gemini's JSON response into KnowledgeItem objects"""
        
        try:
            # Clean response (remove markdown code blocks if present)
            cleaned_text = response_text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.startswith('```'):
                cleaned_text = cleaned_text[3:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
            cleaned_text = cleaned_text.strip()
            
            # Parse JSON
            items_data = json.loads(cleaned_text)
            
            if not isinstance(items_data, list):
                logger.warning(f"Expected JSON array, got {type(items_data)}")
                return []
            
            # Convert to KnowledgeItem objects
            knowledge_items = []
            for item_data in items_data:
                # Add source metadata
                item_data['source_type'] = source_type
                item_data['source_reference'] = source_id
                
                # Create KnowledgeItem
                item = KnowledgeItem(item_data)
                knowledge_items.append(item)
            
            return knowledge_items
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from Gemini response: {e}")
            logger.debug(f"Response text: {response_text[:500]}...")
            return []
        except Exception as e:
            logger.error(f"Error parsing Gemini response: {e}")
            return []
    
    def batch_extract(self, items: List[Dict]) -> List[KnowledgeItem]:
        """
        Process multiple source items efficiently
        
        Args:
            items: List of source items with 'text', 'source_type', 'source_id'
            
        Returns:
            List of extracted KnowledgeItem objects
        """
        all_knowledge = []
        total = len(items)
        
        logger.info(f"🔄 Starting batch extraction for {total} items...")
        
        for idx, item in enumerate(items, 1):
            text = item.get('text', '')
            source_type = item.get('source_type', 'unknown')
            source_id = item.get('source_id', f'item_{idx}')
            
            logger.info(f"  [{idx}/{total}] Processing {source_id}...")
            
            # Extract knowledge
            knowledge_items = self.extract_knowledge(text, source_type, source_id)
            all_knowledge.extend(knowledge_items)
            
            # Rate limiting: 500ms delay between API calls
            if idx < total:
                time.sleep(0.5)
        
        logger.info(f"✅ Batch extraction complete: {len(all_knowledge)} total knowledge items extracted")
        return all_knowledge
    
    def score_importance(self, item: KnowledgeItem) -> int:
        """
        Score the importance of a knowledge item (1-10)
        
        Args:
            item: KnowledgeItem to score
            
        Returns:
            Importance score (1-10)
        """
        score = 5  # Base score
        
        # Failures and incidents are important
        if item.content_type in ['failure', 'incident']:
            score += 3
        
        # Decisions with reasoning are valuable
        if item.content_type == 'decision' and len(item.key_facts) > 2:
            score += 2
        
        # Multiple people involved = more significant
        if len(item.people_involved) > 2:
            score += 1
        
        # Has specific dates = more concrete
        if item.date_occurred:
            score += 1
        
        # Financial impact mentioned (simple heuristic)
        summary_lower = item.summary.lower()
        if any(word in summary_lower for word in ['cost', 'revenue', 'budget', 'million', 'dollar', '$']):
            score += 3
        
        return min(score, 10)  # Cap at 10
