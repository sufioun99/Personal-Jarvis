"""
JARVIS - Main orchestrator and brain
"""
from typing import Optional, Dict, Any, List
import asyncio
from core.llm_integration import llm_router
from core.voice_interface import voice_interface
from core.nlu import nlu_engine, IntentType
from core.command_executor import command_executor
from agents.orchestrator import agent_orchestrator
from api.api_manager import api_manager
from utils.logger import logger


class Jarvis:
    """
    Main JARVIS AI Assistant orchestrator
    Coordinates all components and provides the main interface
    """
    
    def __init__(self):
        """Initialize JARVIS"""
        self.llm_router = llm_router
        self.voice = voice_interface
        self.nlu = nlu_engine
        self.executor = command_executor
        self.orchestrator = agent_orchestrator
        self.api_manager = api_manager
        self.conversation_history: List[Dict[str, str]] = []
        logger.info("JARVIS initialized successfully")
    
    async def process_query(
        self, query: str, voice_output: bool = False
    ) -> Dict[str, Any]:
        """
        Process user query and generate response
        
        Args:
            query: User query text
            voice_output: Whether to output response via voice
            
        Returns:
            Response dictionary with result and metadata
        """
        logger.info(f"Processing query: {query}")
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": query})
        
        try:
            # Classify intent and extract entities
            intent, entities = self.nlu.parse_query(query)
            
            # Route to appropriate handler
            response = await self._route_intent(query, intent, entities)
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": response.get("response", "")
            })
            
            # Voice output if requested
            if voice_output and response.get("response"):
                await self.voice.text_to_speech(response["response"])
            
            return {
                "success": True,
                "query": query,
                "intent": intent.value,
                "entities": entities,
                "response": response.get("response", ""),
                "data": response.get("data", {})
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            error_response = f"I encountered an error: {str(e)}"
            
            if voice_output:
                await self.voice.text_to_speech(error_response)
            
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "response": error_response
            }
    
    async def _route_intent(
        self, query: str, intent: IntentType, entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Route query based on intent"""
        
        if intent == IntentType.SYSTEM_COMMAND:
            return await self._handle_system_command(query, entities)
        
        elif intent == IntentType.CODE_TASK:
            return await self._handle_code_task(query, entities)
        
        elif intent == IntentType.WEB_SEARCH:
            return await self._handle_web_search(query, entities)
        
        elif intent == IntentType.WEATHER:
            return await self._handle_weather(entities)
        
        elif intent == IntentType.NEWS:
            return await self._handle_news(entities)
        
        elif intent == IntentType.FILE_OPERATION:
            return await self._handle_file_operation(query, entities)
        
        else:
            return await self._handle_general_query(query)
    
    async def _handle_system_command(
        self, query: str, entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle Linux system commands"""
        logger.info("Handling system command")
        
        # Execute command using LLM translation
        success, stdout, stderr = await self.executor.execute_with_llm_translation(
            query, self.llm_router
        )
        
        if success:
            response = f"Command executed successfully.\n\nOutput:\n{stdout}"
        else:
            response = f"Command execution failed.\n\nError: {stderr}"
        
        return {
            "response": response,
            "data": {
                "success": success,
                "stdout": stdout,
                "stderr": stderr
            }
        }
    
    async def _handle_code_task(
        self, query: str, entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle code-related tasks"""
        logger.info("Handling code task")
        
        # Delegate to Code Agent
        task = {
            "description": query,
            "type": "generate",  # Could be inferred from query
            "language": entities.get("language", "python")
        }
        
        result = await self.orchestrator.execute_task("code", task)
        
        if result.get("success"):
            code_result = result.get("result", {})
            code = code_result.get("code", "")
            response = f"Here's the code I generated:\n\n```{task['language']}\n{code}\n```"
        else:
            response = f"Failed to generate code: {result.get('error', 'Unknown error')}"
        
        return {
            "response": response,
            "data": result
        }
    
    async def _handle_web_search(
        self, query: str, entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle web search queries"""
        logger.info("Handling web search")
        
        # Extract search query
        search_query = query.replace("search for", "").replace("google", "").strip()
        
        # Perform search
        search_results = await self.api_manager.search_web(search_query)
        
        if "error" in search_results:
            return {
                "response": f"Search failed: {search_results['error']}",
                "data": {}
            }
        
        # Format results
        results = search_results.get("results", [])
        if results:
            response = f"I found these results for '{search_query}':\n\n"
            for i, result in enumerate(results[:3], 1):
                response += f"{i}. {result['title']}\n   {result['snippet']}\n   {result['link']}\n\n"
        else:
            response = "No results found."
        
        return {
            "response": response,
            "data": search_results
        }
    
    async def _handle_weather(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Handle weather queries"""
        logger.info("Handling weather query")
        
        location = entities.get("location", "current location")
        weather_data = await self.api_manager.get_weather(location)
        
        if "error" in weather_data:
            return {
                "response": f"Couldn't get weather: {weather_data['error']}",
                "data": {}
            }
        
        response = f"""Weather in {weather_data['location']}:
- Temperature: {weather_data['temperature']}°C
- Conditions: {weather_data['description']}
- Humidity: {weather_data['humidity']}%
- Wind Speed: {weather_data['wind_speed']} m/s"""
        
        return {
            "response": response,
            "data": weather_data
        }
    
    async def _handle_news(self, entities: Dict[str, Any]) -> Dict[str, Any]:
        """Handle news queries"""
        logger.info("Handling news query")
        
        topic = entities.get("topic")
        news_data = await self.api_manager.get_news(topic)
        
        if "error" in news_data:
            return {
                "response": f"Couldn't get news: {news_data['error']}",
                "data": {}
            }
        
        articles = news_data.get("articles", [])
        if articles:
            response = f"Latest news{' about ' + topic if topic else ''}:\n\n"
            for i, article in enumerate(articles[:3], 1):
                response += f"{i}. {article['title']}\n   {article['description']}\n   Source: {article['source']}\n\n"
        else:
            response = "No news articles found."
        
        return {
            "response": response,
            "data": news_data
        }
    
    async def _handle_file_operation(
        self, query: str, entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle file operations"""
        logger.info("Handling file operation")
        
        # Use command executor for file operations
        return await self._handle_system_command(query, entities)
    
    async def _handle_general_query(self, query: str) -> Dict[str, Any]:
        """Handle general conversational queries"""
        logger.info("Handling general query")
        
        # Build context from conversation history
        context = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in self.conversation_history[-5:]  # Last 5 messages
        ])
        
        # Generate response using LLM
        response = await self.llm_router.generate_response(
            query,
            system_prompt=f"""You are JARVIS, an advanced AI assistant with deep knowledge of Linux systems and programming.
Be helpful, precise, and friendly.

Recent conversation:
{context}""",
            task_type="general",
            temperature=0.7
        )
        
        return {
            "response": response,
            "data": {}
        }
    
    async def voice_mode(self):
        """
        Run JARVIS in voice interaction mode
        """
        logger.info("Starting voice mode")
        print("JARVIS voice mode activated. Say 'Hey JARVIS' to start.")
        
        try:
            while True:
                # Listen for wake word and command
                command = await self.voice.listen_and_transcribe()
                
                if command:
                    # Process command
                    result = await self.process_query(command, voice_output=True)
                    print(f"\nYou: {command}")
                    print(f"JARVIS: {result.get('response', '')}\n")
                
                # Small delay before next iteration
                await asyncio.sleep(0.5)
                
        except KeyboardInterrupt:
            logger.info("Voice mode stopped by user")
            print("\nVoice mode deactivated.")
    
    async def text_mode(self):
        """
        Run JARVIS in text interaction mode
        """
        logger.info("Starting text mode")
        print("JARVIS text mode activated. Type 'exit' to quit.\n")
        
        while True:
            try:
                query = input("You: ").strip()
                
                if not query:
                    continue
                
                if query.lower() in ["exit", "quit", "bye"]:
                    print("JARVIS: Goodbye!")
                    break
                
                result = await self.process_query(query, voice_output=False)
                print(f"JARVIS: {result.get('response', '')}\n")
                
            except KeyboardInterrupt:
                print("\nJARVIS: Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error in text mode: {e}")
                print(f"JARVIS: Sorry, I encountered an error: {e}\n")


# Global JARVIS instance
jarvis = Jarvis()
