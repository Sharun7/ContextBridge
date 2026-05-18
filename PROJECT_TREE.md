# ContextBridge - Complete Project Structure

## 📁 Project Tree

```
contextbridge/
│
├── 📄 Core Configuration Files
│   ├── .env                          # Environment variables (API keys, credentials)
│   ├── .env.example                  # Environment template with all options
│   ├── .dockerignore                 # Docker ignore patterns
│   ├── config.py                     # Application configuration (Settings class)
│   ├── main.py                       # FastAPI application entry point
│   ├── requirements.txt              # Python dependencies
│   ├── docker-compose.yml            # Docker orchestration
│   ├── Dockerfile                    # Backend Docker image
│   ├── startup.bat                   # Windows startup script
│   └── startup.sh                    # Mac/Linux startup script
│
├── 📚 Documentation Files
│   ├── README.md                     # Main project documentation
│   ├── WHATS_NEW.md                  # Overview of new features (START HERE!)
│   ├── REAL_INTEGRATION_GUIDE.md     # Complete setup guide (7000+ words)
│   ├── PRODUCTION_READY.md           # Technical details of changes
│   ├── PROJECT_COMPLETE_SUMMARY.md   # Original project summary
│   ├── PROJECT_TREE.md               # This file - project structure
│   ├── DOCKER_GUIDE.md               # Docker deployment guide
│   ├── QUICK_START.md                # Quick start guide
│   ├── QUICK_REFERENCE.md            # Quick reference
│   ├── FINAL_SUMMARY.md              # Final summary
│   ├── HACKATHON_DEMO_GUIDE.md       # Hackathon demo guide
│   └── SECTION_*.md                  # Section-by-section guides
│
├── 🧪 Test & Verification Scripts
│   ├── test_real_integrations.py     # Test all enterprise integrations
│   ├── test_api.py                   # Test API endpoints
│   ├── test_extraction.py            # Test knowledge extraction
│   ├── test_proactive.py             # Test proactive engine
│   ├── test_storage.py               # Test vector store & graph
│   ├── test_single_extraction.py     # Test single extraction
│   ├── verify_setup.py               # Verify setup
│   ├── check_data.py                 # Check data
│   └── visualize_graph.py            # Visualize knowledge graph
│
├── 📊 Database & Storage
│   ├── contextbridge.db              # SQLite database (metadata, audit logs)
│   └── chroma_db/                    # ChromaDB vector store (persistent)
│       ├── chroma.sqlite3            # ChromaDB metadata
│       └── 9f54a5ac-.../             # Vector embeddings
│
├── 📁 api/ - REST API Layer
│   ├── __init__.py
│   ├── routes.py                     # All API endpoints (13 endpoints)
│   │   ├── POST   /api/ingest                    # Ingest data (NEW: fetch from real sources)
│   │   ├── POST   /api/trigger/jira              # Trigger Jira analysis
│   │   ├── POST   /api/trigger/document          # Trigger document analysis
│   │   ├── POST   /api/query                     # Natural language query
│   │   ├── GET    /api/knowledge/search          # Search knowledge base
│   │   ├── GET    /api/knowledge/{id}            # Get knowledge item
│   │   ├── GET    /api/graph                     # Get knowledge graph (D3.js)
│   │   ├── GET    /api/experts                   # Find experts
│   │   ├── GET    /api/stats                     # System statistics
│   │   ├── POST   /api/demo/seed                 # Seed demo data
│   │   ├── POST   /api/demo/scenario/{A|B|C}     # Run demo scenarios
│   │   ├── GET    /api/health                    # Health check
│   │   └── GET    /                              # Root endpoint
│   │
│   └── models.py                     # Pydantic request/response models
│       ├── IngestRequest             # NEW: supports fetch_from_source
│       ├── IngestResponse
│       ├── JiraTriggerRequest
│       ├── DocumentTriggerRequest
│       ├── QueryRequest
│       ├── ProactiveAlertResponse
│       ├── KnowledgeItemResponse
│       ├── StatsResponse
│       ├── HealthResponse
│       └── ExpertResponse
│
├── 📁 ingestion/ - Data Connectors (✅ REAL API INTEGRATIONS)
│   ├── __init__.py
│   ├── slack_connector.py            # ✅ Real Slack API (slack-sdk)
│   │   ├── SlackConnector class
│   │   ├── fetch_messages()          # Fetch from channels
│   │   ├── get_channels()            # List all channels
│   │   └── Supports: Demo mode & Real API
│   │
│   ├── jira_connector.py             # ✅ Real Jira API (jira library)
│   │   ├── JiraConnector class
│   │   ├── fetch_tickets()           # Fetch tickets by project
│   │   ├── get_projects()            # List all projects
│   │   └── Supports: Demo mode & Real API
│   │
│   ├── drive_connector.py            # ✅ Real Google Drive API
│   │   ├── DriveConnector class
│   │   ├── fetch_documents()         # Fetch docs from folders
│   │   └── Supports: OAuth2 & Service Account
│   │
│   ├── email_connector.py            # ✅ Real Gmail API
│   │   ├── EmailConnector class
│   │   ├── fetch_emails()            # Fetch emails with queries
│   │   └── Supports: OAuth2 & Service Account
│   │
│   └── transcript_connector.py       # Meeting transcripts (placeholder)
│
├── 📁 processing/ - Knowledge Processing Layer
│   ├── __init__.py
│   ├── knowledge_extractor.py        # AI-powered knowledge extraction
│   │   ├── KnowledgeExtractor class
│   │   ├── extract_knowledge()       # Extract using Gemini 2.5 Flash
│   │   ├── Few-shot prompting
│   │   ├── Retry logic with exponential backoff
│   │   └── Importance scoring (1-10)
│   │
│   ├── vector_store.py               # ChromaDB vector database
│   │   ├── VectorStore class
│   │   ├── add_knowledge()           # Store with embeddings
│   │   ├── search_similar()          # Semantic similarity search
│   │   ├── search_by_topic()         # Topic-based search
│   │   └── get_stats()               # Statistics
│   │
│   └── graph_builder.py              # NetworkX knowledge graph
│       ├── GraphBuilder class
│       ├── build_graph()             # Build from knowledge items
│       ├── find_related_items()      # BFS traversal
│       ├── find_experts()            # Expert discovery
│       ├── get_chronological_history() # Timeline
│       └── export_for_d3()           # D3.js format
│
├── 📁 intelligence/ - AI Reasoning Layer (THE MAGIC!)
│   ├── __init__.py
│   ├── proactive_engine.py           # Proactive intelligence engine
│   │   ├── ProactiveEngine class
│   │   ├── handle_jira_trigger()     # Analyze Jira tickets
│   │   ├── handle_document_trigger() # Analyze documents
│   │   ├── handle_query_trigger()    # Answer questions
│   │   ├── Multi-factor confidence scoring (0-100)
│   │   ├── Alert level determination
│   │   └── Gemini synthesis
│   │
│   ├── query_engine.py               # Natural language queries
│   └── synthesizer.py                # AI synthesis
│
├── 📁 db/ - Database Layer
│   ├── __init__.py
│   └── database.py                   # SQLite ORM (SQLAlchemy)
│       ├── Database initialization
│       ├── Audit logging
│       └── Metadata storage
│
├── 📁 demo/ - Demo Data & Scenarios
│   ├── __init__.py
│   ├── seed_data.py                  # Generate realistic demo data
│   ├── demo_scenarios.py             # 3 pre-built scenarios
│   ├── check_data.py                 # Verify demo data
│   │
│   └── data/                         # Demo data files
│       ├── slack_messages.json       # 30 Slack messages (4 channels)
│       ├── jira_tickets.json         # 8 Jira tickets (3 projects)
│       ├── documents.json            # 8 documents (post-mortems, ADRs)
│       └── people.json               # 20 employees with expertise
│
├── 📁 frontend/ - React Frontend (TypeScript + Tailwind)
│   ├── package.json                  # Node.js dependencies
│   ├── package-lock.json
│   ├── tsconfig.json                 # TypeScript configuration
│   ├── tailwind.config.js            # Tailwind CSS configuration
│   ├── postcss.config.js             # PostCSS configuration
│   ├── Dockerfile                    # Frontend Docker image
│   ├── .dockerignore
│   ├── .gitignore
│   ├── README.md
│   │
│   ├── public/                       # Static assets
│   │   ├── index.html
│   │   ├── favicon.ico
│   │   ├── logo192.png
│   │   ├── logo512.png
│   │   ├── manifest.json
│   │   └── robots.txt
│   │
│   ├── build/                        # Production build output
│   │
│   └── src/                          # React source code
│       ├── index.tsx                 # Entry point
│       ├── index.css                 # Global styles
│       ├── App.tsx                   # Main app component
│       ├── App.test.tsx              # App tests
│       ├── setupTests.ts             # Test setup
│       ├── reportWebVitals.ts        # Performance monitoring
│       ├── react-app-env.d.ts        # TypeScript declarations
│       │
│       ├── components/               # Reusable components
│       │   └── layout/
│       │       ├── Layout.tsx        # Main layout wrapper
│       │       ├── Sidebar.tsx       # Navigation sidebar
│       │       └── TopBar.tsx        # Top navigation bar
│       │
│       ├── pages/                    # Page components
│       │   ├── Dashboard.tsx         # Main dashboard (stats, alerts)
│       │   ├── Demo.tsx              # Demo scenarios page
│       │   ├── Query.tsx             # Natural language query page
│       │   ├── Graph.tsx             # Knowledge graph visualization
│       │   └── KnowledgeBase.tsx     # Knowledge base browser
│       │
│       ├── services/                 # API services
│       │   └── api.ts                # API client (axios)
│       │
│       ├── theme/                    # Theme configuration
│       │   └── colors.ts             # Color palette
│       │
│       └── types/                    # TypeScript types
│           └── index.ts              # Type definitions
│
└── 📁 logs/                          # Application logs
    └── contextbridge.log             # Main log file
```

