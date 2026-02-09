"""
FastAPI Web Server for JARVIS
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio
from core.jarvis import jarvis
from agents.orchestrator import agent_orchestrator
from utils.logger import logger
from config import settings


# Create FastAPI app
app = FastAPI(
    title="JARVIS AI Assistant",
    description="Personal AI Assistant with Voice Control and Multi-Agent System",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class QueryRequest(BaseModel):
    """Request model for queries"""
    query: str
    voice_output: bool = False


class QueryResponse(BaseModel):
    """Response model for queries"""
    success: bool
    query: str
    intent: Optional[str] = None
    response: str
    data: Dict[str, Any] = {}


class AgentTaskRequest(BaseModel):
    """Request model for agent tasks"""
    agent: str
    task: Dict[str, Any]


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "JARVIS AI Assistant",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "components": {
            "llm": "operational",
            "voice": "operational",
            "agents": "operational"
        }
    }


@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Process a text query
    """
    try:
        result = await jarvis.process_query(
            request.query,
            voice_output=request.voice_output
        )
        return result
    except Exception as e:
        logger.error(f"Query processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agent/execute")
async def execute_agent_task(request: AgentTaskRequest):
    """
    Execute a task with a specific agent
    """
    try:
        result = await agent_orchestrator.execute_task(
            request.agent,
            request.task
        )
        return result
    except Exception as e:
        logger.error(f"Agent execution error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agent/status")
async def get_agent_status(agent: Optional[str] = None):
    """
    Get status of agents
    """
    try:
        status = agent_orchestrator.get_agent_status(agent)
        return status
    except Exception as e:
        logger.error(f"Status retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversation/history")
async def get_conversation_history():
    """
    Get conversation history
    """
    return {
        "history": jarvis.conversation_history
    }


@app.delete("/conversation/clear")
async def clear_conversation():
    """
    Clear conversation history
    """
    jarvis.conversation_history.clear()
    return {"message": "Conversation history cleared"}


# WebSocket for real-time communication
class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info("WebSocket client connected")
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info("WebSocket client disconnected")
    
    async def send_message(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time communication
    """
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            query = data.get("query", "")
            if not query:
                await manager.send_message(
                    {"error": "No query provided"},
                    websocket
                )
                continue
            
            # Process query
            result = await jarvis.process_query(query, voice_output=False)
            
            # Send response
            await manager.send_message(result, websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await manager.send_message(
            {"error": str(e)},
            websocket
        )
        manager.disconnect(websocket)


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("JARVIS API server starting up")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("JARVIS API server shutting down")
    await jarvis.api_manager.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.jarvis_host,
        port=settings.jarvis_port,
        log_level=settings.log_level.lower()
    )
