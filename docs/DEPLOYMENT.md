# Deployment Guide

## Prerequisites

- Python 3.8+
- Node.js 18+
- Sufficient RAM (2GB+ recommended)
- API keys (OpenAI and/or Anthropic)

## Environment Setup

### Production Environment Variables

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=False

# CORS (restrict in production)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Database
VECTOR_DB_PATH=/var/lib/jarvis/chroma_db

# Security
SAFE_MODE_DEFAULT=True
COMMAND_TIMEOUT=30

# LLM
DEFAULT_LLM_PROVIDER=gpt-4
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=2000
```

## Deployment Options

### Option 1: Direct Deployment

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   cd frontend && npm install && npm run build
   ```

2. **Start backend with production server**
   ```bash
   pip install gunicorn
   gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

3. **Serve frontend with Nginx**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           root /path/to/Personal-Jarvis/frontend/dist;
           try_files $uri $uri/ /index.html;
       }

       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### Option 2: Docker Deployment

Create `Dockerfile`:

```dockerfile
# Backend
FROM python:3.11-slim as backend

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ backend/
EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./chroma_db:/app/chroma_db
    restart: unless-stopped

  frontend:
    image: node:18-alpine
    working_dir: /app
    volumes:
      - ./frontend:/app
    command: sh -c "npm install && npm run build && npx serve -s dist -l 3000"
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped
```

Run with:
```bash
docker-compose up -d
```

### Option 3: Systemd Service

Create `/etc/systemd/system/jarvis-backend.service`:

```ini
[Unit]
Description=Personal Jarvis Backend
After=network.target

[Service]
Type=simple
User=jarvis
WorkingDirectory=/opt/personal-jarvis
Environment="PATH=/opt/personal-jarvis/venv/bin"
ExecStart=/opt/personal-jarvis/venv/bin/gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable jarvis-backend
sudo systemctl start jarvis-backend
```

## Security Considerations

1. **API Keys**: Never commit API keys to version control
2. **CORS**: Restrict CORS origins in production
3. **Rate Limiting**: Implement rate limiting for public APIs
4. **Authentication**: Add authentication for production use
5. **HTTPS**: Always use HTTPS in production
6. **Command Execution**: Keep safe mode enabled
7. **Input Validation**: Validate all user inputs
8. **Logging**: Implement proper logging and monitoring

## Monitoring

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "components": {
    "orchestrator": "active",
    "speech_recognizer": "active",
    "llm_provider": "active",
    "vector_memory": "active",
    "command_executor": "active"
  }
}
```

### Logging

Backend logs are printed to stdout. In production:

```python
# Add to backend/main.py
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/jarvis/app.log'),
        logging.StreamHandler()
    ]
)
```

## Scaling

### Horizontal Scaling

Use a load balancer (Nginx/HAProxy) to distribute traffic across multiple backend instances:

```nginx
upstream jarvis_backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    location /api {
        proxy_pass http://jarvis_backend;
    }
}
```

### Database Scaling

For vector database scaling, consider:
- Persistent volume for Docker
- Shared storage for multiple instances
- Regular backups

## Backup and Recovery

### Backup Vector Database

```bash
# Backup
tar -czf chroma_db_backup_$(date +%Y%m%d).tar.gz chroma_db/

# Restore
tar -xzf chroma_db_backup_YYYYMMDD.tar.gz
```

### Backup Configuration

```bash
# Backup environment
cp .env .env.backup
```

## Troubleshooting

### Backend not starting
- Check API keys are set
- Verify Python version (3.8+)
- Check port 8000 is available

### Speech recognition not working
- Verify OpenAI API key
- Check audio file format (WAV supported)
- Ensure sufficient API quota

### Memory issues
- Monitor ChromaDB size
- Implement memory cleanup routines
- Increase available RAM

### Performance issues
- Use gunicorn with multiple workers
- Enable caching for LLM responses
- Optimize vector database queries

## Production Checklist

- [ ] Set DEBUG=False
- [ ] Configure CORS origins
- [ ] Set up HTTPS
- [ ] Implement authentication
- [ ] Configure rate limiting
- [ ] Set up monitoring and logging
- [ ] Configure backups
- [ ] Test disaster recovery
- [ ] Set up health checks
- [ ] Configure firewall rules
- [ ] Review security settings
- [ ] Set up CI/CD pipeline