---

## 📊 File Statistics

### Backend (Python)
- **Total Python Files**: 25+
- **Lines of Code**: ~4,000+
- **Key Modules**:
  - API Layer: 700+ lines
  - Proactive Engine: 600+ lines
  - Graph Builder: 450+ lines
  - Vector Store: 350+ lines
  - Knowledge Extractor: 300+ lines

### Frontend (React/TypeScript)
- **Total TypeScript Files**: 15+
- **Components**: 8
- **Pages**: 5
- **Services**: 1

### Documentation
- **Total Documentation Files**: 15+
- **Total Words**: 20,000+
- **Comprehensive Guides**: 3

---

## 🔑 Key Files to Know

### Configuration
- **`.env`** - Your API keys and credentials (NEVER commit!)
- **`config.py`** - Application settings and configuration
- **`requirements.txt`** - Python dependencies

### Entry Points
- **`main.py`** - Backend server entry point
- **`frontend/src/index.tsx`** - Frontend entry point

### Core Logic
- **`api/routes.py`** - All API endpoints
- **`intelligence/proactive_engine.py`** - The "magic" proactive intelligence
- **`processing/knowledge_extractor.py`** - AI knowledge extraction

### Connectors (NEW!)
- **`ingestion/slack_connector.py`** - Real Slack integration
- **`ingestion/jira_connector.py`** - Real Jira integration
- **`ingestion/drive_connector.py`** - Real Google Drive integration
- **`ingestion/email_connector.py`** - Real Gmail integration

