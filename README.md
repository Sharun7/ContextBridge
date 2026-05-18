# ContextBridge

**AI-Powered Institutional Memory Agent for Enterprises**

> Never repeat the past. Always move forward with context.

---

## 🎯 What is ContextBridge?

ContextBridge is an AI-powered system that captures, organizes, and proactively surfaces your organization's institutional memory. It prevents repeated mistakes, answers "why" questions, and finds experts—automatically.

**Key Features**:
- ✅ **Real Enterprise Integrations** - Connect to Slack, Jira, Google Drive, Gmail
- ✅ **AI-Powered Knowledge Extraction** - Google Gemini 2.5 Flash
- ✅ **Proactive Intelligence** - Surfaces relevant context BEFORE mistakes happen
- ✅ **Knowledge Graph** - Connects people, topics, and decisions
- ✅ **Semantic Search** - Find relevant information instantly

**Built for**: TechEx Hackathon 2026 | Track 4: Data & Intelligence  
**Powered by**: Google Gemini 2.5 Flash

---

## 🚀 Quick Start

### Option 1: Demo Mode (Quick Test)

**Prerequisites**: Docker Desktop installed and running

```bash
# Windows
startup.bat

# Mac/Linux
chmod +x startup.sh && ./startup.sh
```

**Access the app**:
- 🎯 Demo Page: http://localhost:3000/demo
- 📊 Dashboard: http://localhost:3000
- 📚 API Docs: http://localhost:8000/docs

### Option 2: Production Mode (Real Integrations)

