"""Syntra CLI - Main entry point."""

import asyncio
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich import print as rprint

from cli.console import console
from cli.config import CLI_NAME, CLI_VERSION, API_BASE_URL
from cli.api import SyntraAPI, SyntraAPIError
from cli.utils import (
    run_with_spinner,
    print_panel,
    print_header,
    print_success,
    print_error,
    print_warning,
    print_info,
)

# Create Typer app
app = typer.Typer(
    name=CLI_NAME,
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
    async def _ask():
        async with SyntraAPI(base_url=server) as api:
            result = await run_with_spinner(
                api.ask,
                f"[primary]Asking Syntra AI...[/primary]",
                prompt=prompt,
            )

            if json_output:
                import json
                rprint_json(result)
            else:
                print_header("✨ Syntra AI Response")
                print_panel(result.get("result", "No response"), border_style="success")
                print_success("Task completed!")

    try:
        asyncio.run(_ask())
    except SyntraAPIError as e:
        print_error(f"API Error: {e}")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        print_warning("\nOperation cancelled by user")
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

    async def _interactive():
        print_header("🤖 Syntra AI - Interactive Mode")
        print_info(f"Connected to: {server}")
        print_info("Press Ctrl+C to exit\n")

        async with SyntraAPI(base_url=server) as api:
            while True:
                try:
                    prompt = Prompt.ask("[primary]syntra[/primary]")

                    if not prompt.strip():
                        continue

                    result = await run_with_spinner(
                        api.ask,
                        "[primary]Thinking...[/primary]",
                        prompt=prompt,
                    )

                    print_panel(result.get("result", "No response"), border_style="success")

                except KeyboardInterrupt:
                    print_warning("\nExiting interactive mode...")
                    break
                except SyntraAPIError as e:
                    print_error(f"Error: {e}")

    try:
        asyncio.run(_interactive())
    except KeyboardInterrupt:
        print_warning("\nGoodbye!")
        raise typer.Exit(130)


@app.command()
def health(
    server: str = typer.Option(API_BASE_URL, "--server", "-s", help="Syntra API server URL"),
):
    """
    Check Syntra API health.

    Example:
        syntra health
    """
    async def _health():
        async with SyntraAPI(base_url=server) as api:
            result = await run_with_spinner(
                api.health,
                "[primary]Checking health...[/primary]",
            )

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
            print_success("All systems operational!")

    try:
        asyncio.run(_health())
    except SyntraAPIError as e:
        print_error(f"Health check failed: {e}")
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

    info_table.add_row("CLI Name", CLI_NAME)
    info_table.add_row("Version", CLI_VERSION)
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
    print_warning("Note: All agents are currently in stub implementation")


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
        rprint(f"[primary]{CLI_NAME}[/primary] version [bold]{CLI_VERSION}[/bold]")
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
