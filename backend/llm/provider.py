"""
Multi-LLM Provider - Support for GPT-4, Claude, and other models
"""
from typing import Optional, Dict
import logging
import os

logger = logging.getLogger(__name__)


class LLMProvider:
    """
    Unified interface for multiple LLM providers
    """
    
    def __init__(self):
        self.providers = {
            "gpt-4": self._call_openai,
            "gpt-3.5-turbo": self._call_openai,
            "claude-3-opus": self._call_anthropic,
            "claude-3-sonnet": self._call_anthropic,
            "claude-2": self._call_anthropic,
        }
        self._init_clients()
    
    def _init_clients(self):
        """Initialize API clients"""
        try:
            # OpenAI client
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                from openai import AsyncOpenAI
                self.openai_client = AsyncOpenAI(api_key=api_key)
                logger.info("OpenAI client initialized")
            else:
                self.openai_client = None
                logger.warning("OpenAI API key not found")
            
            # Anthropic client
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if api_key:
                from anthropic import AsyncAnthropic
                self.anthropic_client = AsyncAnthropic(api_key=api_key)
                logger.info("Anthropic client initialized")
            else:
                self.anthropic_client = None
                logger.warning("Anthropic API key not found")
                
        except Exception as e:
            logger.error(f"Error initializing LLM clients: {str(e)}")
    
    def get_available_providers(self) -> list:
        """Get list of available LLM providers"""
        available = []
        
        if self.openai_client:
            available.extend([
                {"name": "gpt-4", "provider": "OpenAI", "description": "Most capable GPT-4 model"},
                {"name": "gpt-3.5-turbo", "provider": "OpenAI", "description": "Fast and efficient"}
            ])
        
        if self.anthropic_client:
            available.extend([
                {"name": "claude-3-opus", "provider": "Anthropic", "description": "Most capable Claude model"},
                {"name": "claude-3-sonnet", "provider": "Anthropic", "description": "Balanced performance"},
                {"name": "claude-2", "provider": "Anthropic", "description": "Previous generation"}
            ])
        
        return available
    
    async def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        provider: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Generate response from specified LLM provider
        """
        try:
            # Get the appropriate provider function
            provider_func = self.providers.get(provider)
            
            if not provider_func:
                raise ValueError(f"Unknown provider: {provider}")
            
            # Call the provider
            response = await provider_func(
                prompt=prompt,
                system_prompt=system_prompt,
                model=provider,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"Error: {str(e)}"
    
    async def _call_openai(
        self,
        prompt: str,
        system_prompt: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Call OpenAI API"""
        if not self.openai_client:
            return "OpenAI API key not configured"
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            return f"OpenAI error: {str(e)}"
    
    async def _call_anthropic(
        self,
        prompt: str,
        system_prompt: str,
        model: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Call Anthropic API"""
        if not self.anthropic_client:
            return "Anthropic API key not configured"
        
        try:
            response = await self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt if system_prompt else "You are a helpful AI assistant.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            return f"Anthropic error: {str(e)}"
