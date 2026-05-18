# 🚀 Render Deployment - Quick Start

## Your Gemini API Key
```
AIzaSyBLoai6drn-l1b-6XT3WN0dOsgeLosTUfQ
```

---

## 📋 Step-by-Step (30 minutes)

### ✅ Step 1: Sign Up (2 min)
1. Go to: **https://render.com**
2. Click **"Get Started"**
3. Sign up with **GitHub**
4. Authorize Render

---

### ✅ Step 2: Deploy Backend (15 min)

#### Create Service:
1. Click **"New +"** → **"Web Service"**
2. Select **"ContextBridge"** repository
3. Click **"Connect"**

#### Configure:
```
Name: contextbridge-backend
Region: Oregon (Free)
Branch: main
Build: pip install -r requirements.txt
Start: uvicorn main:app --host 0.0.0.0 --port $PORT
Plan: Free
```

#### Add Environment Variables:
Click **"Add Environment Variable"** for each:

```
PYTHON_VERSION = 3.11.0
GEMINI_API_KEY = AIzaSyBLoai6drn-l1b-6XT3WN0dOsgeLosTUfQ
ENVIRONMENT = production
DEBUG = False
DATABASE_URL = sqlite:///./data/contextbridge.db
CHROMA_PERSIST_DIR = ./data/chroma_db
DEMO_MODE = true
CORS_ORIGINS = http://localhost:3000
```

#### Add Disk:
```
Name: contextbridge-data
Mount Path: /opt/render/project/src/data
Size: 1 GB
```

#### Deploy:
1. Click **"Create Web Service"**
2. Wait 5-10 minutes
3. **Copy your backend URL** (e.g., `https://contextbridge-backend.onrender.com`)

---

### ✅ Step 3: Update Frontend Config (2 min)

#### Option A: Via GitHub
1. Go to: https://github.com/Sharun7/ContextBridge
2. Open: `frontend/.env.production`
3. Click pencil icon (Edit)
4. Replace with:
```env
REACT_APP_API_URL=https://YOUR-BACKEND-URL.onrender.com
REACT_APP_ENV=production
GENERATE_SOURCEMAP=false
```
5. Replace `YOUR-BACKEND-URL` with your actual backend URL
6. Commit changes

#### Option B: Via Command Line
```bash
cd contextbridge
# Edit frontend/.env.production with your backend URL
git add frontend/.env.production
git commit -m "Update API URL"
git push origin main
```

---

### ✅ Step 4: Deploy Frontend (10 min)

#### Create Static Site:
1. Click **"New +"** → **"Static Site"**
2. Select **"ContextBridge"** repository
3. Click **"Connect"**

#### Configure:
```
Name: contextbridge-frontend
Branch: main
Root Directory: frontend
Build: npm install && npm run build
Publish: build
```

#### Add Environment Variables:
```
REACT_APP_API_URL = https://YOUR-BACKEND-URL.onrender.com
NODE_VERSION = 18.17.0
```

#### Deploy:
1. Click **"Create Static Site"**
2. Wait 5-10 minutes
3. **Copy your frontend URL** (e.g., `https://contextbridge-frontend.onrender.com`)

---

### ✅ Step 5: Update CORS (3 min)

1. Go to **"contextbridge-backend"** service
2. Click **"Environment"**
3. Edit **"CORS_ORIGINS"**
4. Update to:
```
https://YOUR-FRONTEND-URL.onrender.com,http://localhost:3000
```
5. Replace `YOUR-FRONTEND-URL` with your actual frontend URL
6. Save (auto-redeploys)

---

### ✅ Step 6: Test! (5 min)

#### Test Backend:
Open: `https://your-backend-url.onrender.com/docs`
- Should see FastAPI docs

#### Test Frontend:
Open: `https://your-frontend-url.onrender.com`
- Should see ContextBridge dashboard

#### Test Connection:
1. Click "Demo" in sidebar
2. Run a scenario
3. Should see data loading

---

## 🎉 Done!

Your app is live!

**Your URLs:**
- Frontend: `https://contextbridge-frontend.onrender.com`
- Backend: `https://contextbridge-backend.onrender.com`
- API Docs: `https://contextbridge-backend.onrender.com/docs`

---

## ⚠️ Important

**Free Tier:**
- Services spin down after 15 min inactivity
- First request takes 30-60 seconds to wake up
- Use UptimeRobot to keep awake: https://uptimerobot.com

**Keep Awake:**
1. Sign up at UptimeRobot
2. Add monitor: `https://your-backend-url.onrender.com/api/health`
3. Interval: 14 minutes

---

## 🐛 Issues?

**Backend won't start:**
- Check logs in Render dashboard
- Verify all environment variables
- Redeploy manually

**Frontend blank:**
- Check browser console (F12)
- Verify REACT_APP_API_URL is correct
- Check CORS settings

**CORS error:**
- Update CORS_ORIGINS in backend
- Include your frontend URL
- Save and wait for redeploy

---

## 📞 Help

Full guide: `RENDER_DEPLOYMENT_GUIDE.md`

Render docs: https://render.com/docs

---

**Time**: 30 minutes  
**Cost**: $0  
**Difficulty**: Easy 🟢
