# ContextBridge - Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Prerequisites
- Python 3.8+
- Gemini API Key (already configured in `.env`)

### Step 1: Install Dependencies

```bash
cd contextbridge
pip install -r requirements.txt
```

### Step 2: Start the API Server

```bash
python main.py
```

Server starts at: **http://localhost:8000**

### Step 3: Seed Demo Data

Open a new terminal:

```bash
curl -X POST http://localhost:8000/api/demo/seed
```

### Step 4: Run Demo Scenario

```bash
curl -X POST http://localhost:8000/api/demo/scenario/A
```

You should see a **WARNING** alert about the $500K PostgreSQL failure!

---

## 📚 API Documentation

Visit: **http://localhost:8000/docs**

Interactive Swagger UI with all endpoints.

---

## 🎯 Demo Scenarios

### Scenario A: The Mistake Prevented
```bash
curl -X POST http://localhost:8000/api/demo/scenario/A
```
Shows how ContextBridge prevents a $500K database migration failure.

### Scenario B: The Question Answered
```bash
curl -X POST http://localhost:8000/api/demo/scenario/B
```
Answers "Why do we use React?" with full organizational context.

### Scenario C: Document Context
```bash
curl -X POST http://localhost:8000/api/demo/scenario/C
```
Surfaces relevant lessons when writing a migration guide.

---

## 🔍 Try Other Endpoints

### Search Knowledge
```bash
curl "http://localhost:8000/api/knowledge/search?q=database migration&limit=5"
```

### Query Knowledge Base
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What do we know about PostgreSQL?"}'
```

### Get Knowledge Graph
```bash
curl "http://localhost:8000/api/graph"
```

### Find Experts
```bash
curl "http://localhost:8000/api/experts?topic=database"
```

### Get Stats
```bash
curl "http://localhost:8000/api/stats"
```

---

## 🧪 Run Tests

```bash
# Make sure server is running first
python test_api.py
```

---

## 📊 What's Built

✅ **Section 1**: Project setup
✅ **Section 2**: Demo data generator
✅ **Section 3**: Knowledge extraction (Gemini)
✅ **Section 4**: Vector store (ChromaDB) + Knowledge graph (NetworkX)
✅ **Section 5**: Proactive intelligence engine
✅ **Section 6**: FastAPI backend (13 endpoints)

---

## 🎬 Hackathon Demo Flow

1. Start API: `python main.py`
2. Seed data: `POST /api/demo/seed`
3. Run Scenario A: `POST /api/demo/scenario/A`
4. Show the $500K warning alert
5. Query: `POST /api/query` with "Why React?"
6. Visualize: `GET /api/graph`
7. **WOW the judges!** 🎉

---

## 📖 Full Documentation

- `README.md` - Project overview
- `SECTION_3_COMPLETE.md` - Knowledge extraction
- `SECTION_4_COMPLETE.md` - Storage layer
- `SECTION_5_COMPLETE.md` - Proactive engine
- `SECTION_6_COMPLETE.md` - API backend

---

## 🆘 Troubleshooting

### Port already in use?
```bash
# Change port in config.py
API_PORT = 8001
```

### Gemini API errors?
Check your API key in `.env` file.

### ChromaDB errors?
Delete `chroma_db/` folder and restart.

---

## 🎯 Next Steps

- Build React frontend (Section 7)
- Create demo video
- Prepare hackathon presentation

---

**ContextBridge** - Preventing $500K mistakes, one alert at a time! 🚀
