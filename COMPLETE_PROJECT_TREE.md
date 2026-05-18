# ContextBridge - Complete Project Tree

## 📁 Full Project Structure (Source Files Only)

```
contextbridge/
│
├── 📄 Root Configuration Files
│   ├── .dockerignore                    # Docker ignore rules
│   ├── .env                            # Environment variables (gitignored)
│   ├── .env.example                    # Environment template
│   ├── .gitignore                      # Git ignore rules
│   ├── config.py                       # Application configuration
│   ├── docker-compose.yml              # Multi-container orchestration
│   ├── Dockerfile                      # Backend container definition
│   ├── main.py                         # FastAPI application entry point
│   ├── requirements.txt                # Python dependencies
│   ├── startup.bat                     # Windows startup script
│   └── startup.sh                      # Linux/Mac startup script
│
├── 📂 api/                             # REST API Layer
│   ├── __init__.py
│   ├── models.py                       # Pydantic data models
│   ├── routes.py                       # FastAPI route handlers
│   └── __pycache__/                    # Python bytecode cache
│       ├── __init__.cpython-311.pyc
│       ├── __init__.cpython-312.pyc
│       ├── models.cpython-311.pyc
│       ├── models.cpython-312.pyc
│       ├── routes.cpython-311.pyc
│       └── routes.cpython-312.pyc
│
├── 📂 db/                              # Database Layer
│   ├── __init__.py
│   ├── database.py                     # SQLite operations
│   └── __pycache__/
│       ├── __init__.cpython-311.pyc
│       ├── __init__.cpython-312.pyc
│       ├── database.cpython-311.pyc
│       └── database.cpython-312.pyc
│
├── 📂 demo/                            # Demo & Testing
│   ├── __init__.py
│   ├── check_data.py                   # Data verification
│   ├── demo_scenarios.py               # Demo runner
│   ├── seed_data.py                    # Database seeding
│   └── 📂 data/                        # Sample data
│       ├── documents.json              # Sample documents
│       ├── jira_tickets.json           # Sample Jira tickets
│       ├── people.json                 # Sample people data
│       └── slack_messages.json         # Sample Slack messages
│
├── 📂 ingestion/                       # Data Ingestion Connectors
│   ├── __init__.py
│   ├── drive_connector.py              # Google Drive integration
│   ├── email_connector.py              # Email integration
│   ├── jira_connector.py               # Jira integration
│   ├── slack_connector.py              # Slack integration
│   ├── transcript_connector.py         # Meeting transcripts
│   └── __pycache__/
│       ├── __init__.cpython-311.pyc
│       ├── drive_connector.cpython-311.pyc
│       ├── email_connector.cpython-311.pyc
│       ├── jira_connector.cpython-311.pyc
│       └── slack_connector.cpython-311.pyc
│
├── 📂 intelligence/                    # AI Intelligence Layer
│   ├── __init__.py
│   ├── proactive_engine.py             # Proactive insights
│   ├── query_engine.py                 # Query processing
│   ├── synthesizer.py                  # Context synthesis
│   └── __pycache__/
│       ├── __init__.cpython-311.pyc
│       ├── __init__.cpython-312.pyc
│       ├── proactive_engine.cpython-311.pyc
│       ├── proactive_engine.cpython-312.pyc
│       ├── query_engine.cpython-312.pyc
│       └── synthesizer.cpython-312.pyc
│
├── 📂 processing/                      # Data Processing Layer
│   ├── __init__.py
│   ├── graph_builder.py                # Knowledge graph construction
│   ├── knowledge_extractor.py          # Entity extraction
│   ├── vector_store.py                 # ChromaDB operations
│   └── __pycache__/
│       ├── __init__.cpython-311.pyc
│       ├── __init__.cpython-312.pyc
│       ├── graph_builder.cpython-311.pyc
│       ├── graph_builder.cpython-312.pyc
│       ├── knowledge_extractor.cpython-311.pyc
│       ├── knowledge_extractor.cpython-312.pyc
│       ├── vector_store.cpython-311.pyc
│       └── vector_store.cpython-312.pyc
│
├── 📂 frontend/                        # React Frontend Application
│   ├── .dockerignore
│   ├── .gitignore
│   ├── Dockerfile                      # Frontend container
│   ├── package.json                    # NPM dependencies
│   ├── package-lock.json               # NPM lock file
│   ├── postcss.config.js               # PostCSS config
│   ├── serve-build.js                  # Production server
│   ├── tailwind.config.js              # Tailwind CSS config
│   ├── tsconfig.json                   # TypeScript config
│   ├── README.md                       # Frontend docs
│   │
│   ├── 📂 public/                      # Static Assets
│   │   ├── index.html                  # HTML template
│   │   ├── favicon.ico                 # Favicon
│   │   ├── logo192.png                 # Logo 192x192
│   │   ├── logo512.png                 # Logo 512x512
│   │   ├── manifest.json               # PWA manifest
│   │   └── robots.txt                  # SEO robots file
│   │
│   ├── 📂 src/                         # Source Code
│   │   ├── App.tsx                     # Main App component
│   │   ├── App.test.tsx                # App tests
│   │   ├── index.tsx                   # Entry point
│   │   ├── index.css                   # Global styles
│   │   ├── logo.svg                    # Logo asset
│   │   ├── react-app-env.d.ts          # React types
│   │   ├── reportWebVitals.ts          # Performance
│   │   ├── setupTests.ts               # Test setup
│   │   │
│   │   ├── 📂 components/              # React Components
│   │   │   └── 📂 layout/
│   │   │       ├── Layout.tsx          # Main layout
│   │   │       ├── Sidebar.tsx         # Navigation sidebar
│   │   │       └── TopBar.tsx          # Top bar
│   │   │
│   │   ├── 📂 pages/                   # Page Components
│   │   │   ├── Dashboard.tsx           # Dashboard page
│   │   │   ├── Demo.tsx                # Demo page
│   │   │   ├── Graph.tsx               # Graph visualization
│   │   │   ├── KnowledgeBase.tsx       # Knowledge base
│   │   │   └── Query.tsx               # Query interface
│   │   │
│   │   ├── 📂 services/                # API Services
│   │   │   └── api.ts                  # API client
│   │   │
│   │   ├── 📂 theme/                   # Theme Config
│   │   │   └── colors.ts               # Color palette
│   │   │
│   │   └── 📂 types/                   # TypeScript Types
│   │       └── index.ts                # Type definitions
│   │
│   ├── 📂 build/                       # Production build (gitignored)
│   │   ├── index.html
│   │   ├── asset-manifest.json
│   │   ├── favicon.ico
│   │   ├── logo192.png
│   │   ├── logo512.png
│   │   ├── manifest.json
│   │   ├── robots.txt
│   │   └── 📂 static/
│   │       ├── 📂 css/
│   │       ├── 📂 js/
│   │       └── 📂 media/
│   │
│   └── 📂 node_modules/                # NPM packages (gitignored)
│       └── [1000+ packages]
│
├── 📂 chroma_db/                       # Vector Database (gitignored)
│   ├── chroma.sqlite3
│   └── 📂 9f54a5ac-9004-4adc-b190-1a0586d06b0d/
│       ├── data_level0.bin
│       ├── header.bin
│       ├── length.bin
│       └── link_lists.bin
│
├── 📂 logs/                            # Application Logs (gitignored)
│
├── 📂 .venv/                           # Python Virtual Env (gitignored)
│   ├── pyvenv.cfg
│   ├── 📂 Include/
│   ├── 📂 Lib/
│   │   └── 📂 site-packages/
│   └── 📂 Scripts/
│       ├── activate
│       ├── activate.bat
│       ├── Activate.ps1
│       ├── deactivate.bat
│       ├── python.exe
│       └── pip.exe
│
├── 📂 __pycache__/                     # Python Cache (gitignored)
│   ├── config.cpython-311.pyc
│   ├── main.cpython-311.pyc
│   └── main.cpython-312.pyc
│
├── 📂 .git/                            # Git Repository
│   ├── config
│   ├── HEAD
│   ├── index
│   ├── COMMIT_EDITMSG
│   ├── 📂 hooks/
│   ├── 📂 info/
│   ├── 📂 logs/
│   ├── 📂 objects/
│   └── 📂 refs/
│
├── 📄 Database Files (gitignored)
│   ├── contextbridge.db                # SQLite database
│   └── runtime_knowledge_store.json    # Runtime knowledge
│
├── 📄 Runtime Files (gitignored)
│   └── local_runtime_api.js            # Local runtime API
│
├── 📄 Test Scripts
│   ├── list_models.py                  # List Ollama models
│   ├── test_api.py                     # API tests
│   ├── test_extraction.py              # Extraction tests
│   ├── test_proactive.py               # Proactive tests
│   ├── test_real_integrations.py       # Integration tests
│   ├── test_single_extraction.py       # Single extraction
│   ├── test_storage.py                 # Storage tests
│   ├── verify_setup.py                 # Setup verification
│   └── visualize_graph.py              # Graph visualization
│
└── 📄 Documentation Files (24 files)
    ├── README.md                       # Main documentation
    ├── QUICK_START.md                  # Quick start guide
    ├── QUICK_REFERENCE.md              # Quick reference
    ├── DOCKER_GUIDE.md                 # Docker deployment
    ├── HACKATHON_DEMO_GUIDE.md         # Demo guide
    ├── PRODUCTION_READY.md             # Production guide
    ├── REAL_INTEGRATION_GUIDE.md       # Integration setup
    ├── TROUBLESHOOTING.md              # Troubleshooting
    ├── WHATS_NEW.md                    # What's new
    ├── PROJECT_COMPLETE_SUMMARY.md     # Project summary
    ├── PROJECT_STRUCTURE.md            # Architecture docs
    ├── PROJECT_TREE.md                 # Project tree
    ├── COMPLETE_PROJECT_TREE.md        # This file
    ├── GIT_PUSH_INSTRUCTIONS.md        # Git push guide
    ├── BUG_FIXES_COMPLETE.md           # Bug fixes log
    ├── FINAL_FIX_COMPLETE.md           # Final fixes
    ├── FINAL_SUMMARY.md                # Final summary
    ├── SESSION_SUMMARY.md              # Session summary
    ├── SYSTEM_VERIFICATION_REPORT.md   # Verification report
    ├── SECTION_2_COMPLETE.md           # Section 2 docs
    ├── SECTION_3_COMPLETE.md           # Section 3 docs
    ├── SECTION_4_COMPLETE.md           # Section 4 docs
    ├── SECTION_5_COMPLETE.md           # Section 5 docs
    ├── SECTION_6_COMPLETE.md           # Section 6 docs
    ├── SECTION_7_COMPLETE.md           # Section 7 docs
    ├── SECTION_7_FRONTEND_GUIDE.md     # Frontend guide
    └── SECTION_8_COMPLETE.md           # Section 8 docs
```

