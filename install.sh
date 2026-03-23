#!/bin/bash
# Syntra Installation Script

echo "🚀 Installing Syntra..."
echo ""

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip first."
    exit 1
fi

# Install in editable mode
echo "📦 Installing Syntra package..."
pip install -e .

echo ""
echo "✅ Installation complete!"
echo ""
echo "You can now use these commands:"
echo "  syntra       - Main CLI tool"
echo "  syntra-repl  - Enhanced REPL mode"
echo "  syntra-api   - Start API server"
echo ""
echo "Try it:"
echo "  syntra --help"
echo ""
