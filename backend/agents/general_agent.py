"""
General Agent - General purpose assistant
"""
from typing import List, Optional
import logging

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class GeneralAgent(BaseAgent):
    """General purpose AI assistant"""
    
    def __init__(self):
        super().__init__(
            name="general",
            description="General purpose AI assistant for various tasks"
        )
        self.system_prompt = """You are a helpful AI assistant named Jarvis.
You are knowledgeable, friendly, and efficient.
You can help with various tasks including:
- Answering questions
- Providing explanations
- General assistance
- Task planning
- Information synthesis

Provide clear, helpful, and accurate responses."""
    
    async def process(
        self,
        message: str,
        llm_provider: str = "gpt-4",
        context: Optional[List[str]] = None
    ) -> str:
        """Process general requests"""
        logger.info("Processing general request")
        
        # Build context-aware prompt
        prompt = self._build_prompt(message, context)
        
        # Call LLM
        response = await self._call_llm(
            prompt=prompt,
            system_prompt=self.system_prompt,
            llm_provider=llm_provider
        )
        
        return response
    
    def _build_prompt(self, message: str, context: Optional[List[str]] = None) -> str:
        """Build the prompt with context"""
        prompt_parts = []
        
        if context:
            prompt_parts.append("Previous conversation:")
            prompt_parts.extend(context[-5:])  # Last 5 context items
            prompt_parts.append("\n")
        
        prompt_parts.append(f"User: {message}")
        
        return "\n".join(prompt_parts)
