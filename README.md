# Syntra CLI

> 🚀 Syntra - Goalixa AI DevOps Teammate CLI

An interactive CLI tool for communicating with Syntra AI, your DevOps teammate. Now with a skill-based architecture and hierarchical configuration system.

## Installation

```bash
# Clone and install
git clone <repo-url>
cd syntra-cli
python3 -m venv .venv
.venv/bin/pip install -e .
```

## Usage

### Interactive Mode (Default)

Running `syntra-cli` without any arguments starts the interactive REPL:

```bash
syntra-cli
```

You'll see:
```
🤖 Syntra - Goalixa AI Teammate
ℹ Connected to: http://localhost:8000
💡 Type help for commands or exit to quit
📋 Skills: ask, chat, config, health, agents, info

syntra >
```

### Interactive Commands

| Command | Description |
|---------|-------------|
| `help` | Show available commands |
| `clear` | Clear the screen |
| `exit` or `quit` or `q` | Exit interactive mode |
| `/clear` | Clear conversation context |
| `/info` | Show session information |
| `/settings` | Show current settings |
| `/skills` | List available skills |

### Single-Shot Commands

Ask a single question:
```bash
syntra-cli ask "list all pods in production namespace"
```

Check API health:
```bash
syntra-cli health
```

Show CLI information:
```bash
syntra-cli info
```

List available agents:
```bash
syntra-cli agents
```

## Configuration

Syntra CLI uses a hierarchical configuration system:

1. **Built-in defaults** - Hardcoded defaults
2. **Project config** - `.syntra/config.local.json` (git-ignored)
3. **User config** - `~/.syntra/config.json`
4. **Environment variables** - `SYNTRA_*` prefix

### Settings Command

Manage your CLI configuration:

```bash
# List all configuration
syntra-cli settings

# List all configuration including defaults
syntra-cli settings --all

# Get specific value
syntra-cli settings api.base_url

# Set a value
syntra-cli settings api.base_url https://api.syntra.dev

# Unset (remove) a value
syntra-cli settings api.base_url --unset

# Edit in editor
syntra-cli settings --edit

# Export configuration as JSON
syntra-cli settings --export

# Validate configuration
syntra-cli settings --validate

# Reset to defaults
syntra-cli settings --reset
```

### Configuration Files

**User Config** (`~/.syntra/config.json`):
```json
{
  "api": {
    "base_url": "https://api.syntra.dev",
    "timeout": 30.0
  },
  "cli": {
    "theme": "default",
    "prompt_style": "fancy"
  }
}
```

**Project Config** (`.syntra/config.local.json`):
```json
{
  "api": {
    "base_url": "http://localhost:3000"
  }
}
```

### Environment Variables

Override any setting with environment variables:

```bash
export SYNTRA_API_BASE_URL=https://api.syntra.dev
export SYNTRA_API_TIMEOUT=60
export SYNTRA_CLI_THEME=dark
syntra-cli ask "hello"
```

## Skill System

Syntra CLI now uses a skill-based architecture for extensibility:

```bash
# List available skills
syntra-cli /skills    # In interactive mode

# Skills are automatically discovered from:
# - Built-in skills (syntra_pkg/skills/builtin/)
# - User skills (~/.syntra/skills/)
# - Project skills (.syntra/skills/)
```

### Available Skills

- **ask** - Ask single questions
- **chat** - Interactive chat mode
- **settings** - Manage configuration
- **health** - Check API health
- **agents** - List/manage agents
- **info** - Show CLI information

## Output Formats

```bash
# Rich output (default)
syntra-cli ask "list pods"

# JSON output
syntra-cli ask "list pods" --json

# Or set as default
syntra-cli settings output.format json
```

## Command Reference

```
syntra-cli
│
├── ask              Ask Syntra AI a question
│   ├── --server     Override API server URL
│   ├── --json       Output as JSON
│   ├── --stream     Enable streaming
│   └── --context    Additional context
│
├── chat             Start interactive chat mode
│   └── --server     Override API server URL
│
├── settings         Manage configuration
│   ├── --all        List all config (including defaults)
│   ├── --unset      Remove a value
│   ├── --edit       Open in editor
│   ├── --export     Export as JSON
│   ├── --validate   Validate configuration
│   └── --reset      Reset to defaults
│
├── health           Check API health
│   ├── --server     Override API server URL
│   └── --verbose    Show detailed info
│
├── agents           List/manage agents
│   ├── --list       List agents (default)
│   └── --info       Show agent details
│
└── info             Show CLI information
    └── --verbose    Show detailed info
```

## Shell Integration

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
# If using the venv installation
export PATH="/path/to/syntra-cli/.venv/bin:$PATH"

# Or create an alias
alias syntra-cli="/path/to/syntra-cli/.venv/bin/syntra-cli"
```

## Development

```bash
# Install in editable mode
pip install -e .

# Run tests (when implemented)
pytest
```

## Design

See [DESIGN.md](DESIGN.md) for the complete architecture documentation.

## License

MIT
