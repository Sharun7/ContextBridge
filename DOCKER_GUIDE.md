# ContextBridge Docker Guide

Complete guide for running ContextBridge with Docker.

---

## 🐳 Prerequisites

1. **Docker Desktop** installed and running
   - Windows: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Mac: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Linux: Install Docker Engine and Docker Compose

2. **Google Gemini API Key**
   - Get your key from: https://makersuite.google.com/app/apikey

---

## 🚀 One-Command Start

### Windows

```bash
startup.bat
```

### Mac/Linux

```bash
chmod +x startup.sh
./startup.sh
```

The startup script will:
1. ✅ Check if Docker is running
2. ✅ Create `.env` file if missing
3. ✅ Build Docker images
4. ✅ Start all services
5. ✅ Wait for services to be healthy
6. ✅ Seed demo data automatically
7. ✅ Open the demo page in your browser

---

## 📦 What Gets Deployed

### Services

**contextbridge-api** (Backend)
- Port: 8000
- Base Image: python:3.11-slim
- Features:
  - FastAPI REST API
  - Google Gemini integration
  - ChromaDB vector store
  - NetworkX knowledge graph
  - Auto-reload on code changes

**contextbridge-ui** (Frontend)
- Port: 3000
- Base Image: node:20-alpine
- Features:
  - React TypeScript dashboard
  - Tailwind CSS styling
  - D3.js knowledge graph
  - Framer Motion animations
  - Production-optimized build

### Volumes

- `./chroma_db` - Persists vector store data
- `./logs` - Persists application logs

### Network

- `contextbridge-network` - Bridge network for service communication

---

## 🔧 Manual Docker Commands

### Build and Start

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f contextbridge-api
docker-compose logs -f contextbridge-ui
```

### Stop and Remove

```bash
# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove containers, and remove volumes
docker-compose down -v
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart contextbridge-api
docker-compose restart contextbridge-ui
```

### Rebuild After Code Changes

```bash
# Rebuild and restart
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build contextbridge-api
```

---

## 🔍 Health Checks

Both services have built-in health checks:

**Backend Health Check**:
```bash
curl http://localhost:8000/api/health
```

**Frontend Health Check**:
```bash
curl http://localhost:3000
```

**Docker Health Status**:
```bash
docker-compose ps
```

---

## 📊 Seeding Demo Data

### Automatic (via startup script)

The startup script automatically seeds demo data.

### Manual

```bash
# After services are running
curl -X POST http://localhost:8000/api/demo/seed
```

Or use the Python script:
```bash
docker-compose exec contextbridge-api python demo/seed_data.py
```

---

## 🐛 Troubleshooting

### Docker Not Running

**Error**: `Cannot connect to the Docker daemon`

**Solution**: Start Docker Desktop

### Port Already in Use

**Error**: `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Solution**: Stop the service using that port or change the port in `docker-compose.yml`

```yaml
ports:
  - "8001:8000"  # Change 8000 to 8001
```

### API Not Starting

**Check logs**:
```bash
docker-compose logs contextbridge-api
```

**Common issues**:
- Missing GEMINI_API_KEY in `.env`
- Invalid API key
- Network connectivity issues

**Solution**: Verify `.env` file has valid API key

### Frontend Not Loading

**Check logs**:
```bash
docker-compose logs contextbridge-ui
```

**Common issues**:
- Backend not ready yet
- Build failed

**Solution**: Wait for backend to be healthy, then restart frontend:
```bash
docker-compose restart contextbridge-ui
```

### Data Not Persisting

**Issue**: Vector store data lost after restart

**Solution**: Check volume mounts in `docker-compose.yml`:
```yaml
volumes:
  - ./chroma_db:/app/chroma_db
```

### Slow Build Times

**Issue**: Docker build takes too long

**Solutions**:
1. Use Docker layer caching
2. Check `.dockerignore` files
3. Increase Docker Desktop resources (CPU/Memory)

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```bash
# Required
GEMINI_API_KEY=your_api_key_here

# Optional (with defaults)
DEMO_MODE=true
CHROMA_PERSIST_DIR=./chroma_db
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
GEMINI_MODEL=gemini-2.0-flash-exp
CONFIDENCE_THRESHOLD=60
```

---

## 📁 Docker File Structure

```
contextbridge/
├── Dockerfile                 # Backend Dockerfile
├── docker-compose.yml         # Service orchestration
├── .dockerignore             # Backend build exclusions
├── .env                      # Environment variables (create from .env.example)
├── .env.example              # Environment template
├── startup.sh                # Linux/Mac startup script
├── startup.bat               # Windows startup script
└── frontend/
    ├── Dockerfile            # Frontend Dockerfile
    └── .dockerignore         # Frontend build exclusions
```