### Documentation (START HERE!)
- **`WHATS_NEW.md`** - Quick overview of new features
- **`REAL_INTEGRATION_GUIDE.md`** - Complete setup guide
- **`PRODUCTION_READY.md`** - Technical details

### Testing
- **`test_real_integrations.py`** - Test all integrations
- **`test_api.py`** - Test API endpoints

---

## 🚀 Quick Navigation

### Want to...
- **Get started?** → Read `WHATS_NEW.md`
- **Set up real integrations?** → Read `REAL_INTEGRATION_GUIDE.md`
- **Understand the changes?** → Read `PRODUCTION_READY.md`
- **Test connections?** → Run `test_real_integrations.py`
- **See API docs?** → Visit http://localhost:8000/docs
- **Configure credentials?** → Edit `.env` file
- **Add new connector?** → See `ingestion/` folder
- **Modify API?** → Edit `api/routes.py`
- **Change frontend?** → Edit `frontend/src/`

---

## 📦 Dependencies

### Backend (Python)
```
fastapi                    # Web framework
uvicorn                    # ASGI server
google-generativeai        # Gemini AI
chromadb                   # Vector database
networkx                   # Knowledge graph
sqlalchemy                 # Database ORM
pydantic                   # Data validation

# NEW: Enterprise Integrations
slack-sdk                  # Slack API
jira                       # Jira API
google-api-python-client   # Google Drive & Gmail
google-auth-oauthlib       # OAuth2
```

