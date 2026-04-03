# Syntra CLI Design Document

## Overview

Syntra CLI is a modern, extensible command-line interface for the Goalixa AI DevOps Teammate. Inspired by Claude's CLI architecture, it features a plugin/skill system, rich configuration management, and beautiful terminal output.

## Architecture Principles

1. **Modularity**: Every feature is a skill/plugin that can be added/removed independently
2. **Composability**: Skills can depend on and compose with other skills
3. **Configuration Hierarchy**: Environment variables > user config > project config > defaults
4. **Beautiful Output**: Rich terminal UI with progress indicators, tables, and markdown rendering
5. **Session Persistence**: Context and state maintained across CLI invocations

## Directory Structure

```
syntra-cli/
├── syntra_pkg/
│   ├── __init__.py           # Package init, version exports
│   ├── cli.py                # Entry point (thin wrapper)
│   ├── _cli_impl.py          # Main CLI implementation
│   ├── config/
│   │   ├── __init__.py       # Config exports
│   │   ├── settings.py       # Settings manager (Claude-style)
│   │   ├── defaults.py       # Default configuration
│   │   └── schema.py         # Configuration schema/validation
│   ├── skills/
│   │   ├── __init__.py       # Skill system exports
│   │   ├── base.py           # Base skill class/interface
│   │   ├── registry.py       # Skill registry and discovery
│   │   ├── loader.py         # Skill loader from paths
│   │   └── builtin/          # Built-in skills
│   │       ├── __init__.py
│   │       ├── ask.py        # Core ask command
│   │       ├── chat.py       # Interactive chat
│   │       ├── config.py     # Config management
│   │       ├── health.py     # Health checks
│   │       └── agents.py     # Agent management
│   ├── api/
│   │   ├── __init__.py
│   │   ├── client.py         # HTTP client for Syntra API
│   │   └── stream.py         # Streaming response handler
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── console.py        # Rich console instance
│   │   ├── theme.py          # Custom theme definitions
│   │   ├── spinner.py        # Spinner utilities
│   │   └── format.py         # Output formatters
│   ├── session/
│   │   ├── __init__.py
│   │   ├── manager.py        # Session state management
│   │   └── history.py        # Command history
│   └── utils/
│       ├── __init__.py
│       ├── fs.py             # File system utilities
│       ├── git.py            # Git utilities
│       └── env.py            # Environment helpers
├── ~/.syntra/                # User data directory
│   ├── config.json           # User configuration
│   ├── skills/               # User-installed skills
│   ├── sessions/             # Session data
│   └── history               # Command history
└── .syntra/                  # Project-local directory
    ├── config.local.json     # Project overrides
    └── skills/               # Project-local skills
```

## Configuration System

### Settings Hierarchy (Claude-style)

1. **Built-in Defaults** - Hardcoded in `defaults.py`
2. **Project Config** - `.syntra/config.local.json` (git-ignored)
3. **User Config** - `~/.syntra/config.json`
4. **Environment Variables** - `SYNTRA_*` prefix

### Settings Schema

```python
{
    # Core Settings
    "api": {
        "base_url": "http://localhost:8000",
        "timeout": 30.0,
        "max_retries": 3,
        "verify_ssl": true
    },

    # CLI Settings
    "cli": {
        "theme": "default",
        "color_scheme": "auto",
        "prompt_style": "fancy",
        "enable_completion": true
    },

    # Session Settings
    "session": {
        "persist_context": true,
        "max_history": 1000,
        "timeout": 1800,
        "auto_save": true
    },

    # Skill Settings
    "skills": {
        "enabled": ["ask", "chat", "config", "health"],
        "paths": ["~/.syntra/skills", ".syntra/skills"],
        "auto_discover": true
    },

    # Output Settings
    "output": {
        "format": "rich",      # rich, json, markdown, plain
        "stream": true,        # Enable streaming responses
        "show_metadata": false,
        "timestamp": false
    },

    # Editor Integration
    "editor": {
        "external": null,      # External editor command
        "timeout": 30
    },

    # Development Settings
    "dev": {
        "debug": false,
        "log_level": "INFO",
        "trace_requests": false
    }
}
```

### Settings API

