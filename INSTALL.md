# Syntra Installation Guide

## Easy Installation (Recommended)

### Install from Source (Development Mode)

```bash
# Navigate to project directory
cd /Users/snapp/Desktop/projects/Goalixa/Services/syntra

# Install in editable mode (best for development)
pip install -e .

# Now you can use syntra from anywhere!
syntra --help
```

### Install from Source (Production Mode)

```bash
# Navigate to project directory
cd syntra

# Install normally
pip install .

# Now you can use syntra from anywhere!
syntra --help
```

## What Gets Installed

After installation, you'll have these commands available globally:

| Command | Description |
|---------|-------------|
| `syntra` | Main CLI tool |
| `syntra-repl` | Enhanced interactive REPL |
| `syntra-api` | Start the API server |

## Usage Examples

### After Installation

```bash
# Show help
syntra --help

# Ask a question
syntra ask "list pods in production"

# Interactive mode
syntra interactive

# Enhanced REPL mode (recommended)
syntra-repl

# Start API server
syntra-api

# Start API server with custom port
syntra-api --port 8080

# Start API server with auto-reload
syntra-api --reload

# Check health
syntra health

# Show info
syntra info

# List agents
syntra agents

# List tools
syntra tools
```

### Using Direct Scripts (Development)

If you don't want to install the package, you can run scripts directly:

```bash
# From project root
cd syntra

# Run CLI
python CLI/syntra_cli.py --help

# Run REPL
python CLI/syntra_repl.py

# Run with Python module
python -m CLI --help
```

## Platform-Specific Instructions

### Ubuntu / Debian / Linux

```bash
# Update pip
python3 -m pip install --upgrade pip

# Install
cd syntra
pip3 install -e .

# Use
syntra --help
```

### macOS

```bash
# Install
cd syntra
pip install -e .

# Use
syntra --help
```

### Windows

```bash
# Install
cd syntra
pip install -e .

# Use
syntra --help
```

## Uninstall

```bash
pip uninstall syntra
```

## Update

```bash
# Navigate to project directory
cd syntra

# Pull latest changes
git pull

# Reinstall
pip install -e . --force-reinstall
```

## Troubleshooting

### Command not found

If you get `command not found: syntra`:

```bash
# Check pip location
pip --version

# Make sure pip's bin directory is in your PATH
# Usually: ~/.local/bin on Linux/Mac
# Or: %APPDATA%\Python\Scripts on Windows

# Add to PATH (Linux/Mac - add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"

# Reload shell
source ~/.bashrc  # or source ~/.zshrc
```

### Permission denied

```bash
# Install to user directory
pip install -e . --user
```

### Dependencies issues

```bash
# Update pip
python -m pip install --upgrade pip

# Install with build dependencies
pip install -e . --upgrade
```

## Development Mode vs Production Mode

### Development Mode (Recommended for developers)

```bash
pip install -e .
```

**Pros:**
- Changes to code are immediately available
- Don't need to reinstall after changes
- Best for development

**Cons:**
- Requires keeping source code

### Production Mode

```bash
pip install .
```

**Pros:**
- Self-contained installation
- Don't need source code after installation

**Cons:**
- Need to reinstall after code changes

## Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install
pip install -e .

# Use
syntra --help

# Deactivate when done
deactivate
```

## Quick Start After Installation

```bash
# Terminal 1: Start API server
syntra-api --reload

# Terminal 2: Use CLI
syntra health
syntra ask "list pods"
syntra-repl
```

## Docker Installation (Alternative)

```bash
# Build image
docker build -t syntra .

# Run container
docker run -it --rm syntra syntra --help
```

## Summary

**For quick development:**
```bash
pip install -e .
syntra --help
```

**For production:**
```bash
pip install .
syntra --help
```

That's it! 🎉
