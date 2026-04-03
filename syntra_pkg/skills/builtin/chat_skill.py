"""Chat skill - interactive REPL."""

import httpx
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

from syntra_pkg.skills.base import Skill
from syntra_pkg.config import settings

console = Console()


class ChatSkill(Skill):
    """Skill for interactive chat mode."""

    name = "chat"
    version = "1.0.0"
    description = "Start interactive chat mode with Syntra AI"
    category = "core"

    def register(self, app: typer.Typer) -> None:
        @app.command()
        def chat(
            server: Optional[str] = typer.Option(
                None,
                "--server",
                "-s",
                help="Syntra API server URL (overrides config)"
            ),
        ):
            """
            Start interactive chat mode.

            Example:
                syntra chat
            """
            # Use server from config if not provided
            api_url = server or settings.api.base_url

            # Display welcome message
            self._print_welcome(api_url)

            session_queries = 0
            client = httpx.Client(
                base_url=api_url,
                timeout=settings.api.timeout,
            )

            try:
                while True:
                    try:
                        prompt = Prompt.ask(
                            f"[bold cyan]syntra[/bold cyan] [dim]({session_queries})[/dim]"
                        )
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
                            self._print_help()
                            continue

                        # Handle slash commands
                        if prompt.startswith("/"):
                            handled = self._handle_slash_command(prompt, session_queries, api_url)
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
                        self._render_response(result_text)

                    except httpx.HTTPError as e:
                        console.print(f"[red]✗ Error: {e}[/red]\n")

            except KeyboardInterrupt:
                console.print("\n⚠ Exiting chat mode...", style="yellow")

            finally:
                client.close()
                if session_queries > 0:
                    console.print(f"[dim]Session summary: {session_queries} queries[/dim]\n")

    def _print_welcome(self, api_url: str) -> None:
        """Print welcome message."""
        console.print()
        console.print("🤖 [bold cyan]Syntra - Goalixa AI Teammate[/bold cyan]")
        console.print(f"ℹ Connected to: [cyan]{api_url}[/cyan]")
        console.print("💡 Type [yellow]help[/yellow] for commands or [yellow]exit[/yellow] to quit\n")

    def _print_help(self) -> None:
        """Print help message."""
        console.print("\n[bold]Available Commands:[/bold]")
        console.print("  [cyan]help[/cyan]     - Show this help message")
        console.print("  [cyan]clear[/cyan]    - Clear the screen")
        console.print("  [cyan]exit[/cyan]     - Exit chat mode")
        console.print("  [cyan]/clear[/cyan]   - Clear conversation context")
        console.print("  [cyan]/info[/cyan]    - Show session info")
        console.print("  [cyan]/settings[/cyan]- Show current settings\n")

    def _handle_slash_command(self, prompt: str, count: int, api_url: str) -> str:
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
            console.print(f"  Format: [cyan]{settings.output.format}[/cyan]")
            console.print(f"  Stream: [cyan]{settings.output.stream}[/cyan]\n")
            return "continue"
        else:
            console.print(f"[yellow]Unknown command: {prompt}[/yellow]")
            console.print("Type [cyan]help[/cyan] for available commands\n")
            return "continue"

    def _render_response(self, text: str) -> None:
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


# Export skill instance
skill = ChatSkill()
