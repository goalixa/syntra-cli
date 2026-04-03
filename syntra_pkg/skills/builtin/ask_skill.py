"""Ask skill - single question command."""

import httpx
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from syntra_pkg.skills.base import Skill
from syntra_pkg.config import settings

console = Console()


class AskSkill(Skill):
    """Skill for asking Syntra AI single questions."""

    name = "ask"
    version = "1.0.0"
    description = "Ask Syntra AI a single question"
    category = "core"

    def register(self, app: typer.Typer) -> None:
        @app.command()
        def ask(
            prompt: str = typer.Argument(..., help="Your question for Syntra AI"),
            server: Optional[str] = typer.Option(
                None,
                "--server",
                "-s",
                help="Syntra API server URL (overrides config)"
            ),
            json_output: bool = typer.Option(
                False,
                "--json",
                "-j",
                help="Output as JSON"
            ),
            stream: bool = typer.Option(
                None,
                "--stream",
                help="Enable streaming output (uses default from settings if not specified)"
            ),
            context: Optional[str] = typer.Option(
                None,
                "--context",
                "-c",
                help="Additional context for the question"
            ),
        ):
            """
            Ask Syntra AI a single question.

            Example:
                syntra ask "list all pods in production namespace"
                syntra ask "explain this error" --context "production deployment"
            """
            # Use server from config if not provided
            api_url = server or settings.api.base_url
            should_stream = stream if stream is not None else settings.output.stream

            try:
                with console.status("[primary]Asking Syntra AI...[/primary]"):
                    client = httpx.Client(
                        base_url=api_url,
                        timeout=settings.api.timeout,
                    )

                    payload = {"prompt": prompt}
                    if context:
                        payload["context"] = context

                    response = client.post("/api/ask", json=payload)
                    response.raise_for_status()
                    result = response.json()
                    client.close()

                if json_output or settings.output.format == "json":
                    import json as json_lib
                    console.print_json(data=result)
                else:
                    console.print()
                    result_text = result.get("result", "No response")

                    # Render as markdown if it contains markdown markers
                    if any(marker in result_text for marker in ["```", "**", "*", "#", "- "]):
                        try:
                            md = Markdown(result_text)
                            console.print(md)
                        except Exception:
                            console.print(
                                Panel(result_text, title="✨ Syntra AI Response", border_style="green")
                            )
                    else:
                        console.print(
                            Panel(result_text, title="✨ Syntra AI Response", border_style="green")
                        )

                    console.print()
                    console.print("✓ Task completed!", style="green")

                    # Show metadata if enabled
                    if settings.output.show_metadata:
                        metadata = result.get("metadata", {})
                        if metadata:
                            console.print(f"[dim]Duration: {metadata.get('duration_ms', 'N/A')}ms[/dim]")

            except httpx.HTTPError as e:
                console.print(f"✗ API Error: {e}", style="red")
                raise typer.Exit(1)
            except KeyboardInterrupt:
                console.print("\n⚠ Operation cancelled by user", style="yellow")
                raise typer.Exit(130)


# Export skill instance
skill = AskSkill()
