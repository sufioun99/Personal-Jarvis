"""
Base Agent class for all specialized AI agents
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum
from utils.logger import logger


class AgentStatus(Enum):
    """Agent execution status"""
    IDLE = "idle"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"


class BaseAgent(ABC):
    """
    Base class for all specialized AI agents
    """
    
    def __init__(self, name: str, description: str):
        """
        Initialize base agent
        
        Args:
            name: Agent name
            description: Agent description
        """
        self.name = name
        self.description = description
        self.status = AgentStatus.IDLE
        self.current_task = None
        logger.info(f"Agent initialized: {name}")
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task
        
        Args:
            task: Task specification
            
        Returns:
            Task result
        """
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current agent status
        
        Returns:
            Status information
        """
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status.value,
            "current_task": self.current_task
        }
    
    async def handle_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle task execution with status management
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
        """
        try:
            self.status = AgentStatus.WORKING
            self.current_task = task.get("description", "Unknown task")
            logger.info(f"{self.name} starting task: {self.current_task}")
            
            result = await self.execute(task)
            
            self.status = AgentStatus.COMPLETED
            self.current_task = None
            logger.info(f"{self.name} completed task successfully")
            
            return {
                "success": True,
                "agent": self.name,
                "result": result
            }
            
        except Exception as e:
            self.status = AgentStatus.FAILED
            logger.error(f"{self.name} task failed: {e}")
            
            return {
                "success": False,
                "agent": self.name,
                "error": str(e)
            }
        finally:
            self.status = AgentStatus.IDLE
