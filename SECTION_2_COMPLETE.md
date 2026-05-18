# ✅ Section 2 Complete: Demo Data Generator

## What We Built

A complete, realistic enterprise demo data generator for **NovaTech Solutions** - a fictional 500-person software company.

## Generated Data Files

### 📁 demo/data/people.json (20 employees)
- **Sarah Chen** - Senior Backend Engineer (led failed PostgreSQL migration)
- **James Wilson** - Principal Architect (led React decision)
- **Emily Rodriguez** - Product Manager (led APAC expansion)
- **Alex Kumar** - Staff Engineer (led Stripe evaluation)
- **Maria Garcia** - DevOps Lead (infrastructure expert)
- Plus 15 more team members with realistic roles and expertise

### 💬 demo/data/slack_messages.json (30 messages)
Realistic conversations across 4 channels:
- **#engineering** - PostgreSQL migration failure, microservices success
- **#architecture** - React vs Vue debate and decision
- **#product** - APAC expansion planning and pause
- **#incidents** - Production incident reports

### 🎫 demo/data/jira_tickets.json (8 tickets)
- **ENG-1234** - Failed PostgreSQL migration (with detailed comments)
- **ENG-1235** - Post-mortem for the failure
- **ARCH-045** - ADR: Standardize on React
- **PROD-567** - APAC expansion (on hold)
- **ENG-890** - Successful microservices refactoring
- **ENG-1100** - Stripe vs Braintree evaluation
- Plus monitoring and testing tickets

### 📄 demo/data/documents.json (8 documents)
- **ADR-015** - Architecture Decision Record: Why React was chosen (2022)
- **DOC-089** - Post-mortem: PostgreSQL Migration Failure (Q3 2023)
  - Root cause: Connection pool misconfiguration
  - Cost: $500K, 3 months wasted
  - Detailed lessons learned
- **DOC-112** - APAC Expansion Technical Requirements (2024)
  - Compliance requirements for Singapore, Japan, Australia
  - Why it was paused
- **DOC-095** - Stripe vs Braintree vendor evaluation
  - Detailed comparison with ratings
  - Why Stripe won
- **DOC-001** - Team Expertise Directory
- Plus architecture guides and best practices

## Demo Scenarios

### 🚨 Scenario A: The Mistake Prevented
**Trigger**: Engineer creates Jira ticket "Migrate primary database from MySQL to PostgreSQL"  
**Response**: ContextBridge surfaces the 2023 failure, Sarah Chen's post-mortem, and warns about connection pooling issues  
**Value**: Prevents repeating a $500K mistake

### 💡 Scenario B: The Question Answered
**Trigger**: Query "Why do we use React instead of Vue for our frontend?"  
**Response**: Surfaces the 2022 architecture debate, ADR-015, and 5 specific reasons  
**Value**: Instant access to 2-year-old decision rationale

### 🧠 Scenario C: The Expert Found
**Trigger**: Query "Who in our team has experience with database migrations?"  
**Response**: Returns Sarah Chen, Maria Garcia, and Priya Patel with evidence  
**Value**: Finds the right experts in seconds

## Key Story Arcs

### 1. The PostgreSQL Migration Failure (2023)
- **What happened**: Sarah Chen led a migration from MySQL to PostgreSQL
- **Why it failed**: pgBouncer connection pool set to 100 (should be 500+)
- **Impact**: 45-minute production outage, $500K cost, 3 months wasted
- **Lesson**: Always load test with production traffic before migrations
- **Evidence**: Jira ENG-1234, DOC-089, Slack #engineering, #incidents

### 2. The React Decision (2022)
- **What happened**: Team debated React vs Vue for frontend standardization
- **Why React won**: Better TypeScript, larger ecosystem, easier hiring, React Native
- **Who decided**: James Wilson (Principal Architect)
- **Evidence**: ADR-015, Slack #architecture, Jira ARCH-045

### 3. The APAC Expansion Pause (2024)
- **What happened**: Planned expansion to Singapore, Japan, Australia
- **Why paused**: Compliance requirements too complex (PDPA, APPI, Privacy Act)
- **Impact**: Need specialized legal and engineering talent
- **Evidence**: DOC-112, Slack #product, Jira PROD-567

### 4. The Microservices Success (2022)
- **What happened**: Broke monolith into Auth, User, Payment, Notification services
- **Result**: 40% performance improvement, 30min → 5min deployment time
- **Who led**: David Thompson
- **Evidence**: Jira ENG-890, Slack #engineering

### 5. The Stripe Choice (2023)
- **What happened**: Evaluated Stripe vs Braintree for payment processing
- **Why Stripe won**: Better API, documentation, fraud detection, webhooks
- **Who decided**: Alex Kumar
- **Evidence**: DOC-095, Jira ENG-1100, Slack #engineering

## How to Use

### Generate Demo Data
```bash
cd contextbridge
python demo/seed_data.py
```

### View Demo Scenarios
```bash
python demo/demo_scenarios.py
```

### Access Data Files
```python
import json

# Load people
with open('demo/data/people.json') as f:
    people = json.load(f)

# Load Slack messages
with open('demo/data/slack_messages.json') as f:
    messages = json.load(f)

# Load Jira tickets
with open('demo/data/jira_tickets.json') as f:
    tickets = json.load(f)

# Load documents
with open('demo/data/documents.json') as f:
    documents = json.load(f)
```

## Data Quality

✅ **Realistic**: Based on real enterprise scenarios  
✅ **Interconnected**: People, events, and documents reference each other  
✅ **Detailed**: Rich context with dates, costs, outcomes  
✅ **Diverse**: Successes and failures, decisions and incidents  
✅ **Searchable**: Structured JSON with consistent schema  

## Next Steps

This demo data is ready to be:
1. **Ingested** by the knowledge extraction engine (Section 3)
2. **Stored** in ChromaDB and NetworkX graph (Section 4)
3. **Queried** by the proactive engine (Section 5)
4. **Displayed** in the React dashboard (Section 7)

---

**Section 2 Status**: ✅ **COMPLETE**  
**Time to Build**: ~30 minutes  
**Files Created**: 6 (seed_data.py, demo_scenarios.py, 4 JSON data files)  
**Lines of Code**: ~800  
**Demo Readiness**: 100% - All scenarios have supporting data
