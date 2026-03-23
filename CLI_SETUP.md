# Syntra CLI - Setup & Usage Guide

## Quick Start

### 1. Install Dependencies

Dependencies are already installed, but if you need to reinstall:

```bash
pip install typer rich httpx aiohttp
```

### 2. Start the Backend Server

The CLI needs the Syntra API server running:

```bash
# Option 1: Using uvicorn (recommended for development)
cd /Users/snapp/Desktop/projects/Goalixa/Services/syntra
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Option 2: Using Docker Compose
docker-compose up
```

### 3. Use the CLI

In a **new terminal** (keep the server running):

```bash
# Navigate to project directory
cd /Users/snapp/Desktop/projects/Goalixa/Services/syntra

# Show help
python syntra_cli.py --help

# Show CLI info
python syntra_cli.py info

# List agents
python syntra_cli.py agents

# List tools
python syntra_cli.py tools
```

## All CLI Commands

### Ask Command
Ask Syntra AI to perform a task:

```bash
python CLI/syntra_cli.py ask "list all pods in production namespace"

# With custom server
python CLI/syntra_cli.py ask "check pod status" --server http://localhost:8000

# JSON output
python CLI/syntra_cli.py ask "list pods" --json
```

### Interactive Mode

#### Standard Interactive Mode
Start an interactive session (like ChatGPT):

```bash
python CLI/syntra_cli.py interactive
```

Then type commands:
```
🤖 syntra (0)> list pods in default namespace
🤖 syntra (1)> check logs for auth service
🤖 syntra (2)> deploy latest version
🤖 syntra (3)> exit
```

**Interactive commands:**
- `help` - Show available commands
- `clear` - Clear the screen
- `stats` - Show session statistics
- `exit` or `quit` or `q` - Exit interactive mode
- `Ctrl+C` - Exit with confirmation

#### Enhanced REPL Mode (Recommended)
For the best experience with history and better UX:

```bash
python CLI/syntra_repl.py
```

**Features:**
- 📜 Command history (up to 100 commands)
- 📊 Session statistics
- ⌨️ Better prompt with query counter
- 🎯 Markdown rendering for responses
- 💡 Enhanced help system
- 🔄 Graceful exit on Ctrl+C

**REPL Commands:**
```
help      - Show help
clear     - Clear screen
history   - Show command history
stats     - Show session statistics
server    - Show server information
exit      - Exit REPL
```

### Health Check
Check if the API server is running:

```bash
python syntra_cli.py health
```

### Info Command
Show CLI information:

```bash
python syntra_cli.py info
```

### Agents Command
List available agents:

```bash
python syntra_cli.py agents
```

### Tools Command
List available tools:

```bash
python syntra_cli.py tools
```

### Version
Show CLI version:

```bash
python syntra_cli.py --version
```

## Quick Reference

| Command | Description |
|---------|-------------|
| `python syntra_cli.py ask <prompt>` | Ask AI to perform a task |
| `python syntra_cli.py interactive` | Start interactive mode |
| `python syntra_cli.py health` | Check API health |
| `python syntra_cli.py info` | Show CLI info |
| `python syntra_cli.py agents` | List agents |
| `python syntra_cli.py tools` | List tools |
| `python syntra_cli.py --help` | Show help |
| `python syntra_cli.py --version` | Show version |

## Tips

1. **Keep server running**: Always run the backend server in a separate terminal
2. **Use interactive mode**: Best for multiple questions in one session
3. **Custom server**: Use `--server` flag to connect to different environments
4. **JSON output**: Use `--json` flag for script-friendly output

## Troubleshooting

### "Failed to connect" error
- Make sure the backend server is running
- Check the server URL with `--server` flag
- Verify server is running on port 8000

### "Module not found" error
- Make sure you're in the project directory
- Install dependencies: `pip install typer rich httpx aiohttp`

### CLI not working
- Use full path: `python syntra_cli.py command`
- Or run from project directory

## Examples

### Example 1: Quick health check
```bash
# Terminal 1: Start server
uvicorn main:app --reload

# Terminal 2: Check health
python syntra_cli.py health
```

### Example 2: Interactive session
```bash
# Terminal 1: Start server
uvicorn main:app --reload

# Terminal 2: Start interactive mode
python syntra_cli.py interactive
> list pods in default namespace
> check auth service status
> exit
```

### Example 3: Single command
```bash
# Terminal 1: Start server
uvicorn main:app --reload

# Terminal 2: Ask a question
python syntra_cli.py ask "list all services in production"
```

## Next Steps

1. Start the backend server: `uvicorn main:app --reload`
2. Test CLI: `python syntra_cli.py health`
3. Try interactive mode: `python syntra_cli.py interactive`
4. Explore all commands: `python syntra_cli.py --help`
