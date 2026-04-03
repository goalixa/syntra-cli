#!/usr/bin/env python3
"""
Syntra CLI Implementation - Skill-based architecture.

This is the main CLI implementation that loads skills and provides
the command-line interface.
"""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich import print as rprint

# Import from new architecture
from syntra_pkg.config import settings
from syntra_pkg.skills import skill_registry, SkillContext
from syntra_pkg import __version__

# Create console
console = Console()

# Create main Typer app
app = typer.Typer(
    name="syntra-cli",
    help="🚀 Syntra - Goalixa AI DevOps Teammate",
    no_args_is_help=False,
    add_completion=False,
    invoke_without_command=True,
    rich_markup_mode="rich",
)


# Initialize skills at module load time
def _initialize_skills_module():
    """Initialize skills when module is loaded."""
    # Discover built-in skills
    skill_registry.discover_builtin()

    # Discover user skills (if enabled)
    if settings.skills.auto_discover:
        try:
            skill_registry.discover_user_skills()
        except Exception:
            pass  # Silently skip if user skills can't be loaded

    # Register all skill commands with the app
    for skill in skill_registry.list(include_hidden=False):
        try:
            skill.register(app)
        except Exception:
            pass  # Skip skills that fail to register


# Initialize skills when module is loaded
_initialize_skills_module()


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        rprint(f"[primary]syntra-cli[/primary] version [bold]{__version__}[/bold]")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
    config: Optional[str] = typer.Option(
        None,
        "--config",
        "-C",
        help="Path to custom config file",
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable debug mode",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Minimal output",
    ),
):
    """
    Syntra - Goalixa AI DevOps Teammate.

    Running without arguments starts interactive mode.
    """
    # Handle custom config
    if config:
        settings._user_config_file = Path(config)
        settings.reload()

    # Handle debug mode
    if debug:
        settings.set("dev.debug", True, persist=False)

    # If no subcommand was provided, start interactive mode
    if ctx.invoked_subcommand is None:
        _start_interactive_mode()


def _start_interactive_mode():
    """Start the interactive REPL."""
    import httpx
    from rich.prompt import Prompt
    from rich.panel import Panel
    from rich.markdown import Markdown

    api_url = settings.api.base_url

    # Display welcome message
    console.print()
    console.print("🤖 [bold cyan]Syntra - Goalixa AI Teammate[/bold cyan]")
    console.print(f"ℹ Connected to: [cyan]{api_url}[/cyan]")
    console.print(f"💡 Type [yellow]help[/yellow] for commands or [yellow]exit[/yellow] to quit")
    console.print(f"📋 Skills: [cyan]{', '.join(settings.skills.enabled)}[/cyan]\n")

    session_queries = 0
    client = httpx.Client(
        base_url=api_url,
        timeout=settings.api.timeout,
    )

    try:
        while True:
            try:
                # Build prompt based on settings
                prompt_style = settings.cli.prompt_style
                count_display = f" [dim]({session_queries})[/dim]" if session_queries > 0 else ""

                if prompt_style == "minimal":
                    prompt_text = "> "
                elif prompt_style == "context":
                    # Get git context if available
                    try:
                        import subprocess
                        branch = subprocess.check_output(
                            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                            stderr=subprocess.DEVNULL,
                        ).decode().strip()
                        context_str = f" [{branch}]"
                    except Exception:
                        context_str = ""
                    prompt_text = f"[bold cyan]syntra{context_str}[/bold cyan]{count_display} > "
                else:
                    # Fancy (default)
                    prompt_text = f"[bold cyan]syntra[/bold cyan]{count_display} > "

                prompt = Prompt.ask(prompt_text)
                prompt = prompt.strip()

                if not prompt:
                    continue

                # Handle exit commands
                if prompt.lower() in ["exit", "quit", "q"]:
                    console.print("\n👋 Goodbye! [dim](Session ended)[/dim]\n")
                    break

                # Handle clear command
                if prompt.lower() == "clear":
                    console.clear()
                    continue

                # Handle help command
                if prompt.lower() == "help":
                    _print_interactive_help()
                    continue

                # Handle slash commands
                if prompt.startswith("/"):
                    handled = _handle_slash_command(prompt, session_queries, api_url)
                    if handled == "continue":
                        continue
                    elif handled == "exit":
                        break

                session_queries += 1

                # Send request to API
                with console.status("[primary]Thinking...[/primary]"):
                    response = client.post("/api/ask", json={"prompt": prompt})
                    response.raise_for_status()
                    result = response.json()

                result_text = result.get("result", "No response")

                # Render response
                _render_response(result_text)

            except httpx.HTTPError as e:
                console.print(f"[red]✗ Error: {e}[/red]\n")

    except KeyboardInterrupt:
        console.print("\n⚠ Exiting interactive mode...", style="yellow")

    finally:
        client.close()

        # Shutdown all skills
        skill_registry.shutdown_all()

        if session_queries > 0:
            console.print(f"[dim]Session summary: {session_queries} queries[/dim]\n")


