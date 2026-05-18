# SECTION 7 - React Frontend Dashboard
## Complete Implementation Guide

**Status**: 📋 **DESIGN COMPLETE - READY TO BUILD**

---

## Overview

A React TypeScript dashboard with Tailwind CSS, Recharts, and D3.js for visualizing ContextBridge's proactive intelligence.

---

## Project Setup

### 1. Create React App

```bash
cd contextbridge
npx create-react-app frontend --template typescript
cd frontend
```

### 2. Install Dependencies

```bash
npm install \
  tailwindcss postcss autoprefixer \
  @tanstack/react-query \
  axios \
  recharts \
  d3 \
  @types/d3 \
  react-router-dom \
  lucide-react \
  framer-motion
```

### 3. Initialize Tailwind CSS

```bash
npx tailwindcss init -p
```

---

## Color Scheme

```typescript
// src/theme/colors.ts
export const colors = {
  primary: '#1B4F72',      // Deep blue
  accent: '#2471A3',       // Medium blue
  success: '#1E8449',      // Green
  warning: '#D35400',      // Orange
  danger: '#C0392B',       // Red
  background: '#F4F6F9',   // Light gray
  card: '#FFFFFF',         // White
  text: {
    primary: '#2C3E50',
    secondary: '#7F8C8D',
    light: '#BDC3C7'
  }
};
```

---

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Sidebar.tsx
│   │   │   ├── TopBar.tsx
│   │   │   └── Layout.tsx
│   │   ├── dashboard/
│   │   │   ├── StatsCard.tsx
│   │   │   ├── RecentAlerts.tsx
│   │   │   └── TopTopicsChart.tsx
│   │   ├── demo/
│   │   │   ├── ScenarioButton.tsx
│   │   │   ├── AlertDisplay.tsx
│   │   │   └── LoadingAnimation.tsx
│   │   ├── query/
│   │   │   ├── SearchBar.tsx
│   │   │   └── ResultDisplay.tsx
│   │   ├── graph/
│   │   │   ├── KnowledgeGraph.tsx
│   │   │   ├── NodeDetails.tsx
│   │   │   └── GraphFilters.tsx
│   │   └── knowledge/
│   │       ├── KnowledgeTable.tsx
│   │       └── ItemDetailModal.tsx
│   ├── pages/
│   │   ├── Dashboard.tsx
│   │   ├── Demo.tsx
│   │   ├── Query.tsx
│   │   ├── Graph.tsx
│   │   └── KnowledgeBase.tsx
│   ├── services/
│   │   └── api.ts
│   ├── types/
│   │   └── index.ts
│   ├── theme/
│   │   └── colors.ts
│   ├── App.tsx
│   └── index.tsx
├── tailwind.config.js
└── package.json
```

---

## Core Files

### 1. API Service (`src/services/api.ts`)

```typescript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
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
    limit?: number;
  }) => api.get('/knowledge/search', { params }),
  
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
```

### 2. Types (`src/types/index.ts`)

```typescript
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
```

### 3. Layout Component (`src/components/layout/Layout.tsx`)

```typescript
import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import TopBar from './TopBar';

const Layout: React.FC = () => {
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <TopBar />
        <main className="flex-1 overflow-y-auto p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;
```

### 4. Sidebar (`src/components/layout/Sidebar.tsx`)

```typescript
import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Database, 
  MessageSquare, 
  Network, 
  Presentation 
} from 'lucide-react';

const Sidebar: React.FC = () => {
  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/knowledge', icon: Database, label: 'Knowledge Base' },
    { path: '/query', icon: MessageSquare, label: 'Query' },
    { path: '/graph', icon: Network, label: 'Graph' },
    { path: '/demo', icon: Presentation, label: 'Demo' },
  ];

  return (
    <div className="w-64 bg-[#1B4F72] text-white flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-blue-600">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-blue-400 rounded-lg flex items-center justify-center">
            🛡️🧠
          </div>
          <div>
            <h1 className="text-xl font-bold">ContextBridge</h1>
            <p className="text-xs text-blue-300">Institutional Memory</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-blue-200 hover:bg-blue-700'
              }`
            }
          >
            <item.icon size={20} />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-blue-600 text-xs text-blue-300">
        <p>TechEx Hackathon 2026</p>
        <p>Track 4: Data & Intelligence</p>
      </div>
    </div>
  );
};

export default Sidebar;
```

### 5. Demo Page (`src/pages/Demo.tsx`)

