#!/bin/bash

# Weather MCP Server Setup Script
echo "🌤️ Setting up Weather MCP Server..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or later."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
if python3 -m venv weather_env; then
    echo "✅ Virtual environment created"
else
    echo "❌ Failed to create virtual environment"
    echo "💡 You may need to install python3-venv:"
    echo "   sudo apt install python3-venv  # On Ubuntu/Debian"
    echo "   brew install python3           # On macOS"
    exit 1
fi

# Activate virtual environment and install dependencies
echo "📥 Installing dependencies..."
source weather_env/bin/activate

if pip install -r requirements.txt; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    echo "💡 Try installing manually:"
    echo "   source weather_env/bin/activate"
    echo "   pip install mcp httpx pydantic"
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "🚀 To run the weather MCP server:"
echo "   source weather_env/bin/activate"
echo "   python weather_mcp_server.py"
echo ""
echo "🧪 To test in development mode:"
echo "   source weather_env/bin/activate" 
echo "   mcp dev weather_mcp_server.py"
echo ""
echo "📚 See README.md for more information and usage examples."