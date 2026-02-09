# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (React)                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐    │
│  │    Chat    │  │   Agent    │  │   Voice Input      │    │
│  │ Interface  │  │ Selection  │  │   (Microphone)     │    │
│  └────────────┘  └────────────┘  └────────────────────┘    │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/WebSocket
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (Python)                   │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                    Main API Router                     │  │
│  │  /chat  /speech  /command  /agents  /llm/providers   │  │
│  └───────────────────────────────────────────────────────┘  │
│                            │                                 │
│  ┌────────────────────────┴─────────────────────────────┐  │
│  │                                                        │  │
│  ▼                   ▼                ▼                  ▼  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Agent   │  │  Speech  │  │   LLM    │  │  Memory  │  │
│  │Orchestr. │  │Recognizer│  │ Provider │  │  Vector  │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│       │              │              │              │        │
│       ▼              ▼              ▼              ▼        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   Code   │  │ OpenAI   │  │  OpenAI  │  │ ChromaDB │  │
│  │  Agent   │  │ Whisper  │  │   API    │  │  Store   │  │
│  ├──────────┤  └──────────┘  ├──────────┤  └──────────┘  │
│  │ DevOps   │                 │Anthropic │                 │
│  │  Agent   │                 │   API    │                 │
│  ├──────────┤                 └──────────┘                 │
│  │ Research │                                               │
│  │  Agent   │                                               │
│  ├──────────┤                                               │
│  │ General  │       ┌──────────┐                           │
│  │  Agent   │       │ Command  │                           │
│  └──────────┘       │Executor  │                           │
│                     └──────────┘                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Linux System  │
                    │   Commands    │
                    └───────────────┘
```

## Component Details

### Frontend Layer
- **React UI**: Modern, responsive interface
- **Chat Interface**: Real-time message display
- **Agent Selection**: Choose specialized agents
- **Voice Input**: Microphone integration (placeholder)
- **Settings**: LLM provider and language selection

### API Layer (FastAPI)
- **REST Endpoints**: Chat, speech, commands, metadata
- **WebSocket**: Real-time bidirectional communication
- **CORS Middleware**: Cross-origin support
- **Request Validation**: Pydantic models

### Agent Orchestration
- **Orchestrator**: Routes requests to appropriate agents
- **Code Agent**: Programming assistance
- **DevOps Agent**: System operations
- **Research Agent**: Information gathering
- **General Agent**: General purpose tasks

### LLM Integration
- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude 3 Opus, Sonnet, Claude 2
- **Unified Interface**: Abstract provider differences
- **Error Handling**: Graceful fallbacks

### Speech Recognition
- **OpenAI Whisper**: Multi-language transcription
- **14+ Languages**: Auto-detection support
- **Audio Processing**: WAV format support

### Vector Memory
- **ChromaDB**: Persistent vector storage
- **Embeddings**: Semantic search
- **Context Retrieval**: Relevant history
- **Conversation Storage**: User/assistant messages

### Command Execution
- **Safety Checks**: Pattern-based blocking
- **Timeout Protection**: Configurable limits
- **Output Capture**: stdout/stderr
- **Error Handling**: Graceful failures

## Data Flow

### Chat Request Flow
```
User Input → Frontend
    ↓
HTTP POST /chat
    ↓
FastAPI Router
    ↓
Agent Orchestrator
    ↓
Selected Agent (Code/DevOps/Research/General)
    ↓
LLM Provider (OpenAI/Anthropic)
    ↓
Vector Memory (Context Storage)
    ↓
Response → Frontend → User
```

### Speech Recognition Flow
```
Audio File → Frontend
    ↓
HTTP POST /speech/transcribe
    ↓
Speech Recognizer
    ↓
OpenAI Whisper API
    ↓
Transcribed Text → Frontend → User
```

### Command Execution Flow
```
Command → Frontend
    ↓
HTTP POST /command/execute
    ↓
Command Executor
    ↓
Safety Validation
    ↓
Linux Shell Execution
    ↓
Output Capture → Frontend → User
```

## Security Model

### Input Validation
- Pydantic models for request validation
- Type checking and constraints
- Sanitization of user inputs

### Command Safety
- Dangerous pattern blocking
- Whitelist/blacklist approach
- Timeout protection
- Safe mode by default

### API Security
- Environment-based API keys
- No key exposure in responses
- Rate limiting (to be implemented)
- CORS configuration

### Data Privacy
- Local vector storage
- No conversation logging (unless configured)
- Secure API key management

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Load balancer ready
- Shared vector storage

### Performance
- Async/await throughout
- Connection pooling
- Efficient vector queries

### Resource Management
- Configurable timeouts
- Memory limits
- Connection limits

## Extension Points

### Adding New Agents
1. Inherit from BaseAgent
2. Implement process() method
3. Register in orchestrator
4. Update UI agent list

### Adding New LLM Providers
1. Add client initialization
2. Implement provider method
3. Register in providers dict
4. Update available providers

### Adding New Features
- New API endpoints in main.py
- New React components
- New agent capabilities
- Integration with external services

## Technology Stack

**Backend:**
- FastAPI 0.104+
- Python 3.8+
- Pydantic for validation
- ChromaDB for vectors
- OpenAI/Anthropic SDKs

**Frontend:**
- React 18
- Vite build tool
- Lucide React icons
- Modern CSS

**Infrastructure:**
- Uvicorn ASGI server
- WebSocket support
- Environment-based config

## Deployment Architecture

```
Internet
    ↓
[Load Balancer / Reverse Proxy]
    ↓
┌────────────────────────┐
│  Frontend (Nginx)      │
│  Static Files          │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│  Backend Instances     │
│  (Gunicorn+Uvicorn)    │
│  ┌──────────────────┐  │
│  │   Instance 1     │  │
│  │   Instance 2     │  │
│  │   Instance N     │  │
│  └──────────────────┘  │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│  Shared Storage        │
│  - Vector DB           │
│  - Logs                │
└────────────────────────┘
```

## Monitoring Points

- API endpoint latency
- LLM response times
- Vector database query performance
- Memory usage
- Error rates
- Command execution counts
- Agent selection distribution

## Future Enhancements

- WebRTC for real-time voice
- User authentication
- Rate limiting
- Caching layer
- Additional LLM providers
- More specialized agents
- Plugin system
- Mobile app
