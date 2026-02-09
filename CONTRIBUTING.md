# Contributing to Personal Jarvis

Thank you for considering contributing to Personal Jarvis! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a new branch for your feature
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/Personal-Jarvis.git
cd Personal-Jarvis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-asyncio black pylint

# Install frontend dependencies
cd frontend
npm install
cd ..

# Set up environment
cp .env.example .env
# Edit .env with your API keys
```

## Code Style

### Python
- Follow PEP 8
- Use type hints
- Write docstrings for all public functions
- Use meaningful variable names
- Keep functions focused and small

```python
# Good
async def process_request(message: str, agent_type: str) -> Dict:
    """
    Process a user request through the specified agent.
    
    Args:
        message: The user's message
        agent_type: Type of agent to use
    
    Returns:
        Dictionary with response and metadata
    """
    # Implementation
```

Format code with Black:
```bash
black backend/
```

Lint with pylint:
```bash
pylint backend/
```

### JavaScript/React
- Use ES6+ features
- Use functional components with hooks
- Follow Airbnb style guide
- Use meaningful component and variable names

Format and lint:
```bash
cd frontend
npm run lint
```

## Testing

### Backend Tests

Create tests in `tests/` directory:

```python
# tests/test_agents.py
import pytest
from backend.agents.orchestrator import AgentOrchestrator

@pytest.mark.asyncio
async def test_agent_orchestrator():
    orchestrator = AgentOrchestrator()
    agents = orchestrator.get_available_agents()
    assert len(agents) > 0
    assert any(a['name'] == 'code' for a in agents)
```

Run tests:
```bash
pytest tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Adding New Features

### Adding a New Agent

1. Create agent file in `backend/agents/`:

```python
# backend/agents/my_agent.py
from .base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="my_agent",
            description="Description of what this agent does"
        )
        self.system_prompt = """Your system prompt here"""
    
    async def process(self, message, llm_provider="gpt-4", context=None):
        # Implementation
        pass
```

2. Register in orchestrator (`backend/agents/orchestrator.py`):

```python
from .my_agent import MyAgent

class AgentOrchestrator:
    def __init__(self):
        self.agents = {
            # ... existing agents
            "my_agent": MyAgent()
        }
```

3. Add to agent list and selection logic

### Adding a New LLM Provider

1. Update `backend/llm/provider.py`:

```python
def _init_clients(self):
    # Add your provider initialization
    pass

async def _call_my_provider(self, prompt, system_prompt, model, temperature, max_tokens):
    # Implementation
    pass
```

2. Add to providers dictionary and available providers list

### Adding API Endpoints

Add to `backend/main.py`:

```python
@app.post("/my/endpoint")
async def my_endpoint(request: MyRequest):
    """
    Endpoint description
    """
    try:
        # Implementation
        return {"result": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Documentation

- Update README.md for user-facing features
- Update docs/API.md for API changes
- Add inline comments for complex logic
- Write docstrings for all public functions

## Commit Messages

Use conventional commits:

```
feat: add new research agent
fix: resolve memory leak in vector store
docs: update API documentation
test: add tests for command executor
refactor: simplify agent orchestration logic
chore: update dependencies
```

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Create pull request with clear description
6. Wait for review

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests passing
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Reviewed own code
```

## Security

- Never commit API keys or secrets
- Use environment variables for sensitive data
- Validate all user inputs
- Report security vulnerabilities privately

## Questions?

Open an issue for questions or discussion!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
