# 🚀 Deploy ContextBridge on Render (Backend + Frontend)

## Complete Guide - Both Services on Render

---

## 📋 Your Gemini API Key

```
AIzaSyBLoai6drn-l1b-6XT3WN0dOsgeLosTUfQ
```

**Keep this safe!** You'll need it in Step 3.

---

## ⏱️ Total Time: 30-40 minutes

---

## 🎯 Step 1: Sign Up for Render (5 minutes)

1. Go to: **https://render.com**
2. Click **"Get Started"**
3. Sign up with **GitHub**
4. Click **"Authorize Render"**
5. You'll be redirected to Render Dashboard

✅ **Done!** You now have a Render account.

---

## 🔧 Step 2: Deploy Backend (15 minutes)

### 2.1 Create Web Service

1. In Render Dashboard, click **"New +"** (top right)
2. Select **"Web Service"**
3. Click **"Connect a repository"**
4. Find and select **"ContextBridge"**
5. Click **"Connect"**

### 2.2 Configure Backend Service

Fill in these settings:

**Basic Settings:**
```
Name: contextbridge-backend
Region: Oregon (Free)
Branch: main
Root Directory: (leave empty)
Runtime: Python 3
```

**Build & Deploy:**
```
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Instance Type:**
```
Plan: Free
```

### 2.3 Add Environment Variables

Scroll down to **"Environment Variables"** section.

Click **"Add Environment Variable"** and add these **ONE BY ONE**:

```
Key: PYTHON_VERSION
Value: 3.11.0
```

```
Key: GEMINI_API_KEY
Value: AIzaSyBLoai6drn-l1b-6XT3WN0dOsgeLosTUfQ
```

```
Key: ENVIRONMENT
Value: production
```

```
Key: DEBUG
Value: False
```

```
Key: DATABASE_URL
Value: sqlite:///./data/contextbridge.db
```

```
Key: CHROMA_PERSIST_DIR
Value: ./data/chroma_db
```

```
Key: DEMO_MODE
Value: true
```

```
Key: CORS_ORIGINS
Value: http://localhost:3000
```
*(We'll update this after deploying frontend)*

### 2.4 Add Persistent Disk

Scroll down to **"Disk"** section.

Click **"Add Disk"** and configure:

```
Name: contextbridge-data
Mount Path: /opt/render/project/src/data
Size: 1 GB
```

### 2.5 Deploy Backend

1. Click **"Create Web Service"** (bottom of page)
2. Wait for deployment (5-10 minutes)
3. Watch the logs - you'll see:
   - Installing dependencies
   - Starting server
   - "Application startup complete"

### 2.6 Copy Backend URL

Once deployed, you'll see your service URL at the top:

**Example**: `https://contextbridge-backend.onrender.com`

**📝 WRITE THIS DOWN!** You'll need it for the frontend.

✅ **Backend is live!**

Test it: Open `https://your-backend-url.onrender.com/docs`

You should see the FastAPI documentation page.

---

## 🎨 Step 3: Deploy Frontend (15 minutes)

### 3.1 Update Frontend Environment File

Before deploying, we need to update the frontend config.

**Option A: Update via GitHub (Recommended)**

1. Go to your GitHub repository: https://github.com/Sharun7/ContextBridge
2. Navigate to: `frontend/.env.production`
3. Click the pencil icon (Edit)
4. Replace the content with:

```env
REACT_APP_API_URL=https://your-backend-url.onrender.com
REACT_APP_ENV=production
GENERATE_SOURCEMAP=false
```

**⚠️ IMPORTANT**: Replace `your-backend-url.onrender.com` with YOUR actual backend URL from Step 2.6

5. Click **"Commit changes"**
6. Add commit message: "Update frontend API URL"
7. Click **"Commit changes"**

**Option B: Update Locally**

```bash
cd contextbridge
# Edit frontend/.env.production with your backend URL
git add frontend/.env.production
git commit -m "Update frontend API URL"
git push origin main
```

### 3.2 Create Static Site

1. In Render Dashboard, click **"New +"**
2. Select **"Static Site"**
3. Find and select **"ContextBridge"** repository
4. Click **"Connect"**

