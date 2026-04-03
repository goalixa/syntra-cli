#!/usr/bin/env python3
"""
Syntra CLI Implementation.

This module contains the actual CLI implementation.
It's separated to allow clean package imports.
"""

import sys
import os
from pathlib import Path
import httpx
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich import print as rprint

# Add project root to path for config module
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from config import config as cfg, DEFAULT_API_BASE_URL, CLI_NAME, CLI_VERSION, USER_CONFIG_FILE

# Create console
console = Console()

# Create Typer app
app = typer.Typer(
    name=CLI_NAME,
    help="🚀 Syntra - Goalixa AI DevOps Teammate",
    no_args_is_help=False,
    add_completion=False,
    invoke_without_command=True,
)


@app.command()
def ask(
    prompt: str = typer.Argument(..., help="Your prompt for Syntra AI"),
    server: Optional[str] = typer.Option(None, "--server", "-s", help="Syntra API server URL (overrides config)"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
):
    """
    Ask Syntra AI to perform a task.

    Example:
        syntra-cli ask "list all pods in production namespace"
    """
    # Use server from config if not provided
    api_url = server or cfg.api_base_url

    try:
        with console.status("[primary]Asking Syntra AI...[/primary]"):
            client = httpx.Client(base_url=api_url, timeout=30.0)
            response = client.post("/api/ask", json={"prompt": prompt})
            response.raise_for_status()
            result = response.json()
            client.close()

        if json_output:
            import json
            rprint(result)
        else:
            console.print()
            console.print(Panel(result.get("result", "No response"), title="✨ Syntra AI Response", border_style="green"))
            console.print()
            console.print("✓ Task completed!", style="green")

    except httpx.HTTPError as e:
        console.print(f"✗ API Error: {e}", style="red")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n⚠ Operation cancelled by user", style="yellow")
        raise typer.Exit(130)


@app.command()
def interactive(
    server: Optional[str] = typer.Option(None, "--server", "-s", help="Syntra API server URL (overrides config)"),
):
    """
    Start interactive mode.

    Example:
        syntra-cli interactive
    """

    # Use server from config if not provided
    api_url = server or cfg.api_base_url

    console.print()
    console.print("🤖 [bold cyan]Syntra - Goalixa AI Teammate[/bold cyan]")
    console.print(f"ℹ Connected to: [cyan]{api_url}[/cyan]")
    console.print("💡 Type [yellow]help[/yellow] for commands or [yellow]exit[/yellow] to quit\n")

    session_queries = 0
    client = httpx.Client(base_url=api_url, timeout=30.0)

    try:
        while True:
            try:
                prompt = Prompt.ask(f"[bold cyan]syntra[/bold cyan] [dim]({session_queries})[/dim]")
                prompt = prompt.strip()

                if not prompt:
                    continue

                if prompt.lower() in ["exit", "quit", "q"]:
                    console.print("\n👋 Goodbye! [dim](Session ended)[/dim]\n")
                    break

                if prompt.lower() == "clear":
                    console.clear()
                    continue

                if prompt.lower() == "help":
                    console.print("\n[bold]Available Commands:[/bold]")
                    console.print("  [cyan]help[/cyan]   - Show this help message")
                    console.print("  [cyan]clear[/cyan]  - Clear the screen")
                    console.print("  [cyan]exit[/cyan]   - Exit interactive mode\n")
                    continue

                session_queries += 1

                with console.status("[primary]Thinking...[/primary]"):
                    response = client.post("/api/ask", json={"prompt": prompt})
                    response.raise_for_status()
                    result = response.json()

                result_text = result.get("result", "No response")

                if any(marker in result_text for marker in ["```", "**", "*", "#", "- "]):
                    try:
                        md = Markdown(result_text)
                        console.print(md)
                    except:
                        console.print(Panel(result_text, border_style="green", padding=(0, 1)))
                else:
                    console.print(Panel(result_text, border_style="green", padding=(0, 1)))

            except httpx.HTTPError as e:
                console.print(f"[red]✗ Error: {e}[/red]\n")

    except KeyboardInterrupt:
        console.print("\n⚠ Exiting interactive mode...", style="yellow")

    finally:
        client.close()
        if session_queries > 0:
            console.print(f"[dim]Session summary: {session_queries} queries[/dim]\n")


@app.command()
def health(
    server: Optional[str] = typer.Option(None, "--server", "-s", help="Syntra API server URL (overrides config)"),
):
    """Check Syntra API health."""
    # Use server from config if not provided
    api_url = server or cfg.api_base_url

    try:
        with console.status("[primary]Checking health...[/primary]"):
            client = httpx.Client(base_url=api_url, timeout=30.0)
            response = client.get("/")
            response.raise_for_status()
            result = response.json()
            client.close()

        table = Table(title="Syntra Health Status", show_header=True)
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Details", style="dim")

        for key, value in result.items():
            table.add_row(key, "✓ Healthy", str(value))

        console.print()
        console.print(table)
        console.print()
        console.print("✓ All systems operational!", style="green")

    except httpx.HTTPError as e:
        console.print(f"✗ Health check failed: {e}", style="red")
        raise typer.Exit(1)


@app.command()
def info():
    """Show Syntra CLI information."""
    info_table = Table(title="Syntra CLI Information", show_header=True)
    info_table.add_column("Property", style="cyan")
    info_table.add_column("Value", style="green")

    info_table.add_row("CLI Name", CLI_NAME)
    info_table.add_row("Version", CLI_VERSION)
    info_table.add_row("API Server", cfg.api_base_url)
    info_table.add_row("Config File", str(USER_CONFIG_FILE))
    info_table.add_row("Python Version", "3.11+")

    console.print()
    console.print(info_table)
    console.print()


@app.command()
def config(
    key: Optional[str] = typer.Argument(None, help="Configuration key to set/view"),
    value: Optional[str] = typer.Argument(None, help="Configuration value to set"),
    unset: bool = typer.Option(False, "--unset", "-u", help="Unset (remove) a configuration value"),
    list_all: bool = typer.Option(False, "--list", "-l", help="List all configuration values"),
):
    """
    Manage Syntra CLI configuration.

    Configuration is stored in ~/.syntra/cfg.json

    Examples:
        syntra-cli config                    # List all config
        syntra-cli config api_base_url       # Get a value
        syntra-cli config api_base_url http://localhost:9000  # Set a value
        syntra-cli config api_base_url --unset  # Remove a value
    """
    if list_all or (key is None and value is None):
        # List all configuration
        all_config = cfg.get_all()

        if not all_config:
            console.print("[dim]No custom configuration set.[/dim]")
            console.print(f"\n[cyan]Default API URL:[/cyan] {DEFAULT_API_BASE_URL}")
            console.print(f"[cyan]Config file:[/cyan] {USER_CONFIG_FILE}")
            return

        table = Table(title="Syntra Configuration", show_header=True)
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="green")

        for k, v in all_config.items():
            table.add_row(k, str(v))

        console.print()
        console.print(table)
        console.print()
        return

    if unset:
        # Unset a configuration value
        cfg.unset(key)
        console.print(f"✓ Unset [cyan]{key}[/cyan]", style="green")
        return

    if value is None:
        # Get a single configuration value
        val = cfg.get(key)
        if val is None:
            console.print(f"[dim]Configuration key '[cyan]{key}[/cyan]' not set.[/dim]")
            console.print(f"Use: [cyan]{CLI_NAME} config {key} <value>[/cyan] to set it.")
        else:
            console.print(f"[cyan]{key}[/cyan] = [green]{val}[/green]")
    else:
        # Set a configuration value
        cfg.set(key, value)
        console.print(f"✓ Set [cyan]{key}[/cyan] = [green]{value}[/green]", style="green")


