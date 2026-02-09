"""
Main FastAPI application for Personal Jarvis
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import logging

from .agents.orchestrator import AgentOrchestrator
from .speech.recognizer import SpeechRecognizer
from .llm.provider import LLMProvider
from .memory.vector_store import VectorMemory
from .system.command_executor import SafeCommandExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Personal Jarvis",
    description="Voice AI Assistant with multi-language support and specialized agents",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
orchestrator = AgentOrchestrator()
speech_recognizer = SpeechRecognizer()
llm_provider = LLMProvider()
vector_memory = VectorMemory()
command_executor = SafeCommandExecutor()


# Request/Response Models
class ChatRequest(BaseModel):
    message: str
    agent_type: Optional[str] = "general"
    llm_provider: Optional[str] = "gpt-4"
    language: Optional[str] = "en"


class ChatResponse(BaseModel):
    response: str
    agent_used: str
    metadata: Optional[dict] = None


class CommandRequest(BaseModel):
    command: str
    safe_mode: bool = True


class CommandResponse(BaseModel):
    success: bool
    output: str
    error: Optional[str] = None


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Personal Jarvis",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "components": {
            "orchestrator": "active",
            "speech_recognizer": "active",
            "llm_provider": "active",
            "vector_memory": "active",
            "command_executor": "active"
        }
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process chat messages through the agent orchestrator
    """
    try:
        logger.info(f"Processing chat request with agent: {request.agent_type}")
        
        # Store in memory
        await vector_memory.store_interaction(request.message, "user")
        
        # Process through orchestrator
        response = await orchestrator.process_request(
            message=request.message,
            agent_type=request.agent_type,
            llm_provider=request.llm_provider,
            context=await vector_memory.get_relevant_context(request.message)
        )
        
        # Store response
        await vector_memory.store_interaction(response["response"], "assistant")
        
        return ChatResponse(
            response=response["response"],
            agent_used=response["agent"],
            metadata=response.get("metadata")
        )
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/speech/transcribe")
async def transcribe_speech(audio: UploadFile = File(...), language: str = "en"):
    """
    Transcribe audio file to text using multi-language speech recognition
    """
    try:
        logger.info(f"Transcribing audio in language: {language}")
        
        # Read audio file
        audio_data = await audio.read()
        
        # Transcribe
        text = await speech_recognizer.transcribe(audio_data, language)
        
        return {"text": text, "language": language}
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/command/execute", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    """
    Execute Linux commands with safety checks
    """
    try:
        logger.info(f"Executing command: {request.command[:50]}...")
        
        result = await command_executor.execute(
            command=request.command,
            safe_mode=request.safe_mode
        )
        
        return CommandResponse(
            success=result["success"],
            output=result["output"],
            error=result.get("error")
        )
    except Exception as e:
        logger.error(f"Command execution error: {str(e)}")
        return CommandResponse(
            success=False,
            output="",
            error=str(e)
        )


@app.get("/agents/list")
async def list_agents():
    """
    List all available specialized agents
    """
    return {
        "agents": orchestrator.get_available_agents()
    }


@app.get("/llm/providers")
async def list_llm_providers():
    """
    List available LLM providers
    """
    return {
        "providers": llm_provider.get_available_providers()
    }


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """
    WebSocket endpoint for real-time chat
    """
    await websocket.accept()
    logger.info("WebSocket connection established")
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Process message
            response = await orchestrator.process_request(
                message=data.get("message", ""),
                agent_type=data.get("agent_type", "general"),
                llm_provider=data.get("llm_provider", "gpt-4")
            )
            
            await websocket.send_json(response)
    except WebSocketDisconnect:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
