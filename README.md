# JARVIS - Personal AI Assistant with Voice Control

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A sophisticated AI assistant inspired by JARVIS from Iron Man, featuring:
- 🎤 **Multi-language voice control** with wake word detection
- 🐧 **Deep Linux system integration** with natural language command execution
- 🤖 **Multi-agent AI system** with specialized agents for different tasks
- 🧠 **Multiple LLM support** (GPT-4, Claude, Gemini) with intelligent routing
- 🌐 **Comprehensive API integrations** (Search, Weather, News, Cloud services)
- 🔒 **Security-first design** with command validation and sandboxing
- 💬 **Web interface** with REST API and WebSocket support

## 🌟 Features

### Voice Interface
- **Speech-to-Text**: Multi-language support with OpenAI Whisper and Google Speech
- **Text-to-Speech**: Natural voice output with ElevenLabs or Google TTS
- **Wake Word Detection**: Activate with "Hey JARVIS"

### Natural Language Understanding
- Intent classification for various task types
- Entity extraction (file paths, package names, locations)
- Context-aware conversation handling

### Linux System Integration
- Natural language to shell command translation
- Safe command execution with whitelisting/blacklisting
- Confirmation prompts for dangerous operations
- Support for package management, process control, file operations

### AI Agent System
- **Code Agent**: Generate, debug, refactor code in any language
- **Research Agent**: Web scraping and information gathering
- **Data Analysis Agent**: Process and analyze data
- **DevOps Agent**: CI/CD and infrastructure management
- **Security Agent**: Vulnerability scanning and security audits
- **Documentation Agent**: Auto-generate docs, READMEs, API documentation

### API Integrations
- Web Search (Google, Bing)
- Weather information
- Latest news
- GitHub operations
- Cloud services (AWS, Azure, GCP)

## 🚀 Quick Start

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/sufioun99/Personal-Jarvis.git
cd Personal-Jarvis
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Basic Usage

#### Text Mode (Interactive)
```bash
python main.py --mode text
```

#### Voice Mode
```bash
python main.py --mode voice
```

#### Single Query
```bash
python main.py --query "list all files in the current directory"
```

#### API Server
```bash
python main.py --mode server
# Server runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

## 📖 Usage Examples

### System Commands
```
You: list all files in the current directory
JARVIS: [Executes 'ls -la' and shows output]

You: show disk usage
JARVIS: [Executes 'df -h' and shows disk information]

You: install package nginx
JARVIS: [Executes 'sudo apt-get install -y nginx']
```

### Code Generation
```
You: write a Python function to calculate fibonacci numbers
JARVIS: [Generates complete function with documentation]

You: debug this code [paste code]
JARVIS: [Analyzes and provides fixed version]
```

### Information Queries
```
You: what's the weather in New York?
JARVIS: [Fetches and displays current weather]

You: search for machine learning tutorials
JARVIS: [Shows top search results]

You: latest news about technology
JARVIS: [Displays recent tech news]
```

## 🏗️ Architecture

```
JARVIS/
├── core/                    # Core system components
│   ├── jarvis.py           # Main orchestrator
│   ├── llm_integration.py  # Multi-LLM support
│   ├── voice_interface.py  # Voice I/O
│   ├── nlu.py             # Natural language understanding
│   └── command_executor.py # Safe command execution
├── agents/                 # Specialized AI agents
│   ├── base_agent.py      # Base agent class
│   ├── specialized_agents.py # All specialized agents
│   └── orchestrator.py    # Agent coordination
├── api/                   # External API integrations
│   └── api_manager.py     # API client manager
├── utils/                 # Utilities
│   └── logger.py          # Logging configuration
├── config.py              # Configuration management
├── server.py              # FastAPI web server
└── main.py               # CLI entry point
```

## 🔧 Configuration

Edit `.env` file with your API keys:

```env
# Required for core functionality
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here

# Optional for voice
ELEVENLABS_API_KEY=your_key_here

# Optional for features
GOOGLE_SEARCH_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
NEWS_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here

# Safety settings
ENABLE_SUDO=False
REQUIRE_CONFIRMATION=True
COMMAND_WHITELIST=ls,cd,pwd,cat,grep,find,ps,df,free,top
```

## 🔒 Security Features

- **Command Whitelisting**: Only approved commands can be executed
- **Dangerous Command Detection**: Prompts for confirmation on risky operations
- **Blacklist**: Prevents execution of harmful commands
- **Sudo Control**: Sudo commands can be disabled
- **Input Validation**: All inputs are sanitized and validated
- **API Key Security**: Keys stored in environment variables, never in code

## 🧪 Testing

Run tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

## 🛠️ API Documentation

When running in server mode, visit:
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### REST API Endpoints

- `POST /query` - Process a text query
- `POST /agent/execute` - Execute task with specific agent
- `GET /agent/status` - Get agent status
- `GET /conversation/history` - Get conversation history
- `DELETE /conversation/clear` - Clear history
- `WS /ws` - WebSocket for real-time communication

### Example API Call

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={
        "query": "list all files",
        "voice_output": False
    }
)
print(response.json())
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude
- Google for Gemini and various APIs
- ElevenLabs for high-quality TTS
- FastAPI for the excellent web framework

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the documentation
- Review existing issues

## 🗺️ Roadmap

- [ ] Docker containerization
- [ ] Kubernetes deployment support
- [ ] Enhanced memory system with vector DB
- [ ] Plugin system for custom agents
- [ ] Mobile app interface
- [ ] Multi-user support
- [ ] Fine-tuned models for specific tasks
- [ ] Integration with more cloud services
- [ ] Advanced scheduling capabilities
- [ ] Voice biometric authentication

## ⚠️ Disclaimer

This is an AI assistant that can execute system commands. Always review commands before execution, especially in production environments. The developers are not responsible for any damage caused by improper use.

---

**Made with ❤️ for the AI community** 
