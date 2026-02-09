# Personal Jarvis Examples

This directory contains example code demonstrating how to use Personal Jarvis.

## Examples

### Python Client Example

```bash
# Make sure the backend is running
python examples/example_usage.py
```

Demonstrates:
- Listing available agents
- Listing LLM providers
- Chatting with different agents
- Executing Linux commands
- Handling errors

### JavaScript/Node.js Example

```bash
# Make sure the backend is running
node examples/example_usage.js
```

Demonstrates:
- Using the API with fetch
- Async/await patterns
- Error handling
- Real-time chat setup

## Running the Examples

1. **Start the backend:**
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

2. **Configure API keys:**
   Make sure your `.env` file has valid API keys:
   ```bash
   OPENAI_API_KEY=your_key
   ANTHROPIC_API_KEY=your_key
   ```

3. **Run an example:**
   ```bash
   # Python
   python examples/example_usage.py
   
   # JavaScript
   node examples/example_usage.js
   ```

## Example Use Cases

### Code Analysis
```python
result = chat_with_agent(
    "Review this Python code and suggest improvements: ...",
    agent_type="code"
)
```

### System Operations
```python
result = execute_command("df -h")
print(result['output'])
```

### Research and Analysis
```python
result = chat_with_agent(
    "Compare different machine learning frameworks",
    agent_type="research"
)
```

### DevOps Assistance
```python
result = chat_with_agent(
    "How do I set up CI/CD with GitHub Actions?",
    agent_type="devops"
)
```

## Integration Examples

See the `docs/API.md` file for more detailed API documentation and integration examples.
