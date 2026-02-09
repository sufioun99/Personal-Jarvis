# Quick Start Guide

Get Personal Jarvis up and running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Node.js 18+ installed
- API keys (at least OpenAI for basic functionality)

## Step 1: Clone and Setup (2 min)

```bash
# Clone repository
git clone https://github.com/sufioun99/Personal-Jarvis.git
cd Personal-Jarvis

# Setup environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Step 2: Install Dependencies (2 min)

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
cd ..
```

## Step 3: Start Services (1 min)

**Option A: Use startup script (recommended)**
```bash
chmod +x start.sh
./start.sh
```

**Option B: Manual start**

Terminal 1 (Backend):
```bash
python -m uvicorn backend.main:app --reload
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

## Step 4: Access Jarvis

- **UI**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Quick Test

### Via UI
1. Open http://localhost:3000
2. Select an agent (Code/DevOps/Research/General)
3. Type a message and press Send

### Via API (curl)
```bash
# Health check
curl http://localhost:8000/health

# Chat with Code Agent
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain Python decorators",
    "agent_type": "code",
    "llm_provider": "gpt-4"
  }'

# Execute safe command
curl -X POST http://localhost:8000/command/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "echo Hello Jarvis",
    "safe_mode": true
  }'

# List agents
curl http://localhost:8000/agents/list
```

### Via Python
```bash
cd examples
python example_usage.py
```

## Common Issues

### "ModuleNotFoundError"
```bash
# Make sure you installed dependencies
pip install -r requirements.txt
```

### "Cannot connect to backend"
```bash
# Make sure backend is running
# Check if port 8000 is available
lsof -i :8000
```

### "OpenAI API error"
```bash
# Check your API key in .env
cat .env | grep OPENAI_API_KEY
```

### Frontend build errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Next Steps

1. **Explore Agents**: Try different specialized agents
2. **Read API Docs**: http://localhost:8000/docs
3. **Check Examples**: `examples/` directory
4. **Deploy**: See `docs/DEPLOYMENT.md`

## Configuration

Edit `.env` to customize:
- API keys (OpenAI, Anthropic)
- Default LLM provider
- Server port
- Safety settings
- Vector DB location

## Getting Help

- 📖 [Full README](README.md)
- 🏗️ [Architecture](docs/ARCHITECTURE.md)
- 🚀 [Deployment Guide](docs/DEPLOYMENT.md)
- 💻 [API Reference](docs/API.md)
- 🤝 [Contributing](CONTRIBUTING.md)

## Available Agents

- **Code**: Programming help, debugging, refactoring
- **DevOps**: System ops, deployment, infrastructure
- **Research**: Info gathering, analysis, explanations
- **General**: Multi-purpose assistance

## Features at a Glance

✅ Multi-language speech (14+ languages)
✅ Safe command execution
✅ Multiple LLM providers
✅ Specialized AI agents
✅ Vector memory
✅ Real-time chat
✅ WebSocket support
✅ REST API

## Minimal Example

**Python:**
```python
import requests

response = requests.post('http://localhost:8000/chat', json={
    'message': 'Hello!',
    'agent_type': 'general'
})
print(response.json()['response'])
```

**JavaScript:**
```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    message: 'Hello!',
    agent_type: 'general'
  })
});
const data = await response.json();
console.log(data.response);
```

---

**You're all set!** 🎉 Start chatting with Jarvis!
