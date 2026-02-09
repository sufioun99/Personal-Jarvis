#!/usr/bin/env python3
"""
JARVIS CLI - Command Line Interface
"""
import asyncio
import argparse
from core.jarvis import jarvis
from utils.logger import logger
from config import settings


async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="JARVIS - Personal AI Assistant with Voice Control"
    )
    parser.add_argument(
        "--mode",
        choices=["voice", "text", "server"],
        default="text",
        help="Interaction mode (default: text)"
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Single query to process (non-interactive)"
    )
    parser.add_argument(
        "--voice-output",
        action="store_true",
        help="Enable voice output for single query"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("JARVIS - Personal AI Assistant")
    print("Advanced AI with Voice Control and Multi-Agent System")
    print("=" * 60)
    print()
    
    # Single query mode
    if args.query:
        logger.info(f"Processing single query: {args.query}")
        result = await jarvis.process_query(args.query, voice_output=args.voice_output)
        
        print(f"Query: {result['query']}")
        print(f"Intent: {result.get('intent', 'unknown')}")
        print(f"\nResponse:\n{result.get('response', '')}")
        
        if not result.get('success'):
            print(f"\nError: {result.get('error', '')}")
        
        return
    
    # Interactive modes
    if args.mode == "voice":
        await jarvis.voice_mode()
    elif args.mode == "text":
        await jarvis.text_mode()
    elif args.mode == "server":
        print(f"Starting JARVIS API server...")
        print(f"Server will be available at http://{settings.jarvis_host}:{settings.jarvis_port}")
        print(f"API documentation at http://{settings.jarvis_host}:{settings.jarvis_port}/docs")
        print()
        
        # Import and run server
        import uvicorn
        from server import app
        
        uvicorn.run(
            app,
            host=settings.jarvis_host,
            port=settings.jarvis_port,
            log_level=settings.log_level.lower()
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nJARVIS shutting down...")
        logger.info("JARVIS stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\nFatal error: {e}")
