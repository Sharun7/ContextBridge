export interface ProactiveAlert {
  alert_id: string;
  trigger_type: 'jira' | 'document' | 'query';
  trigger_content: string;
  alert_level: 'warning' | 'info' | 'expert_needed';
  headline: string;
  context_items: any[];
  synthesized_insight: string;
  recommended_actions: string[];
  relevant_people: string[];
  confidence_score: number;
  timestamp: string;
}

export interface Stats {
  total_knowledge_items: number;
  items_by_type: Record<string, number>;
  items_by_outcome: Record<string, number>;
  recent_alerts: number;
  top_topics: Array<{ topic: string; count: number }>;
}

export interface KnowledgeItem {
  id: string;
  content_type: string;
  title: string;
  summary: string;
  key_facts: string[];
  people_involved: string[];
  teams_involved: string[];
  date_occurred?: string;
  topics: string[];
  outcome: string;
  importance_score: number;
  source_type: string;
  source_reference: string;
}

export interface GraphData {
  nodes: Array<{
    id: string;
    label: string;
    type: string;
    color: string;
    data: any;
  }>;
  links: Array<{
    source: string;
    target: string;
    type: string;
  }>;
}
