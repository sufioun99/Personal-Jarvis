"""
DevOps Agent - Specialized in system operations and infrastructure
"""
from typing import List, Optional
import logging

from .base_agent import BaseAgent

logger = logging.getLogger(__name__)


class DevOpsAgent(BaseAgent):
    """Agent specialized in DevOps and system operations"""
    
    def __init__(self):
        super().__init__(
            name="devops",
            description="DevOps, infrastructure, and system operations expert"
        )
        self.system_prompt = """You are a senior DevOps engineer and system administrator.
You specialize in:
- System administration and operations
- CI/CD pipelines and automation
- Container orchestration (Docker, Kubernetes)
- Cloud infrastructure (AWS, Azure, GCP)
- Monitoring and troubleshooting
- Security and best practices

Provide practical, production-ready solutions with safety in mind.
Always consider scalability, reliability, and security."""
    
    async def process(
        self,
        message: str,
        llm_provider: str = "gpt-4",
        context: Optional[List[str]] = None
    ) -> str:
        """Process DevOps-related requests"""
        logger.info("Processing DevOps request")
        
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
