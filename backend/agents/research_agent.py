"""
Research Agent - Specialized in information gathering and analysis
"""
from typing import List, Optional
import logging

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class ResearchAgent(BaseAgent):
    """Agent specialized in research and analysis"""
    
    def __init__(self):
        super().__init__(
            name="research",
            description="Research, analysis, and information synthesis expert"
        )
        self.system_prompt = """You are a research analyst and information specialist.
You specialize in:
- Information gathering and synthesis
- Data analysis and interpretation
- Comparative analysis
- Technical explanations
- Research methodology

Provide well-structured, comprehensive responses with sources when available.
Break down complex topics into understandable explanations."""
    
    async def process(
        self,
        message: str,
        llm_provider: str = "gpt-4",
        context: Optional[List[str]] = None
    ) -> str:
        """Process research-related requests"""
        logger.info("Processing research request")
        
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
            prompt_parts.append("Previous context:")
            prompt_parts.extend(context[-3:])
            prompt_parts.append("\n")
        
        prompt_parts.append(f"Request: {message}")
        
        return "\n".join(prompt_parts)
