# 🚀 ContextBridge Deployment Checklist

## Quick Deployment Steps

### ✅ Step 1: Commit All Changes
```bash
cd contextbridge
git add .
git commit -m "Prepare for production deployment"
git push origin main
```

### ✅ Step 2: Sign Up for Hosting

**Render (Recommended):**
- Go to: https://render.com
- Sign up with GitHub
- Authorize Render to access your repositories

**Vercel (For Frontend):**
- Go to: https://vercel.com
- Sign up with GitHub

### ✅ Step 3: Deploy Backend on Render

1. **Create New Web Service**
   - Dashboard → New + → Web Service
   - Connect Repository: `ContextBridge`

2. **Configure Service**
   ```
   Name: contextbridge-backend
   Region: Oregon (Free)
   Branch: main
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   Plan: Free
   ```

3. **Add Environment Variables** (Click "Advanced")
   ```
   PYTHON_VERSION=3.11.0
   ENVIRONMENT=production
   DEBUG=False
   GEMINI_API_KEY=your-gemini-api-key-here
   DATABASE_URL=sqlite:///./data/contextbridge.db
   CHROMA_PERSIST_DIR=./data/chroma_db
   CORS_ORIGINS=https://contextbridge-frontend.onrender.com,http://localhost:3000
   ```

4. **Add Persistent Disk**
   ```
   Name: contextbridge-data
   Mount Path: /opt/render/project/src/data
   Size: 1 GB
   ```

5. **Click "Create Web Service"**

6. **Wait for deployment** (5-10 minutes)

7. **Copy your backend URL**: 
   - Example: `https://contextbridge-backend.onrender.com`

### ✅ Step 4: Deploy Frontend on Vercel (Recommended)

1. **Import Project**
   - Go to https://vercel.com/new
   - Import Git Repository
   - Select `ContextBridge`

2. **Configure Project**
   ```
   Framework Preset: Create React App
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: build
   ```

3. **Add Environment Variables**
   ```
   REACT_APP_API_URL=https://contextbridge-backend.onrender.com
   ```

4. **Click "Deploy"**

5. **Wait for deployment** (2-3 minutes)

6. **Copy your frontend URL**:
   - Example: `https://contextbridge.vercel.app`

### ✅ Step 5: Update CORS Settings

1. Go back to Render Dashboard
2. Select your backend service
3. Go to "Environment"
4. Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS=https://contextbridge.vercel.app,http://localhost:3000
   ```
5. Save (service will auto-redeploy)

### ✅ Step 6: Test Your Deployment

1. **Test Backend**:
   - Open: `https://your-backend.onrender.com/docs`
   - Should see FastAPI documentation

2. **Test Frontend**:
   - Open: `https://your-frontend.vercel.app`
   - Should see ContextBridge dashboard

3. **Test API Connection**:
   - Click around in the frontend
   - Check if data loads
   - Try the demo scenarios

---

## 🔑 Required Environment Variables

### Backend (Render)

**REQUIRED:**
- `GEMINI_API_KEY` - Get from https://makersuite.google.com/app/apikey
- `CORS_ORIGINS` - Your frontend URL
- `PYTHON_VERSION` - 3.11.0
- `ENVIRONMENT` - production

**OPTIONAL:**
- `DATABASE_URL` - sqlite:///./data/contextbridge.db (default)
- `CHROMA_PERSIST_DIR` - ./data/chroma_db (default)
- `DEBUG` - False (default)

### Frontend (Vercel)

**REQUIRED:**
- `REACT_APP_API_URL` - Your backend URL from Render

---

## 🎯 Where to Get API Keys

### Gemini API Key (Required)
1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key
4. Add to Render environment variables

### Alternative: OpenAI API Key
If you prefer OpenAI instead of Gemini:
1. Go to: https://platform.openai.com/api-keys
2. Create new secret key
3. Add to Render as `OPENAI_API_KEY`
4. Update code to use OpenAI

---

## ⚠️ Important Notes

### Free Tier Limitations

**Render Free Tier:**
- ✅ 750 hours/month (enough for 1 service 24/7)
- ⚠️ Services spin down after 15 minutes of inactivity
- ⚠️ First request after spin-down takes 30-60 seconds
- ✅ 1 GB persistent disk storage

**Vercel Free Tier:**
- ✅ Unlimited bandwidth
- ✅ No spin-down
- ✅ Fast CDN
- ✅ Automatic HTTPS

### Keep Service Awake (Optional)

Use a service like **UptimeRobot** to ping your backend every 14 minutes:
1. Go to: https://uptimerobot.com
2. Add new monitor
3. URL: `https://your-backend.onrender.com/api/health`
4. Interval: 14 minutes

---

## 🐛 Troubleshooting

### Backend won't start
- ✅ Check logs in Render dashboard
- ✅ Verify `GEMINI_API_KEY` is set
- ✅ Check all environment variables
- ✅ Ensure `requirements.txt` is complete

### Frontend can't connect to backend
- ✅ Check `REACT_APP_API_URL` is correct
- ✅ Verify CORS settings in backend
- ✅ Check browser console for errors
- ✅ Ensure backend is running (not spun down)

### Database errors
- ✅ Ensure persistent disk is mounted
- ✅ Check `DATABASE_URL` path
- ✅ Verify disk mount path: `/opt/render/project/src/data`

### Slow first load
- ⚠️ This is normal on free tier
- Service spins down after 15 minutes
- First request wakes it up (30-60 seconds)
- Use UptimeRobot to keep it awake

---

## 📊 Deployment Status

Track your deployment:

- [ ] Code committed and pushed to GitHub
- [ ] Render account created
- [ ] Backend deployed on Render
- [ ] Backend URL copied
- [ ] Gemini API key added
- [ ] Persistent disk configured
- [ ] Vercel account created
- [ ] Frontend deployed on Vercel
- [ ] Frontend URL copied
- [ ] CORS updated with frontend URL
- [ ] Backend health check passes
- [ ] Frontend loads successfully
- [ ] API connection working
- [ ] Demo scenarios tested

---

## 🎉 Success!

Once all checkboxes are complete, your ContextBridge is live!

**Share your URLs:**
- Backend API: `https://your-backend.onrender.com`
- Frontend App: `https://your-frontend.vercel.app`
- API Docs: `https://your-backend.onrender.com/docs`

---

## 📞 Need Help?

**Common Issues:**
1. **"Application failed to respond"** → Check logs, verify environment variables
2. **"CORS error"** → Update CORS_ORIGINS with your frontend URL
3. **"API key invalid"** → Verify Gemini API key is correct
4. **"Database error"** → Check persistent disk is mounted

**Resources:**
- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- Gemini API: https://ai.google.dev/docs

---

**Estimated Deployment Time:** 20-30 minutes  
**Cost:** $0 (Free tier)  
**Difficulty:** Easy 🟢
