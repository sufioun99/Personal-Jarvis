"""
Example: Using JARVIS API Client in Python
"""
import requests
import json
from typing import Dict, Any


class JarvisClient:
    """Simple client for JARVIS API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize JARVIS client
        
        Args:
            base_url: Base URL of JARVIS API server
        """
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check if JARVIS is healthy"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def query(self, text: str, voice_output: bool = False) -> Dict[str, Any]:
        """
        Send a query to JARVIS
        
        Args:
            text: Query text
            voice_output: Whether to enable voice output
            
        Returns:
            Response dictionary
        """
        response = self.session.post(
            f"{self.base_url}/query",
            json={"query": text, "voice_output": voice_output}
        )
        response.raise_for_status()
        return response.json()


def main():
    """Example usage"""
    client = JarvisClient("http://localhost:8000")
    
    print("JARVIS API Client Example")
    print("=" * 60)
    
    # Health check
    try:
        health = client.health_check()
        print(f"✓ JARVIS is healthy: {health.get('status')}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Simple query
    try:
        result = client.query("Hello JARVIS")
        print(f"✓ Response: {result.get('response')[:100]}...")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    main()
