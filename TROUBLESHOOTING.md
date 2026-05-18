# ContextBridge - Troubleshooting Guide

## ✅ FIXED: Port 8000 Already in Use

### Problem
Backend wouldn't start because port 8000 was already in use by old Python processes.

### Solution Applied
```bash
# 1. Find processes using port 8000
netstat -ano | findstr :8000

# 2. Kill the processes
taskkill /F /PID <PID1> /PID <PID2>

# 3. Restart backend
python main.py
```

---

## 🚀 Current Status (WORKING!)

### Backend
- ✅ Running on http://localhost:8000
- ✅ All endpoints responding
- ✅ Stats endpoint returns data with topics
- ✅ Demo data seeded (13 items)

### Frontend  
- ✅ Running on http://localhost:3000
- ✅ Compiled successfully
- ✅ All pages should work now

---

## 🧪 Quick Tests

### Test 1: Backend Health
```bash
curl http://localhost:8000/
# Expected: {"name":"ContextBridge","status":"running",...}
```

### Test 2: Stats with Topics
```bash
curl http://localhost:8000/api/stats
# Expected: {"total_knowledge_items":13,"top_topics":[...]}
```

### Test 3: Knowledge Search
```bash
curl "http://localhost:8000/api/knowledge/search?q=&limit=50"
# Expected: Array of 13 knowledge items
```

### Test 4: Graph Data
```bash
curl http://localhost:8000/api/graph
# Expected: {"nodes":[...],"links":[...]}
```

---

## 🌐 Access Your Application

Open in browser:
- **Main App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API Root**: http://localhost:8000

---

## 📊 What Should Work Now

### Dashboard Page
- ✅ 4 stat cards with counts
- ✅ Top Topics bar chart (10 topics)
- ✅ Content type breakdown
- ✅ Outcome breakdown

### Knowledge Base Page
- ✅ Shows all 13 items on load (Bug 1 Fixed!)
- ✅ Search and filters
- ✅ Item details modal

### Graph Page
- ✅ D3.js visualization (Bug 3 Fixed!)
- ✅ Colored nodes
- ✅ Draggable nodes
- ✅ Node details panel

### Demo Page
- ✅ 3 scenarios (A, B, C)
- ✅ Run scenarios
- ✅ See AI alerts

---

## 🐛 Common Issues & Solutions

### Issue 1: "This site can't be reached"
**Cause**: Frontend not running  
**Solution**: 
```bash
cd frontend
npm start
```

### Issue 2: "Empty reply from server"
**Cause**: Backend crashed or port conflict  
**Solution**:
```bash
# Kill old processes
netstat -ano | findstr :8000
taskkill /F /PID <PID>

# Restart
python main.py
```

### Issue 3: "No data available"
**Cause**: Demo data not seeded  
**Solution**:
```bash
curl -X POST http://localhost:8000/api/demo/seed
```

### Issue 4: Frontend shows errors
**Cause**: API not responding  
**Solution**:
1. Check backend is running: `curl http://localhost:8000/`
2. Check CORS settings in `main.py`
3. Restart both services

---

## 🔄 Clean Restart Process

If everything is broken, do this:

```bash
# 1. Kill all processes
taskkill /F /IM python.exe
taskkill /F /IM node.exe

# 2. Wait 2 seconds
timeout /t 2

# 3. Start backend
cd contextbridge
python main.py

# 4. Wait for backend to start (3 seconds)
timeout /t 3

# 5. Start frontend (in new terminal)
cd frontend
npm start

# 6. Wait for frontend to compile (10 seconds)
timeout /t 10

# 7. Open browser
start http://localhost:3000
```

---

## ✅ Verification Checklist

After starting, verify:

- [ ] Backend responds: `curl http://localhost:8000/`
- [ ] Stats endpoint works: `curl http://localhost:8000/api/stats`
- [ ] Frontend loads: Open http://localhost:3000
- [ ] Dashboard shows data
- [ ] Knowledge Base shows 13 items
- [ ] Graph page renders
- [ ] Demo scenarios work

---

## 📞 Still Not Working?

Check these:

1. **Python version**: Should be 3.11+
   ```bash
   python --version
   ```

2. **Node version**: Should be 16+
   ```bash
   node --version
   ```

3. **Dependencies installed**:
   ```bash
   pip install -r requirements.txt
   cd frontend && npm install
   ```

4. **Environment variables**:
   - Check `.env` file exists
   - `GEMINI_API_KEY` is set
   - `DEMO_MODE=true`

5. **Ports available**:
   - Port 8000 for backend
   - Port 3000 for frontend

---

**Your ContextBridge should now be fully functional!** 🎉