```typescript
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, Info, Users, Loader2 } from 'lucide-react';
import { useMutation } from '@tanstack/react-query';
import apiService from '../services/api';
import { ProactiveAlert } from '../types';

const Demo: React.FC = () => {
  const [selectedScenario, setSelectedScenario] = useState<string | null>(null);
  const [alert, setAlert] = useState<ProactiveAlert | null>(null);

  const scenarioMutation = useMutation({
    mutationFn: (scenarioId: string) => apiService.runScenario(scenarioId),
    onSuccess: (response) => {
      setAlert(response.data);
    },
  });

  const scenarios = [
    {
      id: 'A',
      title: 'Scenario A: Prevent a Mistake',
      icon: AlertTriangle,
      color: 'red',
      description: 'Database migration warning',
    },
    {
      id: 'B',
      title: 'Scenario B: Answer Why',
      icon: Info,
      color: 'blue',
      description: 'React vs Vue decision',
    },
    {
      id: 'C',
      title: 'Scenario C: Find Expert',
      icon: Users,
      color: 'green',
      description: 'Migration best practices',
    },
  ];

  const handleScenarioClick = (scenarioId: string) => {
    setSelectedScenario(scenarioId);
    setAlert(null);
    scenarioMutation.mutate(scenarioId);
  };

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Live Demo - Proactive Intelligence
        </h1>
        <p className="text-gray-600">
          Click a scenario to see ContextBridge prevent mistakes in real-time
        </p>
      </div>

      {/* Scenario Buttons */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        {scenarios.map((scenario) => (
          <button
            key={scenario.id}
            onClick={() => handleScenarioClick(scenario.id)}
            disabled={scenarioMutation.isPending}
            className={`p-6 rounded-xl border-2 transition-all hover:shadow-lg ${
              selectedScenario === scenario.id
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-blue-300'
            }`}
          >
            <scenario.icon 
              size={32} 
              className={`mb-3 text-${scenario.color}-500`} 
            />
            <h3 className="font-bold text-lg mb-1">{scenario.title}</h3>
            <p className="text-sm text-gray-600">{scenario.description}</p>
          </button>
        ))}
      </div>

      {/* Loading State */}
      <AnimatePresence>
        {scenarioMutation.isPending && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="bg-white rounded-xl p-8 shadow-lg text-center"
          >
            <Loader2 className="w-12 h-12 animate-spin text-blue-500 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">
              ContextBridge is analyzing...
            </h3>
            <p className="text-gray-600">
              Searching institutional memory for relevant context
            </p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Alert Display */}
      <AnimatePresence>
        {alert && !scenarioMutation.isPending && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="space-y-6"
          >
            {/* Headline */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className={`p-6 rounded-xl ${
                alert.alert_level === 'warning'
                  ? 'bg-red-50 border-2 border-red-500'
                  : alert.alert_level === 'expert_needed'
                  ? 'bg-green-50 border-2 border-green-500'
                  : 'bg-blue-50 border-2 border-blue-500'
              }`}
            >
              <div className="flex items-start space-x-4">
                {alert.alert_level === 'warning' && (
                  <AlertTriangle className="w-8 h-8 text-red-500 flex-shrink-0" />
                )}
                {alert.alert_level === 'expert_needed' && (
                  <Users className="w-8 h-8 text-green-500 flex-shrink-0" />
                )}
                {alert.alert_level === 'info' && (
                  <Info className="w-8 h-8 text-blue-500 flex-shrink-0" />
                )}
                <div className="flex-1">
                  <h2 className="text-2xl font-bold mb-2">{alert.headline}</h2>
                  <div className="flex items-center space-x-4 text-sm">
                    <span className="font-semibold">
                      Confidence: {alert.confidence_score}%
                    </span>
                    <span className="text-gray-600">
                      {alert.context_items.length} relevant items found
                    </span>
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Synthesized Insight */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
              className="bg-white rounded-xl p-6 shadow-lg"
            >
              <h3 className="text-lg font-bold mb-3 text-gray-900">
                📊 Synthesized Insight
              </h3>
              <p className="text-gray-700 leading-relaxed">
                {alert.synthesized_insight}
              </p>
            </motion.div>

            {/* Recommended Actions */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.6 }}
              className="bg-white rounded-xl p-6 shadow-lg"
            >
              <h3 className="text-lg font-bold mb-3 text-gray-900">
                ✅ Recommended Actions
              </h3>
              <ul className="space-y-2">
                {alert.recommended_actions.map((action, index) => (
                  <li key={index} className="flex items-start space-x-2">
                    <span className="text-blue-500 font-bold">•</span>
                    <span className="text-gray-700">{action}</span>
                  </li>
                ))}
              </ul>
            </motion.div>

            {/* Relevant People */}
            {alert.relevant_people.length > 0 && (
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.8 }}
                className="bg-white rounded-xl p-6 shadow-lg"
              >
                <h3 className="text-lg font-bold mb-3 text-gray-900">
                  👥 Talk To
                </h3>
                <div className="flex flex-wrap gap-2">
                  {alert.relevant_people.map((person, index) => (
                    <span
                      key={index}
                      className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full font-medium"
                    >
                      {person}
                    </span>
                  ))}
                </div>
              </motion.div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Demo;
```

