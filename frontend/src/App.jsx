import React, { useState, useEffect, useRef } from 'react';
import { Mic, Send, Terminal, Bot, Settings, MessageSquare } from 'lucide-react';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [selectedAgent, setSelectedAgent] = useState('general');
  const [selectedLLM, setSelectedLLM] = useState('gpt-4');
  const [agents, setAgents] = useState([]);
  const [llmProviders, setLLMProviders] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // Load available agents and LLM providers
    fetchAgents();
    fetchLLMProviders();
  }, []);

  useEffect(() => {
    // Scroll to bottom when messages change
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const fetchAgents = async () => {
    try {
      const response = await fetch(`${API_URL}/agents/list`);
      const data = await response.json();
      setAgents(data.agents || []);
    } catch (error) {
      console.error('Error fetching agents:', error);
    }
  };

  const fetchLLMProviders = async () => {
    try {
      const response = await fetch(`${API_URL}/llm/providers`);
      const data = await response.json();
      setLLMProviders(data.providers || []);
    } catch (error) {
      console.error('Error fetching LLM providers:', error);
    }
  };

  const sendMessage = async (e) => {
    e?.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input,
          agent_type: selectedAgent,
          llm_provider: selectedLLM
        })
      });

      const data = await response.json();

      const assistantMessage = {
        role: 'assistant',
        content: data.response,
        agent: data.agent_used,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, there was an error processing your request.',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const startRecording = async () => {
    setIsRecording(true);
    // Speech recognition implementation would go here
    // For now, just a placeholder
    setTimeout(() => {
      setIsRecording(false);
    }, 3000);
  };

  return (
    <div className="app">
      <div className="sidebar">
        <div className="sidebar-header">
          <Bot size={32} />
          <h1>Personal Jarvis</h1>
        </div>

        <div className="sidebar-section">
          <h3>
            <MessageSquare size={16} />
            Agent
          </h3>
          <select
            value={selectedAgent}
            onChange={(e) => setSelectedAgent(e.target.value)}
            className="select"
          >
            {agents.map(agent => (
              <option key={agent.name} value={agent.name}>
                {agent.name.charAt(0).toUpperCase() + agent.name.slice(1)}
              </option>
            ))}
          </select>
          {agents.find(a => a.name === selectedAgent)?.description && (
            <p className="agent-description">
              {agents.find(a => a.name === selectedAgent).description}
            </p>
          )}
        </div>

        <div className="sidebar-section">
          <h3>
            <Settings size={16} />
            LLM Provider
          </h3>
          <select
            value={selectedLLM}
            onChange={(e) => setSelectedLLM(e.target.value)}
            className="select"
          >
            {llmProviders.map(provider => (
              <option key={provider.name} value={provider.name}>
                {provider.name}
              </option>
            ))}
          </select>
        </div>

        <div className="sidebar-footer">
          <div className="status-indicator">
            <div className="status-dot"></div>
            <span>Online</span>
          </div>
        </div>
      </div>

      <div className="main-content">
        <div className="chat-container">
          <div className="messages">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <Bot size={64} />
                <h2>Welcome to Personal Jarvis</h2>
                <p>Your voice-enabled AI assistant with specialized agents</p>
                <div className="features">
                  <div className="feature">🎤 Multi-language speech recognition</div>
                  <div className="feature">💻 Linux command execution</div>
                  <div className="feature">🤖 Multi-LLM support (GPT-4/Claude)</div>
                  <div className="feature">🔧 Specialized AI agents</div>
                  <div className="feature">🧠 Vector memory</div>
                </div>
              </div>
            ) : (
              messages.map((message, index) => (
                <div key={index} className={`message ${message.role}`}>
                  <div className="message-icon">
                    {message.role === 'user' ? '👤' : '🤖'}
                  </div>
                  <div className="message-content">
                    <div className="message-header">
                      <span className="message-role">
                        {message.role === 'user' ? 'You' : 'Jarvis'}
                      </span>
                      {message.agent && (
                        <span className="message-agent">
                          via {message.agent} agent
                        </span>
                      )}
                    </div>
                    <div className="message-text">{message.content}</div>
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="message assistant">
                <div className="message-icon">🤖</div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="input-area" onSubmit={sendMessage}>
            <button
              type="button"
              className={`voice-button ${isRecording ? 'recording' : ''}`}
              onClick={startRecording}
              disabled={isRecording}
            >
              <Mic size={20} />
            </button>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message or use voice input..."
              className="message-input"
              disabled={isLoading}
            />
            <button
              type="submit"
              className="send-button"
              disabled={!input.trim() || isLoading}
            >
              <Send size={20} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;
