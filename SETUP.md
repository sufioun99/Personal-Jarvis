# JARVIS Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)
- API keys for services you want to use

## Step-by-Step Installation

### 1. System Dependencies

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv portaudio19-dev
```

#### macOS
```bash
brew install portaudio
```

#### Windows
- Install Python from python.org
- Install PyAudio from wheel: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

### 2. Clone Repository

```bash
git clone https://github.com/sufioun99/Personal-Jarvis.git
cd Personal-Jarvis
```

### 3. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure API Keys

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your API keys:
```bash
nano .env  # or use your preferred editor
```

### Required API Keys

#### OpenAI (Required for core functionality)
- Get API key from: https://platform.openai.com/api-keys
- Add to `.env`: `OPENAI_API_KEY=sk-...`

#### Anthropic Claude (Optional but recommended)
- Get API key from: https://console.anthropic.com/
- Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

#### Google AI (Optional)
- Get API key from: https://makersuite.google.com/app/apikey
- Add to `.env`: `GOOGLE_API_KEY=...`

#### ElevenLabs (Optional, for high-quality TTS)
- Get API key from: https://elevenlabs.io/
- Add to `.env`: `ELEVENLABS_API_KEY=...`

#### Google Custom Search (Optional, for web search)
- Create project: https://console.cloud.google.com/
- Enable Custom Search API
- Create API key and Search Engine ID
- Add to `.env`:
  ```
  GOOGLE_SEARCH_API_KEY=...
  GOOGLE_SEARCH_ENGINE_ID=...
  ```

#### OpenWeatherMap (Optional, for weather)
- Get API key from: https://openweathermap.org/api
- Add to `.env`: `OPENWEATHER_API_KEY=...`

#### NewsAPI (Optional, for news)
- Get API key from: https://newsapi.org/
- Add to `.env`: `NEWS_API_KEY=...`

### 6. Test Installation

Run basic tests to verify setup:
```bash
pytest tests/ -v
```

### 7. Test JARVIS

Try a simple command:
```bash
python main.py --query "hello, how are you?"
```

## Configuration Options

### Safety Settings

Edit `.env` to configure safety features:

```env
# Enable/disable sudo commands
ENABLE_SUDO=False

# Require confirmation for dangerous commands
REQUIRE_CONFIRMATION=True

# Whitelist of allowed commands (comma-separated)
COMMAND_WHITELIST=ls,cd,pwd,cat,grep,find,ps,df,free,top,htop
```

### Wake Word

Change the wake word:
```env
WAKE_WORD=hey jarvis
```

### Logging

Configure logging level:
```env
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=jarvis.log
```

## Running JARVIS

### Text Mode (Interactive)
```bash
python main.py --mode text
```

### Voice Mode
```bash
python main.py --mode voice
```

### Server Mode (API)
```bash
python main.py --mode server
```

Access API docs at: http://localhost:8000/docs

### Single Query
```bash
python main.py --query "your question here"
```

## Troubleshooting

### Import Errors
If you get import errors, ensure you're in the virtual environment:
```bash
source venv/bin/activate
```

### Audio Issues
If voice features don't work:
- Check microphone permissions
- Test microphone: `python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"`
- Install PortAudio: Ubuntu: `sudo apt-get install portaudio19-dev`

### API Key Issues
- Verify keys are correctly set in `.env`
- Check that `.env` is in the project root directory
- Restart JARVIS after changing `.env`

### Permission Errors
If command execution fails:
- Check `ENABLE_SUDO` setting
- Verify commands are in whitelist
- Review `REQUIRE_CONFIRMATION` setting

## Next Steps

- Read the [Usage Guide](USAGE.md)
- Check out [Examples](examples/)
- Join our community
- Contribute to the project

## Getting Help

- Open an issue on GitHub
- Check existing issues
- Review documentation
- Read the FAQ

## Security Best Practices

1. **Never commit `.env` file** - It contains sensitive API keys
2. **Use command whitelist** - Restrict which commands can be executed
3. **Enable confirmations** - For dangerous operations
4. **Disable sudo** - Unless absolutely necessary
5. **Review logs** - Monitor what commands are being executed
6. **Limit API keys** - Use keys with minimal required permissions
7. **Keep updated** - Regularly update dependencies

## Performance Tips

1. **Use appropriate models** - Smaller models for simple tasks
2. **Cache responses** - API responses are cached automatically
3. **Limit context** - Conversation history is limited to recent messages
4. **Parallel execution** - Independent tasks run in parallel

## Advanced Configuration

### Custom Agents

You can create custom agents by extending `BaseAgent`:

```python
from agents.base_agent import BaseAgent

class CustomAgent(BaseAgent):
    def __init__(self):
        super().__init__("CustomAgent", "My custom agent")
    
    async def execute(self, task):
        # Your implementation
        pass
```

### Custom API Integrations

Add new API integrations in `api/api_manager.py`:

```python
async def custom_api_call(self, params):
    # Your API integration
    pass
```

### Environment-Specific Settings

Use different `.env` files for different environments:
- `.env.development`
- `.env.production`
- `.env.testing`

Load with: `export ENV_FILE=.env.production`