```bash
# View all settings
syntra settings

# Get specific setting
syntra settings api.base_url

# Set setting
syntra settings api.base_url https://api.syntra.dev

# Unset (revert to default)
syntra settings api.base_url --unset

# List with defaults
syntra settings --all

# Edit in editor
syntra settings --edit
```

## Skill System

### Skill Interface

Every skill must implement the `Skill` interface:

```python
from abc import ABC, abstractmethod
from typing import Optional, List
import typer

class Skill(ABC):
    """Base class for all Syntra skills."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique skill identifier."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Skill version."""
        pass

    @property
    def description(self) -> str:
        """Human-readable description."""
        return ""

    @property
    def dependencies(self) -> List[str]:
        """List of skill names this depends on."""
        return []

    @abstractmethod
    def register(self, app: typer.Typer) -> None:
        """Register commands with the Typer app."""
        pass

    def initialize(self) -> None:
        """Called when skill is loaded."""
        pass

    def shutdown(self) -> None:
        """Called when CLI exits."""
        pass
```

### Skill Example

```python
# skills/builtin/ask.py
from syntra_pkg.skills.base import Skill
import typer

class AskSkill(Skill):
    name = "ask"
    version = "1.0.0"
    description = "Ask Syntra AI a single question"

    def register(self, app: typer.Typer) -> None:
        @app.command()
        def ask(
            prompt: str = typer.Argument(..., help="Your question"),
            json: bool = typer.Option(False, "--json", help="JSON output")
        ):
            """Ask Syntra AI a question."""
            # Implementation
            pass
```

### Skill Discovery

Skills are auto-discovered from:
1. Built-in skills: `syntra_pkg/skills/builtin/`
2. User skills: `~/.syntra/skills/`
3. Project skills: `.syntra/skills/`

```bash
# List installed skills
syntra skills list

# Show skill info
syntra skills info ask

# Enable/disable skill
syntra skills enable github
syntra skills disable github

# Install skill from URL
syntra skills install https://github.com/user/syntra-skill

# Create new skill
syntra skills create my-skill
```

## Command Structure

### Top-Level Commands

```bash
syntra                           # Start interactive mode
syntra ask "question"            # Single question
syntra chat                      # Interactive chat
syntra settings [key] [val]      # Manage settings
syntra skills                    # Skill management
syntra agents                    # Agent management
syntra health                    # Health check
syntra info                      # CLI information
```

### Global Options

```bash
--config PATH      # Custom config file
--debug            # Enable debug mode
--quiet            # Minimal output
--verbose          # Verbose output
--no-color         # Disable colors
--format FORMAT    # Output format (rich/json/md/plain)
--version          # Show version
--help             # Show help
```

## Interactive Mode

### REPL Features

```bash
syntra
```

**Features:**
- Persistent session context
- Command history (up/down arrows)
- Auto-completion (tab)
- Multi-line input (alt+enter)
- Slash commands
- Syntax highlighting

**Slash Commands:**

```
/help              Show available commands
/clear             Clear conversation context
/exit              Exit CLI
/settings          View/edit settings
/skills            Manage skills
/agent [name]      Switch agent
/history           Show session history
/export            Export conversation
/md                Toggle markdown rendering
```

### Prompt Styles

```
# Fancy (default)
syntra (3) >

# Minimal
>

# Context-aware
syntra [production] (3) >

# Custom
🚀 syntra >
```

## Output Formats

### Rich (Default)

Beautiful terminal output with colors, tables, and formatting.

### JSON

```bash
syntra ask "list pods" --format json
```

```json
{
  "result": "...",
  "metadata": {
    "agent": "devops",
    "duration_ms": 1234,
    "tokens_used": 150
  }
}
```

### Markdown

```bash
syntra ask "explain k8s" --format md
```

Output in pure markdown format.

### Plain

No formatting, pure text output.

## Session Management

### Session State

```bash
# Save current session
syntra session save "investigation-1"

# List sessions
syntra session list

# Load session
syntra session load investigation-1

# Delete session
syntra session delete investigation-1
```

### Session Storage

Sessions stored in `~/.syntra/sessions/`:

```
~/.syntra/sessions/
├── investigation-1.json
├── daily-standup-2.json
└── config-debug-3.json
```

Each session contains:
- Conversation history
- Context state
- Metadata (timestamp, queries, etc.)
- Skill state

## Editor Integration

