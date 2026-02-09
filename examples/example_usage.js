// Example: Using Personal Jarvis API with JavaScript/Node.js

const API_URL = 'http://localhost:8000';

// Chat with an agent
async function chatWithAgent(message, agentType = 'general', llmProvider = 'gpt-4') {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      agent_type: agentType,
      llm_provider: llmProvider,
    }),
  });
  return await response.json();
}

// List available agents
async function listAvailableAgents() {
  const response = await fetch(`${API_URL}/agents/list`);
  return await response.json();
}

// List LLM providers
async function listLLMProviders() {
  const response = await fetch(`${API_URL}/llm/providers`);
  return await response.json();
}

// Execute command
async function executeCommand(command, safeMode = true) {
  const response = await fetch(`${API_URL}/command/execute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ command, safe_mode: safeMode }),
  });
  return await response.json();
}

// Main examples
async function main() {
  console.log('🤖 Personal Jarvis API Examples\n');

  try {
    // Example 1: List available agents
    console.log('1. Available Agents:');
    const agents = await listAvailableAgents();
    agents.agents.forEach((agent) => {
      console.log(`   - ${agent.name}: ${agent.description}`);
    });
    console.log();

    // Example 2: List LLM providers
    console.log('2. Available LLM Providers:');
    const providers = await listLLMProviders();
    providers.providers.forEach((provider) => {
      console.log(`   - ${provider.name} (${provider.provider})`);
    });
    console.log();

    // Example 3: Code Agent
    console.log('3. Ask Code Agent about JavaScript:');
    const codeResult = await chatWithAgent(
      'How do I implement async/await error handling in JavaScript?',
      'code',
      'gpt-4'
    );
    console.log(`   Response: ${codeResult.response.substring(0, 200)}...`);
    console.log(`   Agent used: ${codeResult.agent_used}`);
    console.log();

    // Example 4: DevOps Agent
    console.log('4. Ask DevOps Agent about Kubernetes:');
    const devopsResult = await chatWithAgent(
      'What are Kubernetes deployment strategies?',
      'devops'
    );
    console.log(`   Response: ${devopsResult.response.substring(0, 200)}...`);
    console.log();

    // Example 5: Research Agent
    console.log('5. Ask Research Agent to compare technologies:');
    const researchResult = await chatWithAgent(
      'Compare SQL vs NoSQL databases',
      'research'
    );
    console.log(`   Response: ${researchResult.response.substring(0, 200)}...`);
    console.log();

    // Example 6: Execute a command
    console.log('6. Execute Linux command:');
    const cmdResult = await executeCommand('date');
    if (cmdResult.success) {
      console.log(`   Output: ${cmdResult.output.trim()}`);
    } else {
      console.log(`   Error: ${cmdResult.error}`);
    }
    console.log();

    // Example 7: WebSocket connection (real-time chat)
    console.log('7. WebSocket connection example:');
    console.log('   (See example_websocket.js for WebSocket implementation)');
    console.log();

  } catch (error) {
    if (error.code === 'ECONNREFUSED') {
      console.error('❌ Error: Cannot connect to backend. Make sure it\'s running on http://localhost:8000');
    } else {
      console.error('❌ Error:', error.message);
    }
  }
}

// Run examples
main();
