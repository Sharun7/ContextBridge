# ContextBridge - Quick Reference Card

**One-page reference for hackathon demo**

---

## 🚀 Start Everything

```bash
# Windows
startup.bat

# Mac/Linux
./startup.sh
```

**Ready in**: ~2 minutes

---

## 🎯 Access URLs

| What | URL |
|------|-----|
| **Demo** ⭐ | http://localhost:3000/demo |
| Dashboard | http://localhost:3000 |
| API Docs | http://localhost:8000/docs |
| Health | http://localhost:8000/api/health |

---

## 🎭 Demo Flow

1. Open http://localhost:3000/demo
2. Click **"Scenario A: Prevent a Mistake"**
3. Watch loading animation
4. **Point out**:
   - 🚨 WARNING headline
   - 💯 100% confidence
   - 📊 Gemini synthesis
   - ✅ 5 recommended actions
   - 👥 Relevant experts
5. Say: **"This would have prevented the $500K loss"**

---

## 💬 Key Talking Points

**The Problem**:
- Organizations lose millions repeating mistakes
- NovaTech lost $500K on PostgreSQL migration
- Knowledge scattered across Slack, Jira, documents

**The Solution**:
- AI-powered institutional memory agent
- Uses Google Gemini for extraction & synthesis
- Proactively warns when similar situations arise

**The Impact**:
- Prevents mistakes BEFORE they happen
- 5000x ROI (one prevented incident pays for system)
- Works with existing enterprise tools
- Production-ready with one-command deployment

---

## 🐛 Emergency Fixes

**Backend crashed**:
```bash
docker-compose restart contextbridge-api
```

**Frontend crashed**:
```bash
docker-compose restart contextbridge-ui
```

**No data**:
```bash
curl -X POST http://localhost:8000/api/demo/seed
```

**Fresh start**:
```bash
docker-compose down -v
./startup.sh
```

---

## 📊 Key Stats

- **8 sections** complete
- **60+ files** created
- **6100+ lines** of code
- **14 documentation** files
- **3 demo scenarios** working
- **13 REST endpoints** implemented
- **5 frontend pages** built
- **100% confidence** scores

---

## 🏆 Why We Win

1. **Solves $500K problem** - Compelling story
2. **Complete system** - Backend + Frontend + Docker
3. **AI-powered** - Gemini synthesis
4. **Beautiful UI** - Professional animations
5. **Easy to run** - One command
6. **Production-ready** - Health checks, error handling
7. **Well-documented** - 14 files

---

## 🎤 30-Second Pitch

> "ContextBridge prevents organizations from repeating costly mistakes. NovaTech lost $500K on a PostgreSQL migration because they forgot about a similar failure. ContextBridge uses Google Gemini to extract knowledge from Slack, Jira, and documents, then proactively warns you when similar situations arise. We've built a complete full-stack system with one-command Docker deployment. Even preventing one incident pays for the system 5000 times over."

---

## ✅ Pre-Demo Checklist

- [ ] Docker running
- [ ] API key in `.env`
- [ ] Run startup script
- [ ] Test Scenario A
- [ ] Browser full-screen
- [ ] Close extra tabs

---

**Good luck!** 🏆