```bash
# Edit prompt in external editor
syntra ask --editor

# Edit long-form input
syntra chat --editor
```

Respects `$EDITOR` environment variable.

## Git Integration

```bash
# Auto-detect git context
syntra ask "why is the build failing"

# Manual context
syntra ask "review this PR" --context pr-123
```

## Configuration Files

### User Config: `~/.syntra/config.json`

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

### Project Config: `.syntra/config.local.json`

```json
{
  "api": {
    "base_url": "http://localhost:3000"
  },
  "skills": {
    "enabled": ["ask", "github", "jira"]
  }
}
```

Git-ignored by default (in `.gitignore`).

## Theming

### Built-in Themes

- `default` - Blue/cyan primary
- `dark` - Dark mode optimized
- `light` - Light mode
- `minimal` - Minimal colors
- `hacker` - Green terminal style

### Custom Theme

```json
{
  "cli": {
    "theme": {
      "primary": "bright_blue",
      "success": "green",
      "warning": "yellow",
      "error": "red",
      "info": "cyan",
      "dim": "dim"
    }
  }
}
```

## Progress Indicators

```python
from syntra_pkg.ui.spinner import with_spinner

@with_spinner("Connecting to API...")
def connect():
    # Do work
    pass
```

Shows beautiful spinners for long operations.

## Streaming Responses

```bash
# Enable streaming
syntra ask "explain kubernetes" --stream

# Or in settings
syntra settings output.stream true
```

Real-time token streaming from the API.

## Error Handling

```bash
# User-friendly errors
$ syntra ask "pods"
✗ Error: No context specified. Use --context or run in a git repository.

# Debug mode
$ syntra ask "pods" --debug
[DEBUG] GET /api/ask HTTP/1.1
[DEBUG] Host: localhost:8000
[DEBUG] Response: 400 Bad Request
✗ Error: No context specified
```

## Logging

```bash
# View logs
syntra logs

# Follow logs
syntra logs --follow

# Filter by level
syntra logs --level ERROR
```

Logs stored in `~/.syntra/logs/`.

## Completion

```bash
# Generate completion script
syntra completion bash
syntra completion zsh
syntra completion fish
```

Install for auto-completion of commands and options.

## Examples

### Daily Workflow

```bash
# Start interactive mode
syntra

# In REPL
> /help
> list all failing deployments in production
> /save "prod-outage-2024-04-03"
> explain the root cause
> create a postmortem document
> /export markdown > ~/postmortem.md
> /exit
```

### CI/CD Integration

```bash
# In CI pipeline
syntra ask "check build status" --format json --quiet > result.json
if jq -e '.success' result.json; then
  echo "Build is healthy"
else
  syntra ask "investigate build failure"
fi
```

### Git Hook

```bash
# .git/hooks/pre-commit
syntra ask "review these changes" --format json
```

## Implementation Phases

### Phase 1: Core Refactor
- [ ] Implement settings system
- [ ] Refactor configuration to hierarchy
- [ ] Add skill base classes
- [ ] Implement skill registry

### Phase 2: Built-in Skills
- [ ] Extract existing commands to skills
- [ ] Implement `ask` skill
- [ ] Implement `chat` skill
- [ ] Implement `config` skill (rename from settings)
- [ ] Implement `health` skill
- [ ] Implement `agents` skill

### Phase 3: Enhanced UX
- [ ] Rich prompt customization
- [ ] Multiple output formats
- [ ] Session persistence
- [ ] Command history
- [ ] Auto-completion

### Phase 4: Extensibility
- [ ] Skill loader from paths
- [ ] Skill CLI (install/uninstall/list)
- [ ] Skill templates
- [ ] Third-party skill support

### Phase 5: Polish
- [ ] Comprehensive tests
- [ ] Documentation
- [ ] Examples
- [ ] Performance optimization

## Dependencies

```toml
[project]
dependencies = [
    "typer[all]>=0.9.0",
    "rich>=14.0.0",
    "httpx>=0.25.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
    "prompt-toolkit>=3.0.0",
    "toml>=0.10.0",
]
```

## Versioning

Following Semantic Versioning:
- MAJOR: Breaking changes to CLI or skill API
- MINOR: New features, backward compatible
- PATCH: Bug fixes

## License

MIT License - See LICENSE file
