"""
Base Agent class for all specialized agents
"""
from abc import ABC, abstractmethod
from typing import List, Optional
import logging

from ..llm.provider import LLMProvider

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.llm_provider = LLMProvider()
    
    @abstractmethod
    async def process(
        self,
        message: str,
        llm_provider: str = "gpt-4",
        context: Optional[List[str]] = None
    ) -> str:
        """Process a message and return a response"""
        pass
    
    async def _call_llm(
        self,
        prompt: str,
        system_prompt: str,
        llm_provider: str = "gpt-4"
    ) -> str:
        """Call the LLM with the given prompts"""
        return await self.llm_provider.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            provider=llm_provider
        )
