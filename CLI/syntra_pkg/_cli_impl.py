#!/usr/bin/env python3
"""
Syntra CLI Implementation.

This module contains the actual CLI implementation.
It's separated to allow clean package imports.
"""

import sys
from pathlib import Path
import httpx
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

# Create console
console = Console()

# API Configuration
API_BASE_URL = "http://localhost:8000"

# Create Typer app
app = typer.Typer(
    name="syntra",
    help="🚀 Syntra - Goalixa AI DevOps Teammate",
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
    try:
        with console.status("[primary]Asking Syntra AI...[/primary]"):
            client = httpx.Client(base_url=server, timeout=30.0)
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
    server: str = typer.Option(API_BASE_URL, "--server", "-s", help="Syntra API server URL"),
):
    """
    Start interactive mode.

    Example:
        syntra interactive
    """
    from rich.prompt import Prompt
    from rich.markdown import Markdown

    console.print()
    console.print("🤖 [bold cyan]Syntra - Goalixa AI Teammate[/bold cyan]")
    console.print(f"ℹ Connected to: [cyan]{server}[/cyan]")
    console.print("💡 Type [yellow]help[/yellow] for commands or [yellow]exit[/yellow] to quit\n")

    session_queries = 0
    client = httpx.Client(base_url=server, timeout=30.0)

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
    server: str = typer.Option(API_BASE_URL, "--server", "-s", help="Syntra API server URL"),
):
    """Check Syntra API health."""
    try:
        with console.status("[primary]Checking health...[/primary]"):
            client = httpx.Client(base_url=server, timeout=30.0)
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

    info_table.add_row("CLI Name", "syntra")
    info_table.add_row("Version", "0.1.0")
    info_table.add_row("API Server", API_BASE_URL)
    info_table.add_row("Python Version", "3.11+")

    console.print()
    console.print(info_table)
    console.print()


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
        from syntra_pkg import __version__
        rprint(f"[primary]syntra[/primary] version [bold]{__version__}[/bold]")
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
    """Syntra - Goalixa AI DevOps Teammate."""
    pass


if __name__ == "__main__":
    app()