---

## 🎯 Access Points

After successful startup:

| Service | URL | Description |
|---------|-----|-------------|
| Demo Page | http://localhost:3000/demo | ⭐ Main hackathon demo |
| Dashboard | http://localhost:3000 | Stats and overview |
| Query | http://localhost:3000/query | Natural language queries |
| Graph | http://localhost:3000/graph | D3.js knowledge graph |
| Knowledge Base | http://localhost:3000/knowledge | Searchable items |
| API Docs | http://localhost:8000/docs | OpenAPI documentation |
| API Health | http://localhost:8000/api/health | Health check endpoint |

---

## 🔄 Development Workflow

### Hot Reload

Both services support hot reload:

**Backend**: Code changes automatically reload the FastAPI server

**Frontend**: For development with hot reload, use:
```bash
# Stop the Docker frontend
docker-compose stop contextbridge-ui

# Run frontend locally
cd frontend
npm start
```

### Debugging

**View real-time logs**:
```bash
docker-compose logs -f
```

**Execute commands in container**:
```bash
# Backend
docker-compose exec contextbridge-api bash

# Frontend
docker-compose exec contextbridge-ui sh
```

**Inspect container**:
```bash
docker-compose exec contextbridge-api python --version
docker-compose exec contextbridge-api pip list
```

---

## 📊 Resource Usage

**Typical resource usage**:
- Backend: ~500MB RAM, 1 CPU
- Frontend: ~200MB RAM, 0.5 CPU
- Total: ~700MB RAM, 1.5 CPU

**Recommended Docker Desktop settings**:
- Memory: 4GB minimum, 8GB recommended
- CPUs: 2 minimum, 4 recommended
- Disk: 20GB minimum

---

## 🚀 Production Deployment

### Build Production Images

```bash
# Build optimized images
docker-compose build --no-cache

# Tag images
docker tag contextbridge-api:latest your-registry/contextbridge-api:v1.0
docker tag contextbridge-ui:latest your-registry/contextbridge-ui:v1.0

# Push to registry
docker push your-registry/contextbridge-api:v1.0
docker push your-registry/contextbridge-ui:v1.0
```

### Production docker-compose.yml

```yaml
version: '3.8'

services:
  contextbridge-api:
    image: your-registry/contextbridge-api:v1.0
    restart: always
    environment:
      - DEMO_MODE=false
    # ... other production settings

  contextbridge-ui:
    image: your-registry/contextbridge-ui:v1.0
    restart: always
    # ... other production settings
```

---

## 🧹 Cleanup

### Remove All Containers and Images

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker rmi contextbridge-api contextbridge-ui

# Remove volumes (WARNING: deletes all data)
docker-compose down -v

# Remove all unused Docker resources
docker system prune -a
```

---

## 📝 Tips & Best Practices

1. **Always use `.env` file** - Never commit API keys to Git
2. **Check health before seeding** - Wait for services to be healthy
3. **Use volumes for data** - Persist important data outside containers
4. **Monitor logs** - Use `docker-compose logs -f` to debug issues
5. **Rebuild after changes** - Use `--build` flag when code changes
6. **Clean up regularly** - Remove unused images and containers

---

## 🎭 Hackathon Demo Checklist

Before your presentation:

- [ ] Docker Desktop is running
- [ ] `.env` file has valid GEMINI_API_KEY
- [ ] Run `startup.bat` (Windows) or `./startup.sh` (Mac/Linux)
- [ ] Wait for "✅ ContextBridge is running!" message
- [ ] Open http://localhost:3000/demo
- [ ] Test Scenario A (most important!)
- [ ] Check all 3 scenarios work
- [ ] Verify knowledge graph loads
- [ ] Close unnecessary browser tabs

---

## 🆘 Getting Help

**Check service status**:
```bash
docker-compose ps
```

**View all logs**:
```bash
docker-compose logs
```

**Restart everything**:
```bash
docker-compose down && docker-compose up -d --build
```

**Nuclear option** (fresh start):
```bash
docker-compose down -v
docker system prune -a
./startup.sh  # or startup.bat
```

---

## 🏆 Ready for Demo!

With Docker, ContextBridge is:
- ✅ Easy to deploy (one command)
- ✅ Consistent across environments
- ✅ Production-ready
- ✅ Easy to scale
- ✅ Easy to debug

**Good luck with your hackathon presentation!** 🎉

---

**Built for**: TechEx Hackathon 2026 - Track 4: Data & Intelligence
