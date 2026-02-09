#!/usr/bin/env python3
"""
Demo script showing JARVIS capabilities
Run this to see examples of what JARVIS can do
"""
import asyncio
import sys
import os

from core.jarvis import jarvis
from utils.logger import logger


async def demo():
    """Run demonstration of JARVIS features"""
    
    print("=" * 70)
    print("JARVIS AI Assistant - Demonstration")
    print("=" * 70)
    print()
    
    demos = [
        {
            "name": "System Command",
            "query": "list files in current directory",
            "description": "Translates natural language to 'ls -la' command"
        },
        {
            "name": "General Query",
            "query": "what is artificial intelligence?",
            "description": "Uses LLM to answer general questions"
        },
        {
            "name": "Code Generation",
            "query": "write a python function to reverse a string",
            "description": "Generates code using Code Agent"
        },
        {
            "name": "Information Request",
            "query": "what's the weather in New York?",
            "description": "Fetches weather information via API"
        }
    ]
    
    for i, demo in enumerate(demos, 1):
        print(f"\n{'=' * 70}")
        print(f"Demo {i}: {demo['name']}")
        print(f"Description: {demo['description']}")
        print(f"{'=' * 70}")
        print(f"\nQuery: {demo['query']}")
        print("\nProcessing...")
        
        try:
            result = await jarvis.process_query(demo['query'], voice_output=False)
            
            print(f"\n✓ Intent: {result.get('intent', 'unknown')}")
            print(f"✓ Success: {result.get('success', False)}")
            print(f"\nResponse:")
            print("-" * 70)
            response = result.get('response', 'No response')
            # Limit output length for demo
            if len(response) > 500:
                print(response[:500] + "...\n[Truncated for demo]")
            else:
                print(response)
            print("-" * 70)
            
            if not result.get('success'):
                print(f"\n⚠ Note: {result.get('error', 'Unknown error')}")
                if 'API' in str(result.get('error', '')):
                    print("   This feature requires API keys to be configured in .env")
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
            logger.error(f"Demo error: {e}")
        
        print("\nPress Enter to continue to next demo...")
        input()
    
    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print("\nTo use JARVIS interactively, run:")
    print("  python main.py --mode text    # Text mode")
    print("  python main.py --mode voice   # Voice mode")
    print("  python main.py --mode server  # API server")
    print()


async def quick_test():
    """Quick test without user interaction"""
    print("Running quick test...")
    print()
    
    # Test 1: Simple greeting
    print("Test 1: Simple greeting")
    result = await jarvis.process_query("Hello JARVIS", voice_output=False)
    print(f"✓ Response received: {result.get('success', False)}")
    print()
    
    # Test 2: System info
    print("Test 2: System command")
    result = await jarvis.process_query("show current directory", voice_output=False)
    print(f"✓ Command executed: {result.get('success', False)}")
    print()
    
    print("Quick test complete!")
    print()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="JARVIS Demo")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick test without interaction"
    )
    
    args = parser.parse_args()
    
    try:
        if args.quick:
            asyncio.run(quick_test())
        else:
            asyncio.run(demo())
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\nDemo error: {e}")
        logger.error(f"Demo fatal error: {e}")