@app.command()
def agents():
    """List available agents."""
    agents_table = Table(title="Available Agents", show_header=True)
    agents_table.add_column("Agent", style="cyan")
    agents_table.add_column("Description", style="white")
    agents_table.add_column("Status", style="yellow")

    agents_data = [
        ("PlannerAgent", "Plans tasks based on prompts", "⚠️ Stub"),
        ("DevOpsAgent", "Executes DevOps operations", "⚠️ Stub"),
        ("ReviewerAgent", "Reviews and validates results", "⚠️ Stub"),
    ]

    for agent, desc, status in agents_data:
        agents_table.add_row(agent, desc, status)

    console.print()
    console.print(agents_table)
    console.print()
    console.print("⚠ Note: All agents are currently in stub implementation", style="yellow")


@app.command()
def tools():
    """List available tools."""
    tools_table = Table(title="Available Tools", show_header=True)
    tools_table.add_column("Tool", style="cyan")
    tools_table.add_column("Description", style="white")
    tools_table.add_column("Status", style="green")

    tools_data = [
        ("Kubernetes", "Pod listing and management", "✓ Basic"),
        ("Git", "Repository operations", "❌ Not Implemented"),
        ("Logs", "Log analysis", "❌ Not Implemented"),
    ]

    for tool, desc, status in tools_data:
        tools_table.add_row(tool, desc, status)

    console.print()
    console.print(tools_table)
    console.print()


