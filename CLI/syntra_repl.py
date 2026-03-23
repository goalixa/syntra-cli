#!/usr/bin/env python3
"""
Syntra CLI - Enhanced Interactive Mode with History

Like Claude Code or Codex CLI - persistent session with command history
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import httpx
import datetime
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich import print as rprint

console = Console()

# API Configuration
API_BASE_URL = "http://localhost:8000"


class SyntraREPL:
    """Enhanced REPL for Syntra CLI with history and better UX."""

    def __init__(self, server: str = API_BASE_URL):
        self.server = server
        self.client = httpx.Client(base_url=server, timeout=30.0)
        self.session_start = datetime.datetime.now()
        self.query_count = 0
        self.history: List[str] = []
        self.max_history = 100

    def get_prompt(self) -> str:
        """Generate the prompt string."""
        return f"\n🤖 [bold cyan]syntra[/bold cyan] [dim]({self.query_count})[/dim]"

    def show_welcome(self):
        """Show welcome message."""
        console.print()
        console.print(Panel(
            "[bold cyan]🤖 Syntra - Goalixa AI Teammate[/bold cyan]\n\n"
            f"[dim]Connected to:[/dim] [cyan]{self.server}[/cyan]\n"
            "[dim]Type:[/dim] [yellow]help[/yellow] [dim]for commands[/dim]\n"
            "[dim]Type:[/dim] [yellow]exit[/yellow] [dim]or[/dim] [yellow]Ctrl+C[/yellow] [dim]to quit[/dim]\n"
            "[dim]Use:[/dim] [yellow]↑/↓ arrows[/yellow] [dim]for command history[/dim]",
            border_style="cyan",
            padding=(1, 2)
        ))

    def show_help(self):
        """Show help message."""
        help_table = Table(title="[bold]Available Commands[/bold]", show_header=False)
        help_table.add_column("Command", style="cyan")
        help_table.add_column("Description", style="white")

        commands = [
            ("help", "Show this help message"),
            ("clear", "Clear the screen"),
            ("history", "Show command history"),
            ("stats", "Show session statistics"),
            ("server", "Show server information"),
            ("exit, quit, q", "Exit interactive mode"),
            ("Ctrl+C", "Exit (with confirmation)"),
        ]

        for cmd, desc in commands:
            help_table.add_row(cmd, desc)

        console.print()
        console.print(help_table)
        console.print()

    def show_history(self):
        """Show command history."""
        if not self.history:
            console.print("\n[dim]No commands in history yet.[/dim]\n")
            return

        console.print("\n[bold]Command History:[/bold]\n")
        for i, cmd in enumerate(self.history, 1):
            console.print(f"  [dim]{i:3d}.[/dim] {cmd}")
        console.print()

    def show_stats(self):
        """Show session statistics."""
        duration = datetime.datetime.now() - self.session_start

        stats_table = Table(title="[bold]Session Statistics[/bold]", show_header=False)
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")

        stats_table.add_row("Queries", str(self.query_count))
        stats_table.add_row("Duration", str(duration).split(".")[0])
        stats_table.add_row("Server", self.server)
        stats_table.add_row("History Size", f"{len(self.history)}/{self.max_history}")

        console.print()
        console.print(stats_table)
        console.print()

    def show_server_info(self):
        """Show server information."""
        try:
            response = self.client.get("/")
            response.raise_for_status()
            result = response.json()

            server_table = Table(title="[bold]Server Information[/bold]", show_header=False)
            server_table.add_column("Key", style="cyan")
            server_table.add_column("Value", style="green")

            for key, value in result.items():
                server_table.add_row(key, str(value))

            console.print()
            console.print(server_table)
            console.print()

        except Exception as e:
            console.print(f"\n[red]✗ Failed to get server info: {e}[/red]\n")

    def add_to_history(self, command: str):
        """Add command to history."""
        # Skip empty commands and duplicates
        if not command or command == self.history[-1] if self.history else False:
            return

        self.history.append(command)

        # Limit history size
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

    def execute_command(self, prompt: str):
        """Execute a command and display the result."""
        self.query_count += 1

        # Show timestamp
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        console.print(f"\n[dim][{timestamp}] Query:[/dim] [white]{prompt}[/white]")

        try:
            # Execute request with spinner
            with console.status("[primary]Thinking...[/primary]", spinner="dots"):
                response = self.client.post("/api/ask", json={"prompt": prompt})
                response.raise_for_status()
                result = response.json()

            # Display result
            result_text = result.get("result", "No response")

            # Try to render as markdown
            if any(marker in result_text for marker in ["```", "**", "*", "#", "- "]):
                try:
                    md = Markdown(result_text)
                    console.print("\n", md, "\n")
                except:
                    console.print(Panel(result_text, border_style="green", padding=(0, 1)))
            else:
                console.print(Panel(result_text, border_style="green", padding=(0, 1)))

        except httpx.HTTPError as e:
            console.print(f"\n[red]✗ API Error: {e}[/red]\n")

        except Exception as e:
            console.print(f"\n[red]✗ Unexpected error: {e}[/red]\n")

    def run(self):
        """Run the REPL loop."""
        self.show_welcome()

        try:
            while True:
                try:
                    # Get input
                    prompt = console.input(self.get_prompt()).strip()

                    # Skip empty input
                    if not prompt:
                        continue

                    # Handle special commands
                    prompt_lower = prompt.lower()

                    if prompt_lower in ["exit", "quit", "q"]:
                        console.print("\n👋 [yellow]Goodbye![/yellow] [dim](Session ended)[/dim]\n")
                        break

                    if prompt_lower == "clear":
                        console.clear()
                        continue

                    if prompt_lower == "help":
                        self.show_help()
                        continue

                    if prompt_lower == "history":
                        self.show_history()
                        continue

                    if prompt_lower == "stats":
                        self.show_stats()
                        continue

                    if prompt_lower == "server":
                        self.show_server_info()
                        continue

                    # Add to history
                    self.add_to_history(prompt)

                    # Execute command
                    self.execute_command(prompt)

                except KeyboardInterrupt:
                    # First Ctrl+C - show message
                    console.print("\n\n[yellow]⚠ Press Ctrl+C again to exit, or type 'exit'[/yellow]")
                    try:
                        # Wait for input or second Ctrl+C
                        prompt = console.input(self.get_prompt())
                        if prompt.strip():
                            if prompt.lower() in ["exit", "quit", "q"]:
                                console.print("\n👋 [yellow]Goodbye![/yellow] [dim](Session ended)[/dim]\n")
                                break
                            self.add_to_history(prompt)
                            self.execute_command(prompt)
                    except KeyboardInterrupt:
                        console.print("\n\n👋 [yellow]Goodbye![/yellow] [dim](Session ended)[/dim]\n")
                        break

        finally:
            # Clean up
            self.client.close()

            # Show session summary
            if self.query_count > 0:
                duration = datetime.datetime.now() - self.session_start
                console.print(Panel(
                    f"[bold]Session Summary[/bold]\n\n"
                    f"Queries: [cyan]{self.query_count}[/cyan]\n"
                    f"Duration: [cyan]{str(duration).split('.')[0]}[/cyan]\n"
                    f"History: [cyan]{len(self.history)}[/cyan] commands",
                    border_style="dim",
                ))


def main():
    """Main entry point."""
    import sys

    # Get server from command line if provided
    server = sys.argv[1] if len(sys.argv) > 1 else API_BASE_URL

    # Run REPL
    repl = SyntraREPL(server=server)
    repl.run()


if __name__ == "__main__":
    main()