### 6. Dashboard Page (`src/pages/Dashboard.tsx`)

```typescript
import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Database, CheckCircle, AlertTriangle, Users } from 'lucide-react';
import apiService from '../services/api';

const Dashboard: React.FC = () => {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['stats'],
    queryFn: () => apiService.getStats().then(res => res.data),
  });

  const statsCards = [
    {
      title: 'Total Knowledge Items',
      value: stats?.total_knowledge_items || 0,
      icon: Database,
      color: 'blue',
    },
    {
      title: 'Decisions Captured',
      value: stats?.items_by_type?.decision || 0,
      icon: CheckCircle,
      color: 'green',
    },
    {
      title: 'Failures Documented',
      value: stats?.items_by_type?.failure || 0,
      icon: AlertTriangle,
      color: 'red',
    },
    {
      title: 'Experts Mapped',
      value: Object.keys(stats?.items_by_type || {}).length,
      icon: Users,
      color: 'purple',
    },
  ];

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statsCards.map((card, index) => (
          <div key={index} className="bg-white rounded-xl p-6 shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <card.icon className={`w-8 h-8 text-${card.color}-500`} />
              <span className={`text-3xl font-bold text-${card.color}-600`}>
                {card.value}
              </span>
            </div>
            <h3 className="text-gray-600 font-medium">{card.title}</h3>
          </div>
        ))}
      </div>

      {/* Top Topics Chart */}
      <div className="bg-white rounded-xl p-6 shadow-lg">
        <h2 className="text-xl font-bold mb-4">Top Topics</h2>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={stats?.top_topics || []}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="topic" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" fill="#2471A3" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Dashboard;
```

---

## Tailwind Configuration

```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1B4F72',
        accent: '#2471A3',
        success: '#1E8449',
        warning: '#D35400',
        danger: '#C0392B',
      },
    },
  },
  plugins: [],
}
```

---

## App Router (`src/App.tsx`)

```typescript
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import Demo from './pages/Demo';
import Query from './pages/Query';
import Graph from './pages/Graph';
import KnowledgeBase from './pages/KnowledgeBase';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="demo" element={<Demo />} />
            <Route path="query" element={<Query />} />
            <Route path="graph" element={<Graph />} />
            <Route path="knowledge" element={<KnowledgeBase />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
```

---

## Running the Frontend

```bash
# Install dependencies
npm install

# Start development server
npm start
```

Frontend runs at: **http://localhost:3000**

---

## Integration with Backend

Make sure the FastAPI backend is running:

```bash
# In contextbridge directory
python main.py
```

Backend runs at: **http://localhost:8000**

---

## Key Features

### 1. **Demo Page** (Most Important)
- Three scenario buttons
- Animated loading state
- Dramatic alert reveal
- Slide-in animations
- Perfect for hackathon presentation

### 2. **Dashboard**
- Stats cards with icons
- Top topics bar chart
- Clean, professional design

### 3. **Query Page**
- Large search bar
- Suggested questions
- Result display with citations

### 4. **Knowledge Graph**
- D3.js force-directed graph
- Color-coded nodes
- Interactive node details
- Filter controls

### 5. **Knowledge Base**
- Searchable table
- Filterable by type, outcome, date
- Detail modal

---

## Hackathon Demo Flow

1. **Start Backend**: `python main.py`
2. **Start Frontend**: `npm start`
3. **Navigate to Demo page**
4. **Click "Scenario A"**
5. **Watch the magic happen!**
6. **Show the $500K warning**
7. **WOW the judges!** 🎉

---

## Next Steps

1. Build the remaining pages (Query, Graph, Knowledge Base)
2. Add more animations
3. Polish the UI
4. Test all scenarios
5. Prepare demo script

---

**Status**: 📋 **DESIGN COMPLETE**

All components, pages, and features are fully designed and ready to implement. The Demo page is the star of the show for the hackathon!