**Prerequisites**:
- Python 3.11+
- Node.js 16+
- Google Gemini API Key ([Get it here](https://aistudio.google.com/apikey))
- Enterprise API credentials (Slack, Jira, Google, etc.)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env and add your API keys

# 3. Set DEMO_MODE=false in .env
DEMO_MODE=false

# 4. Start the server
python main.py
```

**See [REAL_INTEGRATION_GUIDE.md](REAL_INTEGRATION_GUIDE.md) for detailed setup instructions.**

---

## 🔌 Enterprise Integrations

ContextBridge supports **REAL** connections to your enterprise data sources:

### Supported Integrations

| Source | Status | What It Captures |
|--------|--------|------------------|
| **Slack** | ✅ Ready | Team conversations, decisions, discussions |
| **Jira** | ✅ Ready | Tickets, issues, project history |
| **Google Drive** | ✅ Ready | Documents, post-mortems, ADRs |
| **Gmail** | ✅ Ready | Email communications, threads |
| **Meeting Transcripts** | 🔄 Coming Soon | Video call transcripts |

### How It Works

1. **Connect** - Provide API credentials for your enterprise tools
2. **Ingest** - ContextBridge fetches and processes your data
3. **Extract** - AI extracts decisions, failures, lessons, and expertise
4. **Surface** - Proactively warns about past mistakes and finds experts

---

## 📊 API Endpoints

### Core Endpoints

```bash
# Ingest from real Slack
POST /api/ingest
{
  "source_type": "slack",
  "fetch_from_source": true,
  "channel": "engineering",
  "limit": 100
}

# Ingest from real Jira
POST /api/ingest
{
  "source_type": "jira",
  "fetch_from_source": true,
  "project": "ENG",
  "limit": 50
}

# Proactive analysis
POST /api/trigger/jira
{
  "ticket_title": "Migrate to PostgreSQL",
  "ticket_description": "Planning database migration..."
}

# Natural language query
POST /api/query
{
  "question": "Why did the 2023 PostgreSQL migration fail?"
}
```

Full API documentation: http://localhost:8000/docs

---

## 📁 Project Structure

```
contextbridge/
├── main.py                    # FastAPI application entry point
├── config.py                  # Configuration and settings
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (your API key)
│
├── ingestion/                 # Data connectors
│   ├── slack_connector.py     # Slack messages
│   ├── jira_connector.py      # Jira tickets
│   ├── drive_connector.py     # Google Drive documents
│   ├── email_connector.py     # Gmail emails
│   └── transcript_connector.py # Meeting transcripts
│
├── processing/                # Knowledge processing
│   ├── knowledge_extractor.py # Gemini-powered extraction
│   ├── graph_builder.py       # Knowledge graph (NetworkX)
│   └── vector_store.py        # Vector embeddings (ChromaDB)
│
├── intelligence/              # AI reasoning layer
│   ├── proactive_engine.py    # Proactive context surfacing
│   ├── query_engine.py        # Natural language queries
│   └── synthesizer.py         # Gemini synthesis
│
├── api/                       # REST API
│   ├── routes.py              # All endpoints
│   └── models.py              # Pydantic models
│
├── db/                        # Database
│   └── database.py            # SQLite for audit logs
│
└── demo/                      # Demo data and scenarios
    ├── seed_data.py           # Generate demo data
    └── demo_scenarios.py      # Pre-built scenarios
```

---

## 🎬 Demo Scenarios

ContextBridge includes 3 pre-built demo scenarios for the hackathon:

### Scenario A: The Mistake Prevented 🚨
**Trigger**: Engineer creates Jira ticket for PostgreSQL migration  
**Response**: Surfaces 2023 failed attempt with documentation and expert contact

### Scenario B: The Question Answered 💡
**Trigger**: "Why do we use React instead of Vue?"  
**Response**: Surfaces 2022 architecture debate with decision rationale

### Scenario C: The Expert Found 🧠
**Trigger**: "Who has database migration experience?"  
**Response**: Returns experts with evidence of past work

Run demo scenarios:
```bash
python demo/demo_scenarios.py
```

---

## 🔧 Configuration

Edit `.env` file:

```env
# Required
GEMINI_API_KEY=your_api_key_here

# Optional (defaults shown)
CHROMA_PERSIST_DIR=./chroma_db
DATABASE_URL=sqlite:///./contextbridge.db
DEMO_MODE=true
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO
```

---

## 📊 API Endpoints

### Core Endpoints

- `POST /api/ingest` - Ingest data from enterprise sources
- `POST /api/trigger/jira` - Trigger proactive analysis for Jira ticket
- `POST /api/trigger/document` - Trigger proactive analysis for document
- `POST /api/query` - Natural language query over knowledge base

### Knowledge Endpoints

- `GET /api/knowledge/search` - Search knowledge base
- `GET /api/knowledge/{id}` - Get specific knowledge item
- `GET /api/graph` - Get knowledge graph (D3.js format)
- `GET /api/experts?topic=...` - Find experts on a topic
- `GET /api/stats` - Get system statistics

### Demo Endpoints

- `POST /api/demo/seed` - Load demo data
- `POST /api/demo/scenario/{A|B|C}` - Run demo scenario

### System Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check

Full API documentation: http://localhost:8000/docs

---

## 🏗️ Architecture

### 5-Layer System

1. **Passive Ingestion Layer**: Connects to Slack, Jira, Drive, Email, Meetings
2. **Knowledge Processing Layer**: Gemini extracts decisions, failures, lessons
3. **Knowledge Storage Layer**: ChromaDB (vectors) + NetworkX (graph) + SQLite (metadata)
4. **Intelligence & Reasoning Layer**: Proactive engine + Query engine + Synthesizer
5. **Experience Layer**: REST API + Web Dashboard (React)

### Security & Governance

- Role-based access control
- Data encryption (in transit & at rest)
- Source-level permissions
- Audit logging (who, what, when)
- PII detection & redaction

---

## 🧪 Development

### Generate Demo Data

```bash
python demo/seed_data.py
```

### Run Tests

```bash
# TODO: Add tests
pytest
```

### View Demo Scenarios

```bash
python demo/demo_scenarios.py
```

---

## 📦 Dependencies

- **FastAPI**: REST API framework
- **ChromaDB**: Vector database for semantic search
- **Google Generative AI**: Gemini 1.5 Pro for knowledge extraction
- **LangChain**: LLM orchestration
- **NetworkX**: Knowledge graph
- **SQLAlchemy**: Database ORM
- **Pydantic**: Data validation

See `requirements.txt` for full list.

---

## 🎓 Team

**Team NexaCore**  
TechEx Hackathon 2026 | Track 4: Data & Intelligence

---

## 📝 License

Built for TechEx Hackathon 2026

---

## 🔗 Links

- **Gemini API**: https://aistudio.google.com/apikey
- **TechEx Hackathon**: https://lablab.ai/ai-hackathons/techex-intelligent-enterprise-solutions-hackathon

---

**ContextBridge** — Because your company's most valuable asset is what it already knows.
