"""
Example: Using Personal Jarvis API with Python
"""
import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"

def chat_with_agent(message, agent_type="general", llm_provider="gpt-4"):
    """Send a message to a specific agent"""
    response = requests.post(
        f"{BASE_URL}/chat",
        json={
            "message": message,
            "agent_type": agent_type,
            "llm_provider": llm_provider
        }
    )
    return response.json()

def list_available_agents():
    """Get list of available agents"""
    response = requests.get(f"{BASE_URL}/agents/list")
    return response.json()

def list_llm_providers():
    """Get list of available LLM providers"""
    response = requests.get(f"{BASE_URL}/llm/providers")
    return response.json()

def execute_command(command, safe_mode=True):
    """Execute a Linux command"""
    response = requests.post(
        f"{BASE_URL}/command/execute",
        json={
            "command": command,
            "safe_mode": safe_mode
        }
    )
    return response.json()

def transcribe_audio(audio_path, language="en"):
    """Transcribe audio file to text"""
    with open(audio_path, 'rb') as audio_file:
        files = {'audio': audio_file}
        response = requests.post(
            f"{BASE_URL}/speech/transcribe",
            files=files,
            params={"language": language}
        )
    return response.json()

def main():
    print("🤖 Personal Jarvis API Examples\n")
    
    # Example 1: List available agents
    print("1. Available Agents:")
    agents = list_available_agents()
    for agent in agents['agents']:
        print(f"   - {agent['name']}: {agent['description']}")
    print()
    
    # Example 2: List LLM providers
    print("2. Available LLM Providers:")
    providers = list_llm_providers()
    for provider in providers['providers']:
        print(f"   - {provider['name']} ({provider['provider']})")
    print()
    
    # Example 3: Code Agent
    print("3. Ask Code Agent about Python optimization:")
    result = chat_with_agent(
        "How do I optimize a Python function that processes large lists?",
        agent_type="code",
        llm_provider="gpt-4"
    )
    print(f"   Response: {result['response'][:200]}...")
    print(f"   Agent used: {result['agent_used']}")
    print()
    
    # Example 4: DevOps Agent
    print("4. Ask DevOps Agent about Docker:")
    result = chat_with_agent(
        "How do I create a multi-stage Docker build?",
        agent_type="devops"
    )
    print(f"   Response: {result['response'][:200]}...")
    print()
    
    # Example 5: Research Agent
    print("5. Ask Research Agent to explain a concept:")
    result = chat_with_agent(
        "Explain the difference between REST and GraphQL APIs",
        agent_type="research"
    )
    print(f"   Response: {result['response'][:200]}...")
    print()
    
    # Example 6: Execute a safe command
    print("6. Execute Linux command:")
    result = execute_command("echo 'Hello from Jarvis'")
    if result['success']:
        print(f"   Output: {result['output'].strip()}")
    else:
        print(f"   Error: {result['error']}")
    print()
    
    # Example 7: Try to execute a dangerous command (will be blocked)
    print("7. Try to execute dangerous command (will be blocked):")
    result = execute_command("rm -rf /", safe_mode=True)
    if not result['success']:
        print(f"   Blocked: {result['error']}")
    print()

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to backend. Make sure it's running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")
