"""
Agent Orchestrator - Routes requests to specialized AI agents
"""
from typing import Dict, Optional, List
import logging

from .code_agent import CodeAgent
from .devops_agent import DevOpsAgent
from .research_agent import ResearchAgent
from .general_agent import GeneralAgent

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """
    Orchestrates multiple specialized AI agents
    """
    
    def __init__(self):
        self.agents = {
            "code": CodeAgent(),
            "devops": DevOpsAgent(),
            "research": ResearchAgent(),
            "general": GeneralAgent()
        }
        logger.info("Agent orchestrator initialized with agents: %s", list(self.agents.keys()))
    
    def get_available_agents(self) -> List[Dict[str, str]]:
        """Get list of available agents with descriptions"""
        return [
            {
                "name": "code",
                "description": "Code analysis, generation, debugging, and refactoring",
                "capabilities": ["analyze", "generate", "debug", "refactor", "review"]
            },
            {
                "name": "devops",
                "description": "System operations, deployments, monitoring, and infrastructure",
                "capabilities": ["deploy", "monitor", "troubleshoot", "optimize", "configure"]
            },
            {
                "name": "research",
                "description": "Information gathering, analysis, and summarization",
                "capabilities": ["search", "analyze", "summarize", "compare", "explain"]
            },
            {
                "name": "general",
                "description": "General purpose assistant for various tasks",
                "capabilities": ["chat", "help", "explain", "assist"]
            }
        ]
    
    async def process_request(
        self,
        message: str,
        agent_type: str = "general",
        llm_provider: str = "gpt-4",
        context: Optional[List[str]] = None
    ) -> Dict:
        """
        Process a request through the appropriate agent
        
        Args:
            message: User message
            agent_type: Type of agent to use
            llm_provider: LLM provider to use
            context: Historical context
        
        Returns:
            Response dictionary with agent output
        """
        try:
            # Get the appropriate agent
            agent = self.agents.get(agent_type, self.agents["general"])
            
            logger.info(f"Processing request with {agent_type} agent")
            
            # Process the request
            response = await agent.process(
                message=message,
                llm_provider=llm_provider,
                context=context or []
            )
            
            return {
                "response": response,
                "agent": agent_type,
                "metadata": {
                    "llm_provider": llm_provider,
                    "context_used": len(context) if context else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return {
                "response": f"Error processing request: {str(e)}",
                "agent": agent_type,
                "metadata": {"error": True}
            }
    
    async def select_best_agent(self, message: str) -> str:
        """
        Automatically select the best agent for a given message
        """
        message_lower = message.lower()
        
        # Simple keyword-based routing
        if any(kw in message_lower for kw in ["code", "function", "bug", "debug", "program"]):
            return "code"
        elif any(kw in message_lower for kw in ["deploy", "server", "system", "docker", "kubernetes"]):
            return "devops"
        elif any(kw in message_lower for kw in ["research", "find", "search", "analyze", "explain"]):
            return "research"
        else:
            return "general"
