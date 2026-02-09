"""
Natural Language Understanding - Intent recognition and entity extraction
"""
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
import re
from utils.logger import logger


class IntentType(Enum):
    """Types of user intents"""
    SYSTEM_COMMAND = "system_command"
    CODE_TASK = "code_task"
    WEB_SEARCH = "web_search"
    FILE_OPERATION = "file_operation"
    INFORMATION = "information"
    WEATHER = "weather"
    NEWS = "news"
    CALENDAR = "calendar"
    EMAIL = "email"
    CLOUD_OPERATION = "cloud_operation"
    GITHUB = "github"
    GENERAL_QUERY = "general_query"
    UNKNOWN = "unknown"


class NLUEngine:
    """
    Natural Language Understanding Engine
    Handles intent classification and entity extraction
    """
    
    def __init__(self):
        """Initialize NLU engine"""
        self.intent_patterns = self._build_intent_patterns()
        logger.info("NLU Engine initialized")
    
    def _build_intent_patterns(self) -> Dict[IntentType, List[str]]:
        """
        Build regex patterns for intent classification
        
        Returns:
            Dictionary mapping intents to regex patterns
        """
        return {
            IntentType.SYSTEM_COMMAND: [
                r"(run|execute|perform)\s+(command|shell)",
                r"(list|show|display)\s+(files|directories|processes)",
                r"(check|monitor)\s+(system|memory|cpu|disk)",
                r"(install|update|remove)\s+package",
                r"(start|stop|restart)\s+service",
                r"(create|delete|move|copy)\s+(file|directory)",
            ],
            IntentType.CODE_TASK: [
                r"(write|create|generate)\s+(code|function|class|script)",
                r"(debug|fix|refactor)\s+code",
                r"(explain|analyze)\s+(this\s+)?code",
                r"(review|optimize)\s+code",
                r"help\s+me\s+(with\s+)?(coding|programming)",
            ],
            IntentType.WEB_SEARCH: [
                r"(search|find|look\s+up)\s+(for\s+)?(.+)\s+(on\s+)?the\s+web",
                r"(google|bing)\s+(.+)",
                r"what\s+is\s+(.+)",
                r"who\s+is\s+(.+)",
            ],
            IntentType.FILE_OPERATION: [
                r"(open|read|view)\s+(file|document)",
                r"(save|write)\s+to\s+file",
                r"(find|locate|search\s+for)\s+file",
            ],
            IntentType.WEATHER: [
                r"(what's|what\s+is)\s+the\s+weather",
                r"weather\s+(in|at|for)",
                r"temperature\s+(in|at|for)",
            ],
            IntentType.NEWS: [
                r"(latest|recent|current)\s+news",
                r"news\s+(about|on)",
                r"what's\s+happening\s+in",
            ],
            IntentType.GITHUB: [
                r"(create|make)\s+(a\s+)?github\s+repo",
                r"(push|commit)\s+to\s+github",
                r"(clone|pull)\s+from\s+github",
            ],
            IntentType.CLOUD_OPERATION: [
                r"(deploy|upload)\s+to\s+(aws|azure|gcp|cloud)",
                r"(list|show)\s+(aws|azure|gcp)\s+resources",
                r"(create|delete)\s+(ec2|lambda|s3|bucket)",
            ],
        }
    
    def classify_intent(self, text: str) -> IntentType:
        """
        Classify user intent from text
        
        Args:
            text: User input text
            
        Returns:
            Classified intent type
        """
        text_lower = text.lower()
        
        # Check each intent pattern
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    logger.info(f"Intent classified as: {intent.value}")
                    return intent
        
        # Default to general query
        logger.info("Intent classified as: general_query")
        return IntentType.GENERAL_QUERY
    
    def extract_entities(self, text: str, intent: IntentType) -> Dict[str, Any]:
        """
        Extract relevant entities based on intent
        
        Args:
            text: User input text
            intent: Classified intent
            
        Returns:
            Dictionary of extracted entities
        """
        entities = {}
        
        if intent == IntentType.SYSTEM_COMMAND:
            entities.update(self._extract_system_entities(text))
        elif intent == IntentType.CODE_TASK:
            entities.update(self._extract_code_entities(text))
        elif intent == IntentType.FILE_OPERATION:
            entities.update(self._extract_file_entities(text))
        elif intent == IntentType.WEATHER:
            entities.update(self._extract_location_entities(text))
        
        return entities
    
    def _extract_system_entities(self, text: str) -> Dict[str, Any]:
        """Extract system-related entities"""
        entities = {}
        
        # Extract package names
        package_match = re.search(r"package\s+([a-z0-9\-]+)", text.lower())
        if package_match:
            entities["package_name"] = package_match.group(1)
        
        # Extract service names
        service_match = re.search(r"service\s+([a-z0-9\-]+)", text.lower())
        if service_match:
            entities["service_name"] = service_match.group(1)
        
        return entities
    
    def _extract_code_entities(self, text: str) -> Dict[str, Any]:
        """Extract code-related entities"""
        entities = {}
        
        # Extract programming language
        languages = ["python", "javascript", "java", "c++", "go", "rust", "ruby", "php"]
        text_lower = text.lower()
        for lang in languages:
            if lang in text_lower:
                entities["language"] = lang
                break
        
        # Extract function/class names
        func_match = re.search(r"function\s+([a-zA-Z_][a-zA-Z0-9_]*)", text)
        if func_match:
            entities["function_name"] = func_match.group(1)
        
        class_match = re.search(r"class\s+([a-zA-Z_][a-zA-Z0-9_]*)", text)
        if class_match:
            entities["class_name"] = class_match.group(1)
        
        return entities
    
    def _extract_file_entities(self, text: str) -> Dict[str, Any]:
        """Extract file-related entities"""
        entities = {}
        
        # Extract file paths
        path_match = re.search(r"(/[\w/\-\.]+|\w+[\w\-\.]*\.\w+)", text)
        if path_match:
            entities["file_path"] = path_match.group(1)
        
        return entities
    
    def _extract_location_entities(self, text: str) -> Dict[str, Any]:
        """Extract location entities"""
        entities = {}
        
        # Extract city/location
        location_match = re.search(r"(in|at|for)\s+([A-Z][a-zA-Z\s]+)", text)
        if location_match:
            entities["location"] = location_match.group(2).strip()
        
        return entities
    
    def parse_query(self, text: str) -> Tuple[IntentType, Dict[str, Any]]:
        """
        Parse user query to extract intent and entities
        
        Args:
            text: User input text
            
        Returns:
            Tuple of (intent, entities)
        """
        intent = self.classify_intent(text)
        entities = self.extract_entities(text, intent)
        
        logger.info(f"Parsed query - Intent: {intent.value}, Entities: {entities}")
        return intent, entities


# Global NLU engine instance
nlu_engine = NLUEngine()
