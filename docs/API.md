# API Integration Guide

Personal Jarvis provides a comprehensive REST API for integrating with other applications.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API is open. For production, implement authentication middleware.

## Endpoints

### Chat with AI Agents

**POST** `/chat`

Send messages to specialized AI agents.

**Request:**
```json
{
  "message": "How do I optimize a Python function?",
  "agent_type": "code",
  "llm_provider": "gpt-4",
  "language": "en"
}
```

**Response:**
```json
{
  "response": "To optimize a Python function...",
  "agent_used": "code",
  "metadata": {
    "llm_provider": "gpt-4",
    "context_used": 3
  }
}
```

### Speech Transcription

**POST** `/speech/transcribe?language=en`

Transcribe audio files to text.

**Request:**
- Form data with audio file
- Query parameter: `language` (optional, default: "en")

**Response:**
```json
{
  "text": "Hello, how can I help you today?",
  "language": "en"
}
```

### Command Execution

**POST** `/command/execute`

Execute Linux commands with safety checks.

**Request:**
```json
{
  "command": "ls -la /tmp",
  "safe_mode": true
}
```

**Response:**
```json
{
  "success": true,
  "output": "total 8\ndrwxrwxrwt...",
  "error": null
}
```

### List Agents

**GET** `/agents/list`

Get available specialized agents.

**Response:**
```json
{
  "agents": [
    {
      "name": "code",
      "description": "Code analysis, generation, debugging, and refactoring",
      "capabilities": ["analyze", "generate", "debug", "refactor", "review"]
    }
  ]
}
```

### List LLM Providers

**GET** `/llm/providers`

Get available LLM providers.

**Response:**
```json
{
  "providers": [
    {
      "name": "gpt-4",
      "provider": "OpenAI",
      "description": "Most capable GPT-4 model"
    }
  ]
}
```

### WebSocket Chat

**WS** `/ws/chat`

Real-time chat via WebSocket.

**Message Format:**
```json
{
  "message": "Hello",
  "agent_type": "general",
  "llm_provider": "gpt-4"
}
```

## Error Handling

All endpoints return standard HTTP status codes:
- 200: Success
- 400: Bad Request
- 500: Internal Server Error

Error response format:
```json
{
  "detail": "Error message"
}
```

## Rate Limiting

Not currently implemented. Consider adding rate limiting for production.

## Python Client Example

```python
import requests

class JarvisClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def chat(self, message, agent="general", llm="gpt-4"):
        response = requests.post(
            f"{self.base_url}/chat",
            json={
                "message": message,
                "agent_type": agent,
                "llm_provider": llm
            }
        )
        return response.json()
    
    def transcribe(self, audio_path, language="en"):
        with open(audio_path, 'rb') as f:
            files = {'audio': f}
            response = requests.post(
                f"{self.base_url}/speech/transcribe",
                params={"language": language},
                files=files
            )
        return response.json()
    
    def execute_command(self, command, safe_mode=True):
        response = requests.post(
            f"{self.base_url}/command/execute",
            json={
                "command": command,
                "safe_mode": safe_mode
            }
        )
        return response.json()

# Usage
client = JarvisClient()
result = client.chat("Explain async/await in Python", agent="code")
print(result['response'])
```

## JavaScript Client Example

```javascript
class JarvisClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }

  async chat(message, agent = 'general', llm = 'gpt-4') {
    const response = await fetch(`${this.baseUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        agent_type: agent,
        llm_provider: llm,
      }),
    });
    return await response.json();
  }

  async transcribe(audioFile, language = 'en') {
    const formData = new FormData();
    formData.append('audio', audioFile);
    
    const response = await fetch(
      `${this.baseUrl}/speech/transcribe?language=${language}`,
      {
        method: 'POST',
        body: formData,
      }
    );
    return await response.json();
  }

  async executeCommand(command, safeMode = true) {
    const response = await fetch(`${this.baseUrl}/command/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        command,
        safe_mode: safeMode,
      }),
    });
    return await response.json();
  }
}

// Usage
const client = new JarvisClient();
const result = await client.chat('How do I deploy to Kubernetes?', 'devops');
console.log(result.response);
```
