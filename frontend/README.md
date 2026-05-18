# ContextBridge Frontend

React TypeScript dashboard for the ContextBridge institutional memory agent.

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ installed
- Backend running at `http://localhost:8000`

### Installation

```bash
# Install dependencies (already done)
npm install

# Start development server
npm start
```

The app will open at **http://localhost:3000**

## 📁 Project Structure

```
src/
├── components/
│   └── layout/
│       ├── Layout.tsx       # Main layout wrapper
│       ├── Sidebar.tsx      # Navigation sidebar
│       └── TopBar.tsx       # Top bar with stats
├── pages/
│   ├── Dashboard.tsx        # Home page with stats
│   ├── Demo.tsx            # ⭐ DEMO PAGE (Most Important)
│   ├── Query.tsx           # Natural language queries
│   ├── Graph.tsx           # D3.js knowledge graph
│   └── KnowledgeBase.tsx   # Searchable knowledge table
├── services/
│   └── api.ts              # API service layer
├── types/
│   └── index.ts            # TypeScript interfaces
├── theme/
│   └── colors.ts           # Color scheme
├── App.tsx                 # Main app with routing
└── index.tsx               # Entry point
```

## 🎨 Pages

### 1. Dashboard (Home)
- **Route**: `/`
- **Features**:
  - 4 stats cards (Total Items, Decisions, Failures, Lessons)
  - Top topics bar chart
  - Items by type and outcome

### 2. Demo Page ⭐ (MOST IMPORTANT)
- **Route**: `/demo`
- **Features**:
  - 3 scenario buttons (A, B, C)
  - Animated loading state
  - Dramatic alert reveal with slide-in animations
  - Perfect for hackathon presentation
- **Scenarios**:
  - **A**: Prevent a Mistake (PostgreSQL migration warning)
  - **B**: Answer Why (React vs Vue decision)
  - **C**: Find Expert (Migration best practices)

### 3. Query Page
- **Route**: `/query`
- **Features**:
  - Large search bar
  - Suggested questions as chips
  - Natural language query results
  - Source citations

### 4. Knowledge Graph
- **Route**: `/graph`
- **Features**:
  - D3.js force-directed graph
  - Interactive node dragging
  - Color-coded by type (blue=knowledge, green=person, orange=topic)
  - Node details panel
  - Topic filtering

### 5. Knowledge Base
- **Route**: `/knowledge`
- **Features**:
  - Searchable knowledge items
  - Filter by type, outcome
  - Click to see full details in modal
  - Importance scores and tags

## 🎨 Color Scheme

```typescript
Primary:    #1B4F72  // Deep blue
Accent:     #2471A3  // Medium blue
Success:    #1E8449  // Green
Warning:    #D35400  // Orange
Danger:     #C0392B  // Red
Background: #F4F6F9  // Light gray
Card:       #FFFFFF  // White
```

## 🔌 API Integration

All API calls go through `src/services/api.ts`:

```typescript
import apiService from './services/api';

// Get stats
const stats = await apiService.getStats();

// Run demo scenario
const alert = await apiService.runScenario('A');

// Query
const result = await apiService.query('Why did we choose React?');

// Search knowledge
const items = await apiService.searchKnowledge({ q: 'migration' });

// Get graph
const graph = await apiService.getGraph();
```

## 🎭 Hackathon Demo Flow

1. **Start Backend**: `cd .. && python main.py`
2. **Start Frontend**: `npm start`
3. **Navigate to Demo page** (`/demo`)
4. **Click "Scenario A"**
5. **Watch the magic!** 🎉
   - Loading animation
   - Alert appears with $500K PostgreSQL warning
   - Synthesized insight from Gemini
   - Recommended actions
   - Relevant experts

## 🛠️ Technologies

- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **React Router** for navigation
- **React Query** for data fetching
- **Framer Motion** for animations
- **D3.js** for knowledge graph
- **Recharts** for charts
- **Lucide React** for icons
- **Axios** for API calls

## 📦 Available Scripts

```bash
# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Eject (not recommended)
npm run eject
```

## 🐛 Troubleshooting

### Backend not responding
- Make sure backend is running: `cd .. && python main.py`
- Check backend is at `http://localhost:8000`
- Verify CORS is enabled in backend

### No data showing
- Seed demo data: `curl -X POST http://localhost:8000/api/demo/seed`
- Or use the backend: `python demo/seed_data.py`

### Graph not rendering
- Check browser console for D3.js errors
- Make sure graph data has nodes and links
- Try refreshing the page

## 🎯 Key Features for Judges

1. **Proactive Intelligence** - Demo page shows real-time mistake prevention
2. **Beautiful UI** - Modern, professional design with animations
3. **Interactive Graph** - D3.js visualization of knowledge relationships
4. **Natural Language** - Query page for asking questions
5. **Comprehensive** - Full knowledge base with search and filters

## 📝 Notes

- The **Demo page** is the star of the show for the hackathon
- All animations are smooth and professional
- Color scheme matches the brand (deep blue theme)
- Responsive design works on all screen sizes
- Real-time data updates every 30 seconds

## 🏆 Hackathon Presentation Tips

1. Start with the **Demo page**
2. Click **Scenario A** first (most dramatic - $500K failure)
3. Highlight the **confidence score** (100%)
4. Show the **synthesized insight** from Gemini
5. Point out the **recommended actions**
6. Show the **relevant experts** to contact
7. Then show **Scenario B** (Answer Why)
8. Finish with the **Knowledge Graph** for visual impact

---

**Built for TechEx Hackathon 2026 - Track 4: Data & Intelligence**
