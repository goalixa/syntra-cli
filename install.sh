#!/bin/bash
# Installation script for syntra-cli

echo "🚀 Installing syntra-cli..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_BIN="$SCRIPT_DIR/.venv/bin"

# Check if virtual environment exists
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv "$SCRIPT_DIR/.venv"
fi

# Install the package in editable mode
echo "📦 Installing package..."
$VENV_BIN/pip install -e .

# Create a symlink or add to PATH
echo ""
echo "✅ Installation complete!"
echo ""
echo "To use syntra-cli, you can:"
echo ""
echo "1. Add this to your shell profile (~/.zshrc or ~/.bashrc):"
echo "   export PATH=\"$VENV_BIN:\$PATH\""
echo ""
echo "2. Or run it directly:"
echo "   $VENV_BIN/syntra-cli"
echo ""
echo "3. Or use the alias (add to your shell profile):"
echo "   alias syntra-cli='$VENV_BIN/syntra-cli'"
echo ""
