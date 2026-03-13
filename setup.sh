#!/bin/bash

# Setup script for LangGraph MCP Agent Project

echo "=========================================="
echo "LangGraph MCP Agent - Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "📋 Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Create virtual environment
echo "🔨 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📄 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo "⚠️  Please edit .env and add your API keys"
else
    echo "ℹ️  .env file already exists"
fi
echo ""

echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To use the project:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Edit .env file with your API keys"
echo "  3. Run the MCP server: python3 main.py --server"
echo "  4. In another terminal, run: python3 main.py --interactive"
echo ""
echo "For help: python3 main.py --help"
echo ""
