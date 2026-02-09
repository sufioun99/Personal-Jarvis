# Docker Quick Start

## Prerequisites

- Docker installed
- Docker Compose installed
- API keys configured in `.env`

## Build and Run

### Using Docker Compose (Recommended)

1. **Setup environment**:
```bash
cp .env.example .env
# Edit .env with your API keys
```

2. **Build and start**:
```bash
docker-compose up -d
```

3. **View logs**:
```bash
docker-compose logs -f jarvis
```

4. **Stop**:
```bash
docker-compose down
```

### Using Docker Directly

1. **Build image**:
```bash
docker build -t jarvis-ai .
```

2. **Run container**:
```bash
docker run -d \
  --name jarvis \
  -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/logs:/app/logs \
  jarvis-ai
```

3. **View logs**:
```bash
docker logs -f jarvis
```

4. **Stop container**:
```bash
docker stop jarvis
docker rm jarvis
```

## Access JARVIS

Once running, access:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Test API

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "hello jarvis", "voice_output": false}'
```

## Interactive Mode

Run JARVIS in text mode:
```bash
docker exec -it jarvis python main.py --mode text
```

## Troubleshooting

### Container won't start
- Check logs: `docker-compose logs jarvis`
- Verify API keys in `.env`
- Ensure ports are not in use

### API errors
- Check that all required API keys are set
- Verify network connectivity
- Check container logs for details

### Permission issues
```bash
sudo chown -R $USER:$USER logs/
```

## Production Deployment

For production:

1. **Use secrets management** (not .env):
```bash
docker secret create openai_key -
docker secret create anthropic_key -
```

2. **Enable proper logging**:
- Configure log rotation
- Use external log aggregation

3. **Set resource limits**:
```yaml
services:
  jarvis:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

4. **Use reverse proxy** (nginx/traefik):
- SSL/TLS termination
- Rate limiting
- Load balancing

## Environment Variables

Required:
- `OPENAI_API_KEY`

Optional:
- `ANTHROPIC_API_KEY`
- `GOOGLE_API_KEY`
- `ELEVENLABS_API_KEY`
- `JARVIS_HOST` (default: 0.0.0.0)
- `JARVIS_PORT` (default: 8000)
- `LOG_LEVEL` (default: INFO)

See `.env.example` for all options.
