# Syntra CLI

> 🚀 Syntra - Goalixa AI DevOps Teammate CLI

An interactive CLI tool for communicating with Syntra AI, your DevOps teammate.

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

syntra (0)>
```

#### Interactive Commands

| Command | Description |
|---------|-------------|
| `help` | Show available commands |
| `clear` | Clear the screen |
| `exit` or `quit` or `q` | Exit interactive mode |
| `/clear` | Clear conversation context |
| `/info` | Show session information |

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

### Configuration

Manage your CLI configuration:

```bash
# List all configuration
syntra-cli config

# Set API server
syntra-cli config api_base_url http://localhost:9000

# Get specific value
syntra-cli config api_base_url

# Unset a value
syntra-cli config api_base_url --unset
```

Configuration is stored in `~/.syntra/config.json`.

### Shell Integration

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

## License

MIT