## 📊 Project Statistics

### File Counts
- **Python Files**: 25 source files
- **TypeScript/TSX Files**: 15 files
- **Configuration Files**: 12 files
- **Documentation Files**: 24 markdown files
- **Test Scripts**: 9 files
- **Total Source Files**: ~85 files (excluding dependencies)

### Directory Structure
- **Backend Modules**: 6 directories (api, db, demo, ingestion, intelligence, processing)
- **Frontend Modules**: 5 directories (components, pages, services, theme, types)
- **Configuration**: Root level
- **Documentation**: Root level
- **Tests**: Root level

### Lines of Code (Approximate)
- **Python Backend**: ~5,000 lines
- **TypeScript Frontend**: ~3,000 lines
- **Configuration**: ~500 lines
- **Documentation**: ~15,000 lines
- **Total**: ~23,500 lines

### Dependencies
- **Python Packages**: 15+ (FastAPI, ChromaDB, SQLAlchemy, etc.)
- **NPM Packages**: 1000+ (React, TypeScript, Tailwind, D3, etc.)

## 🏗️ Architecture Layers

### Backend (Python)
```
main.py
   ↓
api/ (FastAPI routes)
   ↓
intelligence/ (AI processing)
   ↓
processing/ (Knowledge extraction)
   ↓
db/ + chroma_db/ (Storage)
   ↑
ingestion/ (Data sources)
```

