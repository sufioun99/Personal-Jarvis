"""
Integration tests for JARVIS
"""
import pytest
import asyncio
from core.jarvis import jarvis


@pytest.mark.asyncio
class TestJarvisIntegration:
    """Integration tests for JARVIS"""
    
    async def test_jarvis_initialization(self):
        """Test JARVIS initializes correctly"""
        assert jarvis is not None
        assert jarvis.llm_router is not None
        assert jarvis.nlu is not None
        assert jarvis.executor is not None
    
    async def test_process_simple_query(self):
        """Test processing a simple query"""
        # This will only work if API keys are configured
        result = await jarvis.process_query("hello", voice_output=False)
        assert result is not None
        assert "success" in result
        assert "response" in result
    
    async def test_conversation_history(self):
        """Test conversation history tracking"""
        initial_len = len(jarvis.conversation_history)
        await jarvis.process_query("test query", voice_output=False)
        assert len(jarvis.conversation_history) > initial_len


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