### 3.3 Configure Frontend Service

Fill in these settings:

**Basic Settings:**
```
Name: contextbridge-frontend
Branch: main
Root Directory: frontend
```

**Build Settings:**
```
Build Command: npm install && npm run build
Publish Directory: build
```

**Auto-Deploy:**
```
Auto-Deploy: Yes
```

### 3.4 Add Environment Variables

Click **"Advanced"** to expand environment variables.

Add this variable:

```
Key: REACT_APP_API_URL
Value: https://your-backend-url.onrender.com
```

**⚠️ IMPORTANT**: Use YOUR actual backend URL from Step 2.6

```
Key: NODE_VERSION
Value: 18.17.0
```

### 3.5 Deploy Frontend

1. Click **"Create Static Site"**
2. Wait for deployment (5-10 minutes)
3. Watch the logs - you'll see:
   - Installing dependencies
   - Building React app
   - Publishing to CDN

### 3.6 Copy Frontend URL

Once deployed, you'll see your site URL:

**Example**: `https://contextbridge-frontend.onrender.com`

**📝 WRITE THIS DOWN!**

✅ **Frontend is live!**

---

## 🔄 Step 4: Update CORS Settings (5 minutes)

Now we need to tell the backend to accept requests from the frontend.

### 4.1 Update Backend CORS

1. Go to Render Dashboard
2. Click on **"contextbridge-backend"** service
3. Click **"Environment"** in the left sidebar
4. Find the **"CORS_ORIGINS"** variable
5. Click the pencil icon to edit
6. Update the value to:

```
https://contextbridge-frontend.onrender.com,http://localhost:3000
```

**⚠️ IMPORTANT**: Replace `contextbridge-frontend.onrender.com` with YOUR actual frontend URL

7. Click **"Save Changes"**
8. Service will automatically redeploy (2-3 minutes)

✅ **CORS configured!**

---

## 🧪 Step 5: Test Your Deployment (5 minutes)

### 5.1 Test Backend

Open: `https://your-backend-url.onrender.com/docs`

You should see:
- ✅ FastAPI documentation page
- ✅ List of API endpoints
- ✅ Try the `/api/health` endpoint

### 5.2 Test Frontend

Open: `https://your-frontend-url.onrender.com`

You should see:
- ✅ ContextBridge dashboard
- ✅ Navigation sidebar
- ✅ Stats and metrics

### 5.3 Test API Connection

In the frontend:
1. Click **"Demo"** in the sidebar
2. Click **"Run Scenario"** on any demo
3. Wait for results
4. You should see data loading

If you see data, **everything is working!** 🎉

---

## 📊 Your Deployment Summary

### Backend Service
- **URL**: `https://contextbridge-backend.onrender.com`
- **API Docs**: `https://contextbridge-backend.onrender.com/docs`
- **Health Check**: `https://contextbridge-backend.onrender.com/api/health`
- **Plan**: Free
- **Region**: Oregon

### Frontend Service
- **URL**: `https://contextbridge-frontend.onrender.com`
- **Plan**: Free
- **Region**: Oregon

### Environment Variables Set
- ✅ GEMINI_API_KEY
- ✅ PYTHON_VERSION
- ✅ ENVIRONMENT
- ✅ DATABASE_URL
- ✅ CHROMA_PERSIST_DIR
- ✅ CORS_ORIGINS
- ✅ REACT_APP_API_URL

---

## ⚠️ Important Notes

### Free Tier Limitations

**Backend:**
- ✅ 750 hours/month free
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ First request after spin-down takes 30-60 seconds
- ✅ 1 GB persistent disk storage

**Frontend:**
- ✅ 100 GB bandwidth/month
- ✅ Global CDN
- ✅ Automatic HTTPS
- ⚠️ Also spins down after inactivity

### Keep Services Awake (Optional)

Use **UptimeRobot** to ping your backend every 14 minutes:

1. Go to: https://uptimerobot.com
2. Sign up (free)
3. Add New Monitor:
   - **Type**: HTTP(s)
   - **URL**: `https://your-backend-url.onrender.com/api/health`
   - **Monitoring Interval**: 14 minutes
