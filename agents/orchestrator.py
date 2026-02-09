"""
Agent Orchestrator - Coordinates all specialized agents
"""
from typing import Dict, Any, List, Optional
import asyncio
from agents.specialized_agents import (
    CodeAgent, ResearchAgent, DataAnalysisAgent,
    DevOpsAgent, SecurityAgent, DocumentationAgent
)
from core.nlu import IntentType
from utils.logger import logger


class AgentOrchestrator:
    """
    Orchestrates task delegation to specialized agents
    """
    
    def __init__(self):
        """Initialize all specialized agents"""
        self.agents = {
            "code": CodeAgent(),
            "research": ResearchAgent(),
            "data_analysis": DataAnalysisAgent(),
            "devops": DevOpsAgent(),
            "security": SecurityAgent(),
            "documentation": DocumentationAgent(),
        }
        logger.info("Agent Orchestrator initialized with all agents")
    
    def route_to_agent(self, intent: IntentType) -> Optional[str]:
        """
        Route intent to appropriate agent
        
        Args:
            intent: User intent
            
        Returns:
            Agent name or None
        """
        routing = {
            IntentType.CODE_TASK: "code",
            IntentType.WEB_SEARCH: "research",
            IntentType.GITHUB: "devops",
            IntentType.CLOUD_OPERATION: "devops",
        }
        return routing.get(intent)
    
    async def execute_task(
        self, agent_name: str, task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute task with specific agent
        
        Args:
            agent_name: Name of agent to use
            task: Task specification
            
        Returns:
            Task result
        """
        if agent_name not in self.agents:
            raise ValueError(f"Unknown agent: {agent_name}")
        
        agent = self.agents[agent_name]
        logger.info(f"Delegating task to {agent_name}")
        
        return await agent.handle_task(task)
    
    async def execute_parallel(
        self, tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Execute multiple independent tasks in parallel
        
        Args:
            tasks: List of task specifications (each with 'agent' and 'task' keys)
            
        Returns:
            List of results
        """
        logger.info(f"Executing {len(tasks)} tasks in parallel")
        
        coroutines = [
            self.execute_task(task["agent"], task["task"])
            for task in tasks
        ]
        
        results = await asyncio.gather(*coroutines, return_exceptions=True)
        
        # Handle exceptions
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "success": False,
                    "agent": tasks[i]["agent"],
                    "error": str(result)
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def execute_sequential(
        self, tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Execute tasks sequentially (for dependent tasks)
        
        Args:
            tasks: List of task specifications
            
        Returns:
            List of results
        """
        logger.info(f"Executing {len(tasks)} tasks sequentially")
        
        results = []
        for task_spec in tasks:
            result = await self.execute_task(task_spec["agent"], task_spec["task"])
            results.append(result)
            
            # Stop if a task fails
            if not result.get("success", False):
                logger.warning(f"Sequential execution stopped due to failure")
                break
        
        return results
    
    def get_agent_status(self, agent_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get status of agents
        
        Args:
            agent_name: Specific agent name or None for all
            
        Returns:
            Status information
        """
        if agent_name:
            if agent_name not in self.agents:
                return {"error": f"Unknown agent: {agent_name}"}
            return self.agents[agent_name].get_status()
        
        return {
            name: agent.get_status()
            for name, agent in self.agents.items()
        }


# Global orchestrator instance
agent_orchestrator = AgentOrchestrator()
