# Syntra Installation - Quick Start

## Installation Complete!

Syntra has been successfully installed. You can now use the `syntra` command from anywhere.

## Available Commands

### Main CLI
```bash
syntra --help
```

### Commands Available:
- `syntra ask <prompt>` - Ask Syntra AI to perform a task
- `syntra interactive` - Start interactive mode
- `syntra health` - Check API health
- `syntra info` - Show CLI information
- `syntra agents` - List available agents
- `syntra tools` - List available tools
- `syntra --version` - Show version

### Enhanced REPL
```bash
syntra-repl --help
```

## Usage Examples

### Basic Usage
```bash
# Ask a question
syntra ask "list pods in production"

# Check health
syntra health

# Show info
syntra info
```

### Interactive Mode
```bash
# Standard interactive
syntra interactive

# Enhanced REPL (with history)
syntra-repl
```

## Installation Location

The package is installed in your virtual environment:
```
/Users/snapp/Desktop/projects/Goalixa/Services/syntra/.venv/bin/syntra
/Users/snapp/Desktop/projects/Goalixa/Services/syntra/.venv/bin/syntra-repl
```

## Running Scripts Directly (Development)

If you want to run scripts without installation:

```bash
# From project root
python CLI/syntra_cli.py --help
python CLI/syntra_repl.py
```

## Project Structure

```
syntra/
├── CLI/                       # All CLI-related files
│   ├── syntra_cli.py          # Main CLI script
│   ├── syntra_repl.py         # Enhanced REPL script
│   ├── syntra                 # Executable script
│   ├── syntra_pkg/            # Package for pip install
│   │   ├── cli.py             # CLI entry point
│   │   ├── repl.py            # REPL entry point
│   │   └── _cli_impl.py       # CLI implementation
│   └── ...
├── main.py                    # FastAPI application
├── requirements.txt           # Dependencies
├── setup.py                   # Setup configuration
└── pyproject.toml            # Modern Python config
```

## Next Steps

1. Start the API server:
   ```bash
   uvicorn main:app --reload
   ```

2. In a new terminal, use Syntra:
   ```bash
   syntra health
   syntra ask "list pods"
   syntra-repl
   ```

## Troubleshooting

### Command not found

If `syntra` command is not found, make sure your virtual environment is activated:

```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Then use syntra
syntra --help
```

### Dependencies missing

If you get import errors:

```bash
pip install typer rich httpx aiohttp
```

## Uninstall

```bash
pip uninstall syntra
```

## Reinstall

```bash
pip install -e . --force-reinstall
```