4. Save

This keeps your backend awake 24/7!

---

## 🐛 Troubleshooting

### Issue: Backend won't start

**Check:**
1. Go to backend service → **"Logs"**
2. Look for errors
3. Common issues:
   - Missing environment variables
   - Wrong Python version
   - Dependencies not installing

**Solution:**
- Verify all environment variables are set
- Check `PYTHON_VERSION=3.11.0`
- Redeploy: Click **"Manual Deploy"** → **"Deploy latest commit"**

### Issue: Frontend shows blank page

**Check:**
1. Open browser console (F12)
2. Look for errors
3. Common issues:
   - CORS error
   - Wrong API URL
   - Backend not running

**Solution:**
- Verify `REACT_APP_API_URL` is correct
- Check CORS settings in backend
- Ensure backend is running (not spun down)

### Issue: "CORS policy" error

**Solution:**
1. Go to backend service → **"Environment"**
2. Update `CORS_ORIGINS` with your frontend URL
3. Make sure format is: `https://your-frontend.onrender.com`
4. Save and wait for redeploy

### Issue: API calls fail

**Check:**
1. Backend logs for errors
2. Frontend console for errors
3. Network tab in browser DevTools

**Solution:**
- Verify backend is running
- Check API URL in frontend
- Test backend directly: `/docs` endpoint

### Issue: Slow first load

**This is normal!**
- Free tier services spin down after 15 minutes
- First request wakes them up (30-60 seconds)
- Use UptimeRobot to keep awake

---

## 🔄 Making Updates

### Update Backend Code

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update backend"
   git push origin main
   ```
3. Render auto-deploys (if enabled)
4. Or click **"Manual Deploy"** in Render dashboard

### Update Frontend Code

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update frontend"
   git push origin main
   ```
3. Render auto-deploys (if enabled)
4. Or click **"Manual Deploy"** in Render dashboard

---

## 💰 Cost Breakdown

### Free Tier (Current)
- **Backend**: $0/month
- **Frontend**: $0/month
- **Total**: **$0/month** ✅

### Paid Tier (If Needed)
- **Backend**: $7/month (no spin-down, better performance)
- **Frontend**: $7/month (no spin-down, more bandwidth)
- **Total**: $14/month

**Recommendation**: Start with free tier, upgrade if needed.

---

## 📝 Quick Reference

### Your URLs
```
Backend: https://contextbridge-backend.onrender.com
Frontend: https://contextbridge-frontend.onrender.com
API Docs: https://contextbridge-backend.onrender.com/docs
```

### Your API Key
```
GEMINI_API_KEY=AIzaSyBLoai6drn-l1b-6XT3WN0dOsgeLosTUfQ
```

### Important Paths
```
Backend Root: /
Frontend Root: /frontend
Data Mount: /opt/render/project/src/data
```

---

## ✅ Deployment Checklist

- [ ] Render account created
- [ ] Backend service created
- [ ] Backend environment variables added
- [ ] Backend persistent disk configured
- [ ] Backend deployed successfully
- [ ] Backend URL copied
- [ ] Frontend .env.production updated
- [ ] Frontend service created
- [ ] Frontend environment variables added
- [ ] Frontend deployed successfully
- [ ] Frontend URL copied
- [ ] CORS updated with frontend URL
- [ ] Backend health check passes
- [ ] Frontend loads successfully
- [ ] API connection working
- [ ] Demo scenarios tested

---

## 🎉 Success!

Your ContextBridge is now live on Render!

**Share your app:**
- Frontend: `https://your-frontend.onrender.com`
- API Docs: `https://your-backend.onrender.com/docs`

**Next Steps:**
1. Test all features
2. Share with others
3. Monitor usage in Render dashboard
4. Consider UptimeRobot to keep services awake
5. Upgrade to paid tier if needed

---

## 📞 Need Help?

**Render Support:**
- Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

**ContextBridge Issues:**
- Check logs in Render dashboard
- Review environment variables
- Test locally first
- Check CORS settings

---

**Deployment Time**: 30-40 minutes  
**Difficulty**: Easy 🟢  
**Cost**: Free 💰  
**Status**: Production Ready ✅