def _print_interactive_help() -> None:
    """Print help for interactive mode."""
    console.print("\n[bold]Available Commands:[/bold]")
    console.print("  [cyan]help[/cyan]     - Show this help message")
    console.print("  [cyan]clear[/cyan]    - Clear the screen")
    console.print("  [cyan]exit[/cyan]     - Exit interactive mode")
    console.print("\n[bold]Slash Commands:[/bold]")
    console.print("  [cyan]/clear[/cyan]   - Clear conversation context")
    console.print("  [cyan]/info[/cyan]    - Show session info")
    console.print("  [cyan]/settings[/cyan]- Show current settings")
    console.print("  [cyan]/skills[/cyan]  - List available skills")
    console.print()


def _handle_slash_command(prompt: str, count: int, api_url: str) -> str:
    """Handle slash commands. Returns 'continue', 'exit', or None."""
    if prompt.lower() == "/clear":
        console.print("[dim]✓ Conversation context cleared[/dim]\n")
        return "continue"
    elif prompt.lower() == "/info":
        console.print(f"\n[bold]Session Info:[/bold]")
        console.print(f"  Queries: [cyan]{count}[/cyan]")
        console.print(f"  API URL: [cyan]{api_url}[/cyan]")
        console.print(f"  Config: [cyan]{settings._user_config_file}[/cyan]\n")
        return "continue"
    elif prompt.lower() == "/settings":
        console.print(f"\n[bold]Current Settings:[/bold]")
        console.print(f"  Theme: [cyan]{settings.cli.theme}[/cyan]")
        console.print(f"  Prompt: [cyan]{settings.cli.prompt_style}[/cyan]")
        console.print(f"  Format: [cyan]{settings.output.format}[/cyan]")
        console.print(f"  Stream: [cyan]{settings.output.stream}[/cyan]\n")
        return "continue"
    elif prompt.lower() == "/skills":
        console.print(f"\n[bold]Available Skills:[/bold]")
        for skill in skill_registry.list(include_hidden=False):
            enabled = "✓" if skill.name in settings.skills.enabled else " "
            console.print(f"  [{enabled}] [cyan]{skill.name}[/cyan] - {skill.description}")
        console.print()
        return "continue"
    else:
        console.print(f"[yellow]Unknown command: {prompt}[/yellow]")
        console.print("Type [cyan]help[/cyan] for available commands\n")
        return "continue"


def _render_response(text: str) -> None:
    """Render AI response."""
    # Check if it looks like markdown
    if any(marker in text for marker in ["```", "**", "*", "#", "- "]):
        try:
            md = Markdown(text)
            console.print(md)
        except Exception:
            console.print(Panel(text, border_style="green", padding=(0, 1)))
    else:
        console.print(Panel(text, border_style="green", padding=(0, 1)))


if __name__ == "__main__":
    app()