def version_callback(value: bool) -> None:
    """Show version and exit."""
    if value:
        rprint(f"[primary]{CLI_NAME}[/primary] version [bold]{CLI_VERSION}[/bold]")
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
):
    """
    Syntra - Goalixa AI DevOps Teammate.

    Running without arguments starts interactive mode.
    """
    # If no subcommand was provided, start interactive mode
    if ctx.invoked_subcommand is None:
        api_url = cfg.api_base_url

        console.print()
        console.print("🤖 [bold cyan]Syntra - Goalixa AI Teammate[/bold cyan]")
        console.print(f"ℹ Connected to: [cyan]{api_url}[/cyan]")
        console.print("💡 Type [yellow]help[/yellow] for commands or [yellow]exit[/yellow] to quit\n")

        session_queries = 0
        client = httpx.Client(base_url=api_url, timeout=30.0)

        try:
            while True:
                try:
                    prompt = Prompt.ask(f"[bold cyan]syntra[/bold cyan] [dim]({session_queries})[/dim]")
                    prompt = prompt.strip()

                    if not prompt:
                        continue

                    if prompt.lower() in ["exit", "quit", "q"]:
                        console.print("\n👋 Goodbye! [dim](Session ended)[/dim]\n")
                        break

                    if prompt.lower() == "clear":
                        console.clear()
                        continue

                    if prompt.lower() == "help":
                        console.print("\n[bold]Available Commands:[/bold]")
                        console.print("  [cyan]help[/cyan]   - Show this help message")
                        console.print("  [cyan]clear[/cyan]  - Clear the screen")
                        console.print("  [cyan]exit[/cyan]   - Exit interactive mode")
                        console.print("  [cyan]/clear[/cyan] - Clear conversation context")
                        console.print("  [cyan]/info[/cyan]  - Show session info\n")
                        continue

                    # Special slash commands
                    if prompt.startswith("/"):
                        if prompt.lower() == "/clear":
                            session_queries = 0
                            console.print("[dim]✓ Conversation context cleared[/dim]\n")
                            continue
                        elif prompt.lower() == "/info":
                            console.print(f"\n[bold]Session Info:[/bold]")
                            console.print(f"  Queries: [cyan]{session_queries}[/cyan]")
                            console.print(f"  API URL: [cyan]{api_url}[/cyan]")
                            console.print(f"  Config: [cyan]{USER_CONFIG_FILE}[/cyan]\n")
                            continue
                        else:
                            console.print(f"[yellow]Unknown command: {prompt}[/yellow]")
                            console.print("Type [cyan]help[/cyan] for available commands\n")
                            continue

                    session_queries += 1

                    with console.status("[primary]Thinking...[/primary]"):
                        response = client.post("/api/ask", json={"prompt": prompt})
                        response.raise_for_status()
                        result = response.json()

                    result_text = result.get("result", "No response")

                    if any(marker in result_text for marker in ["```", "**", "*", "#", "- "]):
                        try:
                            md = Markdown(result_text)
                            console.print(md)
                        except:
                            console.print(Panel(result_text, border_style="green", padding=(0, 1)))
                    else:
                        console.print(Panel(result_text, border_style="green", padding=(0, 1)))

                except httpx.HTTPError as e:
                    console.print(f"[red]✗ Error: {e}[/red]\n")

        except KeyboardInterrupt:
            console.print("\n⚠ Exiting interactive mode...", style="yellow")

        finally:
            client.close()
            if session_queries > 0:
                console.print(f"[dim]Session summary: {session_queries} queries[/dim]\n")

        raise typer.Exit(0)


if __name__ == "__main__":
    app()