### Frontend (React)
```
react                      # UI framework
typescript                 # Type safety
tailwindcss                # CSS framework
recharts                   # Charts
d3                         # Graph visualization
framer-motion              # Animations
react-query                # Data fetching
react-router-dom           # Routing
axios                      # HTTP client
```

---

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     React Frontend                          │
│  (Dashboard, Demo, Query, Graph, Knowledge Base)            │
│                  http://localhost:3000                      │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/REST API
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                           │
│              http://localhost:8000                          │
│  (13 REST endpoints with OpenAPI docs)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┬─────────────┐
        ↓             ↓             ↓             ↓
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐
│  Ingestion   │ │Knowledge │ │  Vector  │ │  Proactive   │
│  Connectors  │ │Extractor │ │  Store   │ │   Engine     │
│  (NEW!)      │ │ (Gemini) │ │(ChromaDB)│ │  (THE MAGIC) │
│              │ │          │ │          │ │              │
│ • Slack      │ │ • Extract│ │ • Search │ │ • Analyze    │
│ • Jira       │ │ • Score  │ │ • Store  │ │ • Alert      │
│ • Drive      │ │ • Retry  │ │ • Stats  │ │ • Synthesize │
│ • Gmail      │ │          │ │          │ │              │
└──────────────┘ └──────────┘ └──────────┘ └──────────────┘
        │             │             │             │
        └─────────────┴─────────────┴─────────────┘
                      │
                      ↓
        ┌─────────────────────────────┐
        │    Knowledge Graph          │
        │      (NetworkX)             │
        │                             │
        │  • People → Topics          │
        │  • Items → Related Items    │
        │  • Teams → Projects         │
        └─────────────────────────────┘
```

---

## 🎉 Summary

This is a **complete, production-ready** AI-powered institutional memory system with:

- ✅ **Real enterprise integrations** (Slack, Jira, Google Drive, Gmail)
- ✅ **AI-powered knowledge extraction** (Google Gemini 2.5 Flash)
- ✅ **Vector search** (ChromaDB)
- ✅ **Knowledge graph** (NetworkX)
- ✅ **Proactive intelligence** (The "magic" feature)
- ✅ **REST API** (13 endpoints with OpenAPI docs)
- ✅ **React frontend** (TypeScript + Tailwind CSS)
- ✅ **Comprehensive documentation** (15+ guides)
- ✅ **Test suite** (Verify all integrations)
- ✅ **Docker support** (One-command deployment)

**Total Project Size**: ~4,000+ lines of Python, 15+ documentation files, complete frontend

---

**ContextBridge** - Your enterprise's institutional memory, now production-ready! 🚀