### Frontend (React/TypeScript)
```
index.tsx
   ↓
App.tsx
   ↓
Layout (components/layout/)
   ↓
Pages (pages/)
   ↓
Services (services/api.ts)
   ↓
Backend API
```

## 🔧 Key Technologies

### Backend Stack
- **Framework**: FastAPI
- **Database**: SQLite + ChromaDB
- **AI/ML**: Ollama (local LLM)
- **Language**: Python 3.11+

### Frontend Stack
- **Framework**: React 18
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State**: Redux Toolkit
- **Routing**: React Router
- **Visualization**: D3.js, Recharts
- **Animation**: Framer Motion

### DevOps
- **Containerization**: Docker + Docker Compose
- **Version Control**: Git
- **Package Management**: pip (Python), npm (Node.js)

## 📦 Deployment Structure

### Development
```
Backend:  http://localhost:8000
Frontend: http://localhost:3000
```

### Production (Docker)
```
Backend Container:  Port 8000
Frontend Container: Port 80
ChromaDB: Internal network
```

## 🎯 Entry Points

### Backend
- **Main**: `main.py`
- **API**: `api/routes.py`
- **Config**: `config.py`

### Frontend
- **Entry**: `frontend/src/index.tsx`
- **App**: `frontend/src/App.tsx`
- **Config**: `frontend/tsconfig.json`

### Scripts
- **Startup**: `startup.bat` (Windows) or `startup.sh` (Linux/Mac)
- **Demo**: `demo/demo_scenarios.py`
- **Tests**: `test_*.py` files

## 🔐 Security & Configuration

### Environment Variables (.env)
- API keys
- Database URLs
- Ollama configuration
- Integration credentials

### Ignored Files (.gitignore)
- `__pycache__/`
- `.venv/`
- `node_modules/`
- `*.db`, `*.sqlite3`
- `chroma_db/`
- `logs/`
- `.env`
- `build/`

## 📈 Growth Potential

### Scalability
- Microservices architecture ready
- Docker containerization
- Horizontal scaling capable
- API-first design

### Extensibility
- Plugin-based connectors
- Modular intelligence layer
- Customizable frontend
- Open API specification

---

**Repository**: https://github.com/Sharun7/ContextBridge  
**Version**: 1.0.0  
**Last Updated**: 2026-05-18  
**Status**: Production Ready ✅
