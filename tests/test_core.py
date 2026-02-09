"""
Unit tests for JARVIS core components
"""
import pytest
import asyncio
from core.nlu import nlu_engine, IntentType
from core.command_executor import command_executor


class TestNLU:
    """Test Natural Language Understanding"""
    
    def test_intent_classification_system_command(self):
        """Test system command intent classification"""
        query = "list all files in current directory"
        intent = nlu_engine.classify_intent(query)
        assert intent == IntentType.SYSTEM_COMMAND
    
    def test_intent_classification_code_task(self):
        """Test code task intent classification"""
        query = "write a python function to sort a list"
        intent = nlu_engine.classify_intent(query)
        assert intent == IntentType.CODE_TASK
    
    def test_intent_classification_web_search(self):
        """Test web search intent classification"""
        query = "search for machine learning tutorials"
        intent = nlu_engine.classify_intent(query)
        assert intent == IntentType.WEB_SEARCH
    
    def test_intent_classification_weather(self):
        """Test weather intent classification"""
        query = "what's the weather in New York"
        intent = nlu_engine.classify_intent(query)
        assert intent == IntentType.WEATHER
    
    def test_entity_extraction_language(self):
        """Test programming language entity extraction"""
        query = "write a python function"
        intent, entities = nlu_engine.parse_query(query)
        assert entities.get("language") == "python"
    
    def test_entity_extraction_location(self):
        """Test location entity extraction"""
        query = "weather in San Francisco"
        intent, entities = nlu_engine.parse_query(query)
        assert "location" in entities


class TestCommandExecutor:
    """Test command execution safety"""
    
    def test_safe_command_validation(self):
        """Test safe command passes validation"""
        is_safe, reason = command_executor.is_safe_command("ls -la")
        assert is_safe is True
        assert reason is None
    
    def test_dangerous_command_detection(self):
        """Test dangerous command detection"""
        is_safe, reason = command_executor.is_safe_command("rm -rf /")
        assert is_safe is False
        assert reason is not None
    
    def test_blacklisted_command(self):
        """Test blacklisted command rejection"""
        is_safe, reason = command_executor.is_safe_command(":(){ :|:& };:")
        assert is_safe is False
        assert "blacklisted" in reason.lower()
    
    def test_sudo_disabled(self):
        """Test sudo command when disabled"""
        # Assuming sudo is disabled in settings
        if not command_executor.enable_sudo:
            is_safe, reason = command_executor.is_safe_command("sudo apt update")
            assert is_safe is False
            assert "sudo" in reason.lower()
    
    def test_command_translation_list_files(self):
        """Test natural language to command translation"""
        command = command_executor.parse_natural_language_command("list all files")
        assert command is not None
        assert "ls" in command
    
    def test_command_translation_show_disk(self):
        """Test disk usage command translation"""
        command = command_executor.parse_natural_language_command("show disk usage")
        assert command is not None
        assert "df" in command
    
    def test_command_execution_safe(self):
        """Test safe command execution"""
        success, stdout, stderr = command_executor.execute_command("echo 'test'")
        assert success is True
        assert "test" in stdout


@pytest.mark.asyncio
class TestAsyncComponents:
    """Test async components"""
    
    async def test_llm_router_initialization(self):
        """Test LLM router can be initialized"""
        from core.llm_integration import llm_router
        assert llm_router is not None
    
    async def test_api_manager_initialization(self):
        """Test API manager can be initialized"""
        from api.api_manager import api_manager
        assert api_manager is not None
    
    async def test_agent_orchestrator_initialization(self):
        """Test agent orchestrator initialization"""
        from agents.orchestrator import agent_orchestrator
        assert agent_orchestrator is not None
        assert len(agent_orchestrator.agents) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
