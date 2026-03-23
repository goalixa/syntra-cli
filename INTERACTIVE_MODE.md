# Syntra Interactive Mode Guide

## Quick Start

### Enhanced REPL (Recommended)

```bash
# Start the REPL
python syntra_repl.py

# With custom server
python syntra_repl.py http://localhost:8000
```

### Standard Interactive Mode

```bash
python syntra_cli.py interactive
```

## Interactive Commands

### REPL Commands (Enhanced Mode)

| Command | Description |
|---------|-------------|
| `help` | Show all available commands |
| `clear` | Clear the screen |
| `history` | Show command history |
| `stats` | Show session statistics |
| `server` | Show server information |
| `exit`, `quit`, `q` | Exit interactive mode |
| `Ctrl+C` | Exit with confirmation |

## Example Sessions

### Standard Mode

```bash
$ python syntra_cli.py interactive

🤖 Syntra - Goalixa AI Teammate
ℹ Connected to: http://localhost:8000
💡 Type help for commands or exit to quit

🤖 syntra (0)> list pods in default namespace

[12:30:45] Query: list pods in default namespace

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Pod status results...                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🤖 syntra (1)> check auth service logs

[12:31:02] Query: check auth service logs

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Auth service logs...                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🤖 syntra (2)> help

Available Commands:
  help   - Show this help message
  clear  - Clear the screen
  stats  - Show session statistics
  exit   - Exit interactive mode

🤖 syntra (3)> stats

Session Statistics:
  Queries: 2
  Duration: 0:01:30
  Server: http://localhost:8000

🤖 syntra (4)> exit

👋 Goodbye! (Session ended)

Session summary: 2 queries in 0:01:45
```

### Enhanced REPL Mode

```bash
$ python syntra_repl.py

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
│  🤖 Syntra - Goalixa AI Teammate                  │
│                                                    │
│  Connected to: http://localhost:8000              │
│  Type: help for commands                          │
│  Type: exit or Ctrl+C to quit                     │
│  Use: ↑/↓ arrows for command history              │
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🤖 syntra (0)> list pods

[12:30:45] Query: list pods

Thinking...
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Pod results...                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


🤖 syntra (1)> check logs

[12:31:02] Query: check logs

Thinking...
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Log results...                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛


🤖 syntra (2)> history

Command History:
    1. list pods
    2. check logs

🤖 syntra (3)> stats

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
│              Session Statistics                  │
├─────────────────────────────────────────────────┤
│ Queries              │ 2                        │
│ Duration             │ 0:00:45                  │
│ Server               │ http://localhost:8000    │
│ History Size         │ 2/100                    │
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

🤖 syntra (4)> exit

👋 Goodbye! (Session ended)

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
│              Session Summary                     │
├─────────────────────────────────────────────────┤
│ Queries: 2                                       │
│ Duration: 0:01:30                                │
│ History: 2 commands                              │
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

## Features

### Standard Mode Features
- ✅ Basic interactive prompt
- ✅ Query counter
- ✅ Timestamps
- ✅ Markdown rendering
- ✅ Help command
- ✅ Session statistics
- ✅ Graceful exit on Ctrl+C

### Enhanced REPL Features
- ✅ Everything from standard mode, plus:
- ✅ Command history (up to 100 commands)
- ✅ Better welcome screen
- ✅ Enhanced help system
- ✅ Server information command
- ✅ Session summary on exit
- ✅ Better formatting

## Tips

1. **Use REPL mode for development** - Better history and UX
2. **Use standard mode for quick tests** - Lightweight
3. **Type `help`** - See all available commands
4. **Use `history`** - Review your commands
5. **Check `stats`** - See session metrics
6. **Exit gracefully** - Use `exit` or Ctrl+C

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Exit with confirmation |
| `Ctrl+D` | Not supported (use `exit`) |
| `Ctrl+L` | Use `clear` command instead |

## Comparison with Claude Code/Codex

| Feature | Syntra REPL | Claude Code | Codex |
|---------|-------------|-------------|-------|
| Interactive Prompt | ✅ | ✅ | ✅ |
| Command History | ✅ (100) | ✅ | ✅ |
| Session Stats | ✅ | ❌ | ❌ |
| Markdown Output | ✅ | ✅ | ✅ |
| Help System | ✅ | ✅ | ✅ |
| Ctrl+C Exit | ✅ | ✅ | ✅ |
| Open Source | ✅ | ❌ | ❌ |
