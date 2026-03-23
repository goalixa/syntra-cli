#!/usr/bin/env python3
"""
Syntra CLI - Entry point script.

Usage:
    python syntra_cli.py --help
    python syntra_cli.py ask "list pods in production"
    python syntra_cli.py interactive
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import asyncio
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

# Import console and config
console = Console()

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Create Typer app
app = typer.Typer(
    name="syntra",
    help="🚀 Syntra AI - Intelligent DevOps Orchestrator",
    no_args_is_help=True,
    add_completion=False,
)


@app.command()
def ask(
    prompt: str = typer.Argument(..., help="Your prompt for Syntra AI"),
    server: str = typer.Option(API_BASE_URL, "--server", "-s", help="Syntra API server URL"),
    json_output: bool = typer.Option(False, "--json", "-j", help="Output as JSON"),
):
    """
    Ask Syntra AI to perform a task.

    Example:
        syntra ask "list all pods in production namespace"
    """
    import httpx

    try:
        with console.status("[primary]Asking Syntra AI...[/primary]"):
            response = httpx.post(
                f"{server}/api/ask",
                json={"prompt": prompt},
                timeout=30.0,
            )
            response.raise_for_status()
            result = response.json()

        if json_output:
            import json
            rprint_json(result)
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
    server: str = typer.Option(API_BASE_URL, "--server", "-s", help="Syntra API server URL"),
):
    """
    Start interactive mode.

    Example:
        syntra interactive
    """
    import httpx
    from rich.prompt import Prompt
    from rich.markdown import Markdown
    from rich.syntax import Syntax
    import datetime

    console.print()
    console.print("🤖 [bold cyan]Syntra - Goalixa AI Teammate[/bold cyan]")
    console.print(f"ℹ Connected to: [cyan]{server}[/cyan]")
    console.print("💡 Type [yellow]help[/yellow] for commands or [yellow]exit[/yellow] to quit\n")

    # Session stats
    session_start = datetime.datetime.now()
    query_count = 0

    # Create a persistent HTTP client
    client = httpx.Client(base_url=server, timeout=30.0)

    try:
        while True:
            try:
                # Show prompt with query count
                prompt = Prompt.ask(
                    f"[bold cyan]syntra[/bold cyan] [dim]({query_count})[/dim]"
                )

                # Trim and check for empty input
                prompt = prompt.strip()

                if not prompt:
                    continue

                # Handle special commands
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
                    console.print("  [cyan]quit[/cyan]   - Exit interactive mode")
                    console.print("  [cyan]q[/cyan]      - Exit interactive mode\n")
                    continue

                if prompt.lower() == "stats":
                    duration = datetime.datetime.now() - session_start
                    console.print(f"\n[bold]Session Statistics:[/bold]")
                    console.print(f"  Queries: [cyan]{query_count}[/cyan]")
                    console.print(f"  Duration: [cyan]{duration}[/cyan]")
                    console.print(f"  Server: [cyan]{server}[/cyan]\n")
                    continue

                # Increment query count
                query_count += 1

                # Show query with timestamp
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                console.print(f"\n[dim][{timestamp}] Query:[/dim] [white]{prompt}[/white]\n")

                # Execute the query with spinner
                with console.status("[primary]Thinking...[/primary]"):
                    try:
                        response = client.post("/api/ask", json={"prompt": prompt})
                        response.raise_for_status()
                        result = response.json()

                        # Display result
                        result_text = result.get("result", "No response")

                        # Try to render as markdown if it looks like markdown
                        if any(marker in result_text for marker in ["```", "**", "*", "#", "- "]):
                            try:
                                md = Markdown(result_text)
                                console.print(md)
                            except:
                                console.print(Panel(result_text, border_style="green", padding=(0, 1)))
                        else:
                            console.print(Panel(result_text, border_style="green", padding=(0, 1)))

                        console.print()  # Add spacing

                    except httpx.HTTPError as e:
                        console.print(f"[red]✗ Error: {e}[/red]\n")

                    except Exception as e:
                        console.print(f"[red]✗ Unexpected error: {e}[/red]\n")

            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                console.print("\n\n[yellow]⚠ Press Ctrl+C again or type 'exit' to quit[/yellow]")
                try:
                    # Wait for second Ctrl+C or continue
                    prompt = Prompt.ask("[bold cyan]syntra[/bold cyan]", default="")
                    if not prompt:
                        continue
                except KeyboardInterrupt:
                    console.print("\n\n👋 Goodbye! [dim](Session ended)[/dim]\n")
                    break

    finally:
        # Clean up HTTP client
        client.close()

        # Show session summary
        if query_count > 0:
            duration = datetime.datetime.now() - session_start
            console.print(f"[dim]Session summary: {query_count} queries in {duration}[/dim]\n")



@app.command()
def health(
    server: str = typer.Option(API_BASE_URL, "--server", "-s", help="Syntra API server URL"),
):
    """
    Check Syntra API health.

    Example:
        syntra health
    """
    import httpx

    try:
        with console.status("[primary]Checking health...[/primary]"):
            response = httpx.get(f"{server}/", timeout=30.0)
            response.raise_for_status()
            result = response.json()

        # Create health table
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
    """
    Show Syntra CLI information.

    Example:
        syntra info
    """
    info_table = Table(title="Syntra CLI Information", show_header=True)
    info_table.add_column("Property", style="cyan")
    info_table.add_column("Value", style="green")

    info_table.add_row("CLI Name", "syntra")
    info_table.add_row("Version", "0.1.0")
    info_table.add_row("API Server", API_BASE_URL)
    info_table.add_row("Python Version", "3.11+")

    console.print()
    console.print(info_table)
    console.print()


@app.command()
def agents():
    """
    List available agents.

    Example:
        syntra agents
    """
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
    """
    List available tools.

    Example:
        syntra tools
    """
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
        rprint("[primary]syntra[/primary] version [bold]0.1.0[/bold]")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
):
    """Syntra CLI - Intelligent DevOps Orchestrator."""
    pass


if __name__ == "__main__":
    app()
