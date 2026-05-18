# ContextBridge - Complete Deployment Guide

## 🚀 Recommended Hosting Strategy

Since ContextBridge has **two components** (Backend + Frontend), here's the best approach:

### Option 1: Render (Recommended for Full Stack)
- ✅ **Backend**: Render Web Service (Python)
- ✅ **Frontend**: Render Static Site
- ✅ **Database**: Render Disk Storage
- ✅ **Free Tier Available**
- ✅ **Easy Setup**

### Option 2: Split Hosting
- **Backend**: Render or Railway
- **Frontend**: Vercel or Netlify
- More complex but potentially better performance

### Option 3: All-in-One (Docker)
- **Platform**: Render, Railway, or DigitalOcean
- **Method**: Docker Compose
- Best for production

---

## 🎯 RECOMMENDED: Deploy on Render (Easiest)

Render is perfect for your project because:
- Supports Python backend natively
- Can host static frontend
- Provides persistent disk storage
- Has a free tier
- Simple configuration

---

## 📋 Step-by-Step: Deploy on Render

### Prerequisites
1. GitHub account (✅ You already have this)
2. Render account (free): https://render.com
3. Your repository: https://github.com/Sharun7/ContextBridge

---

## Part 1: Deploy Backend on Render

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

### Step 2: Prepare Backend for Render

Create a `render.yaml` file in your project root:

```yaml
services:
  # Backend API Service
  - type: web
    name: contextbridge-backend
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: OLLAMA_BASE_URL
        value: http://localhost:11434
      - key: DATABASE_URL
        value: sqlite:///./contextbridge.db
    disk:
      name: contextbridge-data
      mountPath: /opt/render/project/src
      sizeGB: 1

  # Frontend Static Site
  - type: web
    name: contextbridge-frontend
    env: static
    region: oregon
    plan: free
    buildCommand: cd frontend && npm install && npm run build
    staticPublishPath: frontend/build
    routes:
      - type: rewrite
        source: /*
        destination: /index.html
```

### Step 3: Update Backend Configuration

Update `config.py` to use environment variables:

```python
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("PORT", 8000))

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/contextbridge.db")

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

# ChromaDB Configuration
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(BASE_DIR / "chroma_db"))

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,https://contextbridge-frontend.onrender.com").split(",")

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
```

### Step 4: Create Render Build Script

Create `build.sh` in project root:

```bash
#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Setting up database..."
python -c "from db.database import init_db; init_db()"

echo "Build complete!"
```

Make it executable:
```bash
chmod +x build.sh
```

### Step 5: Deploy Backend on Render

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New +"** → **"Web Service"**
3. **Connect Repository**: Select `ContextBridge`
4. **Configure Service**:
   - **Name**: `contextbridge-backend`
   - **Region**: Oregon (Free)
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

5. **Add Environment Variables**:
   Click "Advanced" → "Add Environment Variable":
   
   ```
   PYTHON_VERSION=3.11.0
   ENVIRONMENT=production
   DEBUG=False
   OLLAMA_BASE_URL=http://localhost:11434
   DATABASE_URL=sqlite:///./contextbridge.db
   CORS_ORIGINS=https://contextbridge-frontend.onrender.com
   ```

6. **Add Persistent Disk** (Important!):
   - Scroll to "Disk"
   - Click "Add Disk"
   - **Name**: `contextbridge-data`
   - **Mount Path**: `/opt/render/project/src/data`
   - **Size**: 1 GB (Free tier)

7. **Click "Create Web Service"**

8. **Wait for Deployment** (5-10 minutes)

9. **Note Your Backend URL**: 
   - Example: `https://contextbridge-backend.onrender.com`

---

## Part 2: Deploy Frontend on Render

### Step 1: Update Frontend API URL

Update `frontend/src/services/api.ts`:

```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://contextbridge-backend.onrender.com'
    : 'http://localhost:8000');

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### Step 2: Create Frontend Environment File

Create `frontend/.env.production`:

```env
REACT_APP_API_URL=https://contextbridge-backend.onrender.com
REACT_APP_ENV=production
```

### Step 3: Deploy Frontend on Render

1. **Go to Render Dashboard**
2. **Click "New +"** → **"Static Site"**
3. **Connect Repository**: Select `ContextBridge`
4. **Configure Site**:
   - **Name**: `contextbridge-frontend`
   - **Branch**: `main`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `build`

5. **Add Environment Variables**:
   ```
   REACT_APP_API_URL=https://contextbridge-backend.onrender.com
   NODE_VERSION=18.17.0
   ```

6. **Click "Create Static Site"**

7. **Wait for Deployment** (3-5 minutes)

8. **Your Frontend URL**: 
   - Example: `https://contextbridge-frontend.onrender.com`

---

## Part 3: Update CORS Settings

After both are deployed, update backend CORS:

1. Go to Render Dashboard → Backend Service
2. Update `CORS_ORIGINS` environment variable:
   ```
   CORS_ORIGINS=https://contextbridge-frontend.onrender.com,http://localhost:3000
   ```
3. Save and redeploy

---

## 🔧 Environment Variables Reference

### Backend Environment Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `PORT` | Server port | `8000` | Auto-set by Render |
| `PYTHON_VERSION` | Python version | `3.11.0` | Yes |
| `ENVIRONMENT` | Environment | `production` | Yes |
| `DEBUG` | Debug mode | `False` | Yes |
| `DATABASE_URL` | Database path | `sqlite:///./contextbridge.db` | Yes |
| `OLLAMA_BASE_URL` | Ollama API URL | `http://localhost:11434` | Yes |
| `OLLAMA_MODEL` | LLM model | `llama2` | No |
| `CHROMA_PERSIST_DIR` | ChromaDB path | `./chroma_db` | No |
| `CORS_ORIGINS` | Allowed origins | `https://your-frontend.com` | Yes |

