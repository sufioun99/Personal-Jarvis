"""
Code Agent - Specialized in code analysis, generation, and debugging
"""
from typing import List, Optional
import logging

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class CodeAgent(BaseAgent):
    """Agent specialized in code-related tasks"""
    
    def __init__(self):
        super().__init__(
            name="code",
            description="Code analysis, generation, debugging, and refactoring expert"
        )
        self.system_prompt = """You are a senior software engineer and code expert.
You specialize in:
- Code analysis and review
- Code generation and refactoring
- Debugging and troubleshooting
- Best practices and design patterns
- Multiple programming languages

Provide clear, well-documented code with explanations.
Consider edge cases, performance, and security."""
    
    async def process(
        self,
        message: str,
        llm_provider: str = "gpt-4",
        context: Optional[List[str]] = None
    ) -> str:
        """Process code-related requests"""
        logger.info("Processing code request")
        
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
            prompt_parts.extend(context[-3:])  # Last 3 context items
            prompt_parts.append("\n")
        
        prompt_parts.append(f"Request: {message}")
        
        return "\n".join(prompt_parts)
