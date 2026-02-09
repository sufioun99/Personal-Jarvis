# Personal Jarvis - Voice AI Assistant

A comprehensive voice-enabled AI assistant with multi-language speech recognition, Linux command execution, multi-LLM support, specialized AI agents, and vector database memory.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Node](https://img.shields.io/badge/node-18+-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## 🌟 Features

- **🎤 Multi-Language Speech Recognition**: Support for 14+ languages using OpenAI Whisper
- **💻 Safe Linux Command Execution**: Execute commands with built-in safety checks
- **🤖 Multi-LLM Support**: Choose between GPT-4, Claude, and other models
- **🔧 Specialized AI Agents**: 
  - **Code Agent**: Code analysis, generation, debugging, refactoring
  - **DevOps Agent**: System operations, deployments, infrastructure
  - **Research Agent**: Information gathering and analysis
  - **General Agent**: General purpose assistance
- **🧠 Vector Database Memory**: Persistent conversation memory using ChromaDB
- **⚡ FastAPI Backend**: High-performance async API
- **💎 React UI**: Modern, responsive user interface
- **🔒 Safe System Operations**: Built-in security checks for command execution
- **🎯 Agent Orchestration**: Intelligent routing to specialized agents

## 🏗️ Architecture

```
Personal-Jarvis/
├── backend/              # FastAPI backend
│   ├── agents/          # Specialized AI agents
│   │   ├── orchestrator.py
│   │   ├── code_agent.py
│   │   ├── devops_agent.py
│   │   ├── research_agent.py
│   │   └── general_agent.py
│   ├── llm/             # Multi-LLM provider
│   ├── speech/          # Speech recognition
│   ├── memory/          # Vector database
│   ├── system/          # Command execution
│   └── main.py          # FastAPI app
├── frontend/            # React UI
│   └── src/
└── requirements.txt     # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- OpenAI API key (for GPT-4 and speech recognition)
- Anthropic API key (optional, for Claude models)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/sufioun99/Personal-Jarvis.git
   cd Personal-Jarvis
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **Install backend dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

1. **Start the backend server**
   ```bash
   python -m backend.main
   # or
   uvicorn backend.main:app --reload
   ```
   The API will be available at `http://localhost:8000`

2. **Start the frontend development server**
   ```bash
   cd frontend
   npm run dev
   ```
   The UI will be available at `http://localhost:3000`

## 📖 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /chat` - Send messages to AI agents
- `POST /speech/transcribe` - Transcribe audio to text
- `POST /command/execute` - Execute Linux commands
- `GET /agents/list` - List available agents
- `GET /llm/providers` - List available LLM providers
- `WS /ws/chat` - WebSocket for real-time chat

## 🎯 Usage Examples

### Chat with AI Agent

```python
import requests

response = requests.post('http://localhost:8000/chat', json={
    'message': 'Explain how to optimize a Python function',
    'agent_type': 'code',
    'llm_provider': 'gpt-4'
})
print(response.json()['response'])
```

### Execute Linux Command

```python
response = requests.post('http://localhost:8000/command/execute', json={
    'command': 'ls -la',
    'safe_mode': True
})
print(response.json()['output'])
```

### Transcribe Audio

```python
with open('audio.wav', 'rb') as audio_file:
    files = {'audio': audio_file}
    response = requests.post(
        'http://localhost:8000/speech/transcribe?language=en',
        files=files
    )
    print(response.json()['text'])
```

## 🔧 Configuration

Edit `.env` file to configure:

```bash
# API Keys
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Server
HOST=0.0.0.0
PORT=8000

# LLM Settings
DEFAULT_LLM_PROVIDER=gpt-4
DEFAULT_TEMPERATURE=0.7
DEFAULT_MAX_TOKENS=2000

# Safety
SAFE_MODE_DEFAULT=True
COMMAND_TIMEOUT=30
```

## 🤖 Specialized Agents

### Code Agent
- Code analysis and review
- Code generation and refactoring
- Debugging and troubleshooting
- Best practices guidance

### DevOps Agent
- System administration
- CI/CD pipeline help
- Container orchestration
- Infrastructure management

### Research Agent
- Information gathering
- Data analysis
- Technical explanations
- Research synthesis

### General Agent
- General purpose assistance
- Task planning
- Question answering

## 🔒 Security Features

- **Safe Mode**: Blocks dangerous commands (rm -rf /, mkfs, etc.)
- **Command Validation**: Pattern-based safety checks
- **Timeout Protection**: Commands timeout after configured duration
- **API Key Management**: Environment-based credential storage

## 🌍 Supported Languages (Speech Recognition)

English, Spanish, French, German, Italian, Portuguese, Dutch, Russian, Chinese, Japanese, Korean, Arabic, Hindi, and auto-detection

## 🛠️ Development

### Backend Testing
```bash
pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

### Linting
```bash
# Python
pylint backend/

# JavaScript
cd frontend
npm run lint
```

## 📦 Deployment

### Docker (Coming Soon)
```bash
docker-compose up
```

### Production
1. Set `DEBUG=False` in `.env`
2. Configure CORS origins appropriately
3. Use a production WSGI server (e.g., Gunicorn)
4. Set up reverse proxy (e.g., Nginx)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- OpenAI for GPT-4 and Whisper
- Anthropic for Claude
- FastAPI for the excellent web framework
- ChromaDB for vector storage
- React and Vite for the frontend

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

Built with ❤️ for the AI community 