### Frontend Environment Variables

| Variable | Description | Example | Required |
|----------|-------------|---------|----------|
| `REACT_APP_API_URL` | Backend API URL | `https://backend.onrender.com` | Yes |
| `NODE_VERSION` | Node.js version | `18.17.0` | Yes |
| `REACT_APP_ENV` | Environment | `production` | No |

---

## ⚠️ Important Notes for Render Free Tier

### Limitations:
1. **Services spin down after 15 minutes of inactivity**
   - First request after inactivity takes 30-60 seconds
   - Solution: Use a service like UptimeRobot to ping every 14 minutes

2. **750 hours/month free** (enough for 1 service 24/7)
   - If you have 2 services, they share the 750 hours

3. **No Ollama on Free Tier**
   - Ollama requires significant resources
   - Options:
     - Use OpenAI API instead
     - Upgrade to paid plan ($7/month)
     - Host Ollama separately

### Workarounds:

#### Option A: Use OpenAI Instead of Ollama

Update `config.py`:
```python
USE_OPENAI = os.getenv("USE_OPENAI", "True").lower() == "true"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
```

Add to Render environment variables:
```
USE_OPENAI=True
OPENAI_API_KEY=your-openai-api-key
```

#### Option B: Keep Ollama Local (Hybrid Approach)
- Deploy frontend and database to Render
- Run backend locally with Ollama
- Use ngrok to expose local backend

---

## 🎯 Alternative: Deploy on Vercel + Render

### Backend on Render (Same as above)

### Frontend on Vercel (Faster)

1. **Go to Vercel**: https://vercel.com
2. **Import Project**: Connect GitHub
3. **Select Repository**: `ContextBridge`
4. **Configure**:
   - **Framework**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

5. **Environment Variables**:
   ```
   REACT_APP_API_URL=https://contextbridge-backend.onrender.com
   ```

6. **Deploy**

**Vercel Advantages**:
- ✅ Faster CDN
- ✅ Better performance
- ✅ Automatic HTTPS
- ✅ No spin-down

---

## 🐳 Alternative: Deploy with Docker (Railway)

Railway supports Docker Compose and has better free tier for Docker.

### Step 1: Update docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "${PORT:-8000}:8000"
    environment:
      - DATABASE_URL=sqlite:///./data/contextbridge.db
      - CHROMA_PERSIST_DIR=/app/data/chroma_db
      - CORS_ORIGINS=${CORS_ORIGINS}
    volumes:
      - app-data:/app/data

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - REACT_APP_API_URL=${BACKEND_URL}
    depends_on:
      - backend

volumes:
  app-data:
```

### Step 2: Deploy on Railway

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `ContextBridge`
5. Railway auto-detects Docker Compose
6. Add environment variables
7. Deploy

---

## 📝 Pre-Deployment Checklist

### Code Changes Needed:

- [ ] Update `config.py` with environment variables
- [ ] Update `frontend/src/services/api.ts` with production URL
- [ ] Create `frontend/.env.production`
- [ ] Add `render.yaml` (optional but recommended)
- [ ] Update CORS settings in backend
- [ ] Test locally with production-like settings

### Commit and Push:

```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

---

## 🧪 Testing Your Deployment

### Backend Health Check:
```bash
curl https://your-backend.onrender.com/health
```

### Frontend Check:
Open browser: `https://your-frontend.onrender.com`

### API Test:
```bash
curl https://your-backend.onrender.com/api/items
```

---

## 🔍 Troubleshooting

### Backend won't start:
1. Check logs in Render dashboard
2. Verify all environment variables are set
3. Check `requirements.txt` is complete
4. Ensure Python version is correct

### Frontend can't connect to backend:
1. Check CORS settings
2. Verify `REACT_APP_API_URL` is correct
3. Check browser console for errors
4. Ensure backend is running

### Database issues:
1. Ensure persistent disk is mounted
2. Check database path in environment variables
3. Verify write permissions

### Ollama not working:
1. Ollama requires significant resources
2. Consider using OpenAI API instead
3. Or upgrade to paid plan

---

## 💰 Cost Comparison

### Free Tier:
- **Render**: Free (with limitations)
- **Vercel**: Free (generous limits)
- **Railway**: $5 credit/month

### Paid Plans:
- **Render**: $7/month per service
- **Vercel**: $20/month (Pro)
- **Railway**: Pay as you go (~$5-10/month)

---

## 🎉 Quick Start Commands

### 1. Prepare for Deployment:
```bash
cd contextbridge

# Update config files
# (Make the changes mentioned above)

# Commit changes
git add .
git commit -m "Configure for production deployment"
git push origin main
```

### 2. Deploy Backend on Render:
- Go to https://dashboard.render.com
- New Web Service
- Connect GitHub repo
- Configure as described above

### 3. Deploy Frontend on Vercel:
- Go to https://vercel.com
- Import Project
- Select repository
- Deploy

### 4. Update Environment Variables:
- Add backend URL to frontend
- Add frontend URL to backend CORS

### 5. Test:
- Visit your frontend URL
- Check if API calls work
- Test all features

---

## 📞 Need Help?

If you encounter issues:
1. Check Render/Vercel logs
2. Review environment variables
3. Test locally first
4. Check CORS settings
5. Verify all URLs are correct

---

**Ready to deploy?** Follow the steps above and your ContextBridge will be live! 🚀

**Recommended Path**: 
1. Backend on Render
2. Frontend on Vercel
3. Use OpenAI API instead of Ollama (for free tier)
