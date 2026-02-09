#!/bin/bash

# JARVIS Quick Start Script
# This script helps you get started with JARVIS quickly

set -e

echo "============================================"
echo "JARVIS AI Assistant - Quick Start"
echo "============================================"
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✓ Found Python $PYTHON_VERSION"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip -q
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt -q
echo "✓ Dependencies installed"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Setting up environment configuration..."
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your API keys"
    echo "   Required: OPENAI_API_KEY"
    echo "   Optional: ANTHROPIC_API_KEY, GOOGLE_API_KEY, etc."
    echo ""
    read -p "Press Enter after you've added your API keys to .env..."
else
    echo "✓ .env file already exists"
fi
echo ""

# Run tests
echo "Running tests to verify installation..."
if pytest tests/ -v --tb=short; then
    echo "✓ All tests passed!"
else
    echo "⚠️  Some tests failed, but you can still use JARVIS"
    echo "   Note: Some tests may fail without API keys configured"
fi
echo ""

echo "============================================"
echo "Installation Complete! 🎉"
echo "============================================"
echo ""
echo "Quick Start Commands:"
echo "  python main.py --mode text      # Interactive text mode"
echo "  python main.py --mode voice     # Voice mode (requires microphone)"
echo "  python main.py --mode server    # API server mode"
echo "  python main.py --query \"hello\"  # Single query"
echo "  python demo.py                  # Run demonstration"
echo ""
echo "Documentation:"
echo "  README.md  - Project overview"
echo "  SETUP.md   - Detailed setup guide"
echo ""
echo "To get started, try:"
echo "  python main.py --mode text"
echo ""
