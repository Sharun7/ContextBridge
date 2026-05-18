import axios from 'axios';

// Determine API base URL based on environment
const API_BASE_URL = process.env.REACT_APP_API_URL 
  ? `${process.env.REACT_APP_API_URL}/api`
  : (process.env.NODE_ENV === 'production'
    ? 'https://contextbridge-backend.onrender.com/api'
    : 'http://localhost:8000/api');

console.log('API Base URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout for production
});

export const apiService = {
  // Stats
  getStats: () => api.get('/stats'),
  
  // Demo scenarios
  runScenario: (scenarioId: string) => 
    api.post(`/demo/scenario/${scenarioId}`),
  
  seedDemoData: () => api.post('/demo/seed'),
  
  // Query
  query: (question: string, userId?: string) =>
    api.post('/query', { question, user_id: userId }),
  
  // Knowledge search
  searchKnowledge: (params: {
    q: string;
    type?: string;
    topics?: string;
    outcome?: string;
    limit?: number;
  }) => api.get('/knowledge/search', { params }),
  
  // Get knowledge item by ID
  getKnowledgeItem: (id: string) => api.get(`/knowledge/${id}`),
  
  // Graph
  getGraph: (focusTopic?: string) =>
    api.get('/graph', { params: { focus_topic: focusTopic } }),
  
  // Experts
  getExperts: (topic: string) =>
    api.get('/experts', { params: { topic } }),
  
  // Health
  getHealth: () => api.get('/health'),
};

export default apiService;
