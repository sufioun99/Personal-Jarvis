"""
LLM Integration Layer - Multi-model support with routing and fallback
"""
from typing import Optional, Dict, Any, List
from enum import Enum
from openai import AsyncOpenAI
from anthropic import Anthropic
import google.generativeai as genai
from config import settings
from utils.logger import logger


class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"


class LLMRouter:
    """
    Routes queries to appropriate LLM based on task type
    Provides fallback mechanism and cost optimization
    """
    
    def __init__(self):
        """Initialize LLM clients"""
        self.openai_client = None
        self.anthropic_client = None
        self.google_client = None
        
        # Initialize OpenAI with new API
        if settings.openai_api_key:
            self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
            logger.info("OpenAI client initialized")
        
        # Initialize Anthropic
        if settings.anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=settings.anthropic_api_key)
            logger.info("Anthropic client initialized")
        
        # Initialize Google
        if settings.google_api_key:
            genai.configure(api_key=settings.google_api_key)
            self.google_client = genai
            logger.info("Google AI client initialized")
    
    def route_query(self, query: str, task_type: str = "general") -> LLMProvider:
        """
        Determine which LLM to use based on task type
        
        Args:
            query: User query
            task_type: Type of task (general, coding, analysis, etc.)
            
        Returns:
            Appropriate LLM provider
        """
        # Task-specific routing
        task_routing = {
            "coding": LLMProvider.OPENAI,
            "analysis": LLMProvider.ANTHROPIC,
            "general": LLMProvider.OPENAI,
            "creative": LLMProvider.GOOGLE,
        }
        
        provider = task_routing.get(task_type, LLMProvider.OPENAI)
        
        # Check if provider is available
        if provider == LLMProvider.OPENAI and not self.openai_client:
            provider = LLMProvider.ANTHROPIC if self.anthropic_client else LLMProvider.GOOGLE
        elif provider == LLMProvider.ANTHROPIC and not self.anthropic_client:
            provider = LLMProvider.OPENAI if self.openai_client else LLMProvider.GOOGLE
        elif provider == LLMProvider.GOOGLE and not self.google_client:
            provider = LLMProvider.OPENAI if self.openai_client else LLMProvider.ANTHROPIC
        
        return provider
    
    async def generate_response(
        self,
        query: str,
        system_prompt: Optional[str] = None,
        task_type: str = "general",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        provider: Optional[LLMProvider] = None
    ) -> str:
        """
        Generate response from appropriate LLM
        
        Args:
            query: User query
            system_prompt: System context/instructions
            task_type: Type of task
            temperature: Sampling temperature
            max_tokens: Maximum response length
            provider: Override automatic routing
            
        Returns:
            Generated response text
        """
        if provider is None:
            provider = self.route_query(query, task_type)
        
        try:
            if provider == LLMProvider.OPENAI:
                return await self._openai_generate(query, system_prompt, temperature, max_tokens)
            elif provider == LLMProvider.ANTHROPIC:
                return await self._anthropic_generate(query, system_prompt, temperature, max_tokens)
            elif provider == LLMProvider.GOOGLE:
                return await self._google_generate(query, system_prompt, temperature, max_tokens)
        except Exception as e:
            logger.error(f"Error with {provider.value}: {e}")
            # Try fallback
            return await self._fallback_generate(query, system_prompt, temperature, max_tokens, provider)
    
    async def _openai_generate(
        self, query: str, system_prompt: Optional[str], temperature: float, max_tokens: int
    ) -> str:
        """Generate response using OpenAI"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": query})
        
        response = await self.openai_client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    async def _anthropic_generate(
        self, query: str, system_prompt: Optional[str], temperature: float, max_tokens: int
    ) -> str:
        """Generate response using Anthropic Claude"""
        response = self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt or "",
            messages=[{"role": "user", "content": query}]
        )
        return response.content[0].text
    
    async def _google_generate(
        self, query: str, system_prompt: Optional[str], temperature: float, max_tokens: int
    ) -> str:
        """Generate response using Google Gemini"""
        model = self.google_client.GenerativeModel('gemini-pro')
        prompt = f"{system_prompt}\n\n{query}" if system_prompt else query
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': temperature,
                'max_output_tokens': max_tokens,
            }
        )
        return response.text
    
    async def _fallback_generate(
        self, query: str, system_prompt: Optional[str], temperature: float, 
        max_tokens: int, failed_provider: LLMProvider
    ) -> str:
        """Try alternative providers as fallback"""
        providers = [LLMProvider.OPENAI, LLMProvider.ANTHROPIC, LLMProvider.GOOGLE]
        providers.remove(failed_provider)
        
        for provider in providers:
            try:
                logger.info(f"Trying fallback provider: {provider.value}")
                return await self.generate_response(
                    query, system_prompt, "general", temperature, max_tokens, provider
                )
            except Exception as e:
                logger.error(f"Fallback provider {provider.value} also failed: {e}")
                continue
        
        raise Exception("All LLM providers failed")


# Global LLM router instance
llm_router = LLMRouter()
