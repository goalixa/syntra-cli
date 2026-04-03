"""Health skill - check API health."""

import httpx
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from syntra_pkg.skills.base import Skill
from syntra_pkg.config import settings

console = Console()


class HealthSkill(Skill):
    """Skill for checking Syntra API health."""

    name = "health"
    version = "1.0.0"
    description = "Check Syntra API health status"
    category = "core"

    def register(self, app: typer.Typer) -> None:
        @app.command()
        def health(
            server: Optional[str] = typer.Option(
                None,
                "--server",
                "-s",
                help="Syntra API server URL (overrides config)"
            ),
            verbose: bool = typer.Option(
                False,
                "-v",
                "--verbose",
                help="Show detailed health information"
            ),
        ):
            """
            Check Syntra API health status.

            Example:
                syntra health
                syntra health --server https://api.syntra.dev
            """
            # Use server from config if not provided
            api_url = server or settings.api.base_url

            try:
                with console.status("[primary]Checking health...[/primary]"):
                    client = httpx.Client(
                        base_url=api_url,
                        timeout=settings.api.timeout,
                    )
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

                if verbose:
                    console.print(f"\n[dim]Connected to: {api_url}[/dim]")
                    console.print(f"[dim]Response time: {result.get('response_time', 'N/A')}[/dim]")

            except httpx.ConnectError:
                console.print(f"✗ Cannot connect to {api_url}", style="red")
                console.print(
                    "\n[cyan]Tips:[/cyan]\n"
                    "  • Check if the API server is running\n"
                    "  • Verify the URL in: syntra settings api.base_url\n"
                    "  • Use --server to specify a different URL"
                )
                raise typer.Exit(1)
            except httpx.HTTPError as e:
                console.print(f"✗ Health check failed: {e}", style="red")
                raise typer.Exit(1)


# Export skill instance
skill = HealthSkill()
