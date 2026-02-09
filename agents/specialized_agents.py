"""
Specialized AI Agents for different task types
"""
from typing import Dict, Any
from agents.base_agent import BaseAgent
from core.llm_integration import llm_router
from utils.logger import logger


class CodeAgent(BaseAgent):
    """
    Agent specialized in code generation, debugging, and refactoring
    """
    
    def __init__(self):
        super().__init__(
            name="CodeAgent",
            description="Specialized in code generation, debugging, and refactoring"
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code-related task"""
        task_type = task.get("type", "generate")
        language = task.get("language", "python")
        description = task.get("description", "")
        code = task.get("code", "")
        
        if task_type == "generate":
            return await self._generate_code(description, language)
        elif task_type == "debug":
            return await self._debug_code(code, language, description)
        elif task_type == "refactor":
            return await self._refactor_code(code, language)
        elif task_type == "explain":
            return await self._explain_code(code, language)
        else:
            raise ValueError(f"Unknown task type: {task_type}")
    
    async def _generate_code(self, description: str, language: str) -> Dict[str, Any]:
        """Generate code from description"""
        prompt = f"""Generate {language} code for the following task:

{description}

Provide clean, well-documented code with comments."""
        
        code = await llm_router.generate_response(
            prompt,
            system_prompt=f"You are an expert {language} programmer. Write clean, efficient code.",
            task_type="coding",
            temperature=0.3
        )
        
        return {"code": code, "language": language}
    
    async def _debug_code(self, code: str, language: str, issue: str) -> Dict[str, Any]:
        """Debug code and fix issues"""
        prompt = f"""Debug this {language} code:

```{language}
{code}
```

Issue: {issue}

Provide the fixed code with explanations of what was wrong."""
        
        response = await llm_router.generate_response(
            prompt,
            system_prompt=f"You are an expert {language} debugger.",
            task_type="coding",
            temperature=0.2
        )
        
        return {"fixed_code": response, "language": language}
    
    async def _refactor_code(self, code: str, language: str) -> Dict[str, Any]:
        """Refactor code for better quality"""
        prompt = f"""Refactor this {language} code to improve readability and efficiency:

```{language}
{code}
```

Provide the refactored code with explanations."""
        
        refactored = await llm_router.generate_response(
            prompt,
            system_prompt=f"You are an expert {language} code reviewer.",
            task_type="coding",
            temperature=0.3
        )
        
        return {"refactored_code": refactored, "language": language}
    
    async def _explain_code(self, code: str, language: str) -> Dict[str, Any]:
        """Explain what code does"""
        prompt = f"""Explain what this {language} code does:

```{language}
{code}
```

Provide a clear, detailed explanation."""
        
        explanation = await llm_router.generate_response(
            prompt,
            system_prompt="You are a programming instructor.",
            task_type="coding",
            temperature=0.4
        )
        
        return {"explanation": explanation, "language": language}


class ResearchAgent(BaseAgent):
    """
    Agent specialized in web research and information gathering
    """
    
    def __init__(self):
        super().__init__(
            name="ResearchAgent",
            description="Specialized in web research and information gathering"
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research task"""
        query = task.get("query", "")
        
        # Use LLM to generate comprehensive research
        prompt = f"""Research the following topic and provide detailed information:

{query}

Include:
- Key facts and information
- Recent developments
- Relevant sources and references"""
        
        research = await llm_router.generate_response(
            prompt,
            system_prompt="You are a research assistant. Provide accurate, well-sourced information.",
            task_type="general",
            temperature=0.5,
            max_tokens=3000
        )
        
        return {"research": research, "query": query}


class DataAnalysisAgent(BaseAgent):
    """
    Agent specialized in data analysis and visualization
    """
    
    def __init__(self):
        super().__init__(
            name="DataAnalysisAgent",
            description="Specialized in data processing and analysis"
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute data analysis task"""
        data_description = task.get("data", "")
        analysis_type = task.get("analysis_type", "general")
        
        prompt = f"""Analyze the following data:

{data_description}

Analysis type: {analysis_type}

Provide:
- Statistical summary
- Key insights
- Recommendations
- Suggested visualizations"""
        
        analysis = await llm_router.generate_response(
            prompt,
            system_prompt="You are a data scientist. Provide thorough analysis.",
            task_type="analysis",
            temperature=0.4
        )
        
        return {"analysis": analysis, "type": analysis_type}


class DevOpsAgent(BaseAgent):
    """
    Agent specialized in DevOps, CI/CD, and infrastructure
    """
    
    def __init__(self):
        super().__init__(
            name="DevOpsAgent",
            description="Specialized in DevOps, CI/CD, and infrastructure management"
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute DevOps task"""
        operation = task.get("operation", "")
        context = task.get("context", "")
        
        prompt = f"""DevOps task: {operation}

Context: {context}

Provide:
- Step-by-step implementation plan
- Commands to execute
- Configuration files needed
- Best practices and considerations"""
        
        plan = await llm_router.generate_response(
            prompt,
            system_prompt="You are a DevOps expert. Provide practical, secure solutions.",
            task_type="general",
            temperature=0.3
        )
        
        return {"plan": plan, "operation": operation}


class SecurityAgent(BaseAgent):
    """
    Agent specialized in security audits and vulnerability scanning
    """
    
    def __init__(self):
        super().__init__(
            name="SecurityAgent",
            description="Specialized in security audits and vulnerability scanning"
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute security task"""
        code = task.get("code", "")
        system = task.get("system", "")
        
        if code:
            return await self._audit_code(code)
        elif system:
            return await self._audit_system(system)
        else:
            raise ValueError("Need code or system to audit")
    
    async def _audit_code(self, code: str) -> Dict[str, Any]:
        """Audit code for security vulnerabilities"""
        prompt = f"""Perform a security audit on this code:

```
{code}
```

Identify:
- Security vulnerabilities
- Best practice violations
- Potential exploits
- Recommendations for fixes"""
        
        audit = await llm_router.generate_response(
            prompt,
            system_prompt="You are a cybersecurity expert. Identify all security issues.",
            task_type="general",
            temperature=0.2
        )
        
        return {"security_audit": audit, "type": "code"}
    
    async def _audit_system(self, system: str) -> Dict[str, Any]:
        """Audit system configuration"""
        prompt = f"""Perform a security audit on this system configuration:

{system}

Analyze:
- Configuration security
- Access controls
- Network security
- Compliance with best practices"""
        
        audit = await llm_router.generate_response(
            prompt,
            system_prompt="You are a system security expert.",
            task_type="general",
            temperature=0.2
        )
        
        return {"security_audit": audit, "type": "system"}


class DocumentationAgent(BaseAgent):
    """
    Agent specialized in generating documentation
    """
    
    def __init__(self):
        super().__init__(
            name="DocumentationAgent",
            description="Specialized in generating documentation and READMEs"
        )
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute documentation task"""
        doc_type = task.get("type", "readme")
        content = task.get("content", "")
        project_name = task.get("project_name", "Project")
        
        if doc_type == "readme":
            return await self._generate_readme(project_name, content)
        elif doc_type == "api":
            return await self._generate_api_docs(content)
        elif doc_type == "comments":
            return await self._add_code_comments(content)
        else:
            raise ValueError(f"Unknown documentation type: {doc_type}")
    
    async def _generate_readme(self, project_name: str, description: str) -> Dict[str, Any]:
        """Generate README file"""
        prompt = f"""Generate a comprehensive README.md for this project:

Project Name: {project_name}
Description: {description}

Include:
- Project overview
- Features
- Installation instructions
- Usage examples
- Configuration
- Contributing guidelines
- License"""
        
        readme = await llm_router.generate_response(
            prompt,
            system_prompt="You are a technical writer. Create clear, professional documentation.",
            task_type="general",
            temperature=0.5
        )
        
        return {"documentation": readme, "type": "readme"}
    
    async def _generate_api_docs(self, api_spec: str) -> Dict[str, Any]:
        """Generate API documentation"""
        prompt = f"""Generate API documentation for:

{api_spec}

Include:
- Endpoint descriptions
- Parameters
- Request/response examples
- Error codes
- Authentication"""
        
        docs = await llm_router.generate_response(
            prompt,
            system_prompt="You are an API documentation expert.",
            task_type="general",
            temperature=0.4
        )
        
        return {"documentation": docs, "type": "api"}
    
    async def _add_code_comments(self, code: str) -> Dict[str, Any]:
        """Add comments to code"""
        prompt = f"""Add comprehensive comments to this code:

```
{code}
```

Add:
- Function/class docstrings
- Inline comments for complex logic
- Type hints where appropriate"""
        
        commented = await llm_router.generate_response(
            prompt,
            system_prompt="You are a code documentation expert.",
            task_type="coding",
            temperature=0.3
        )
        
        return {"documented_code": commented, "type": "comments"}
