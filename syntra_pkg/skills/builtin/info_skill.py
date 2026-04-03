"""Info skill - show CLI information."""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from syntra_pkg.skills.base import Skill
from syntra_pkg.config import settings
import sys

console = Console()


class InfoSkill(Skill):
    """Skill for displaying CLI information."""

    name = "info"
    version = "1.0.0"
    description = "Show Syntra CLI information"
    category = "core"

    def register(self, app: typer.Typer) -> None:
        @app.command()
        def info(
            verbose: bool = typer.Option(
                False,
                "-v",
                "--verbose",
                help="Show detailed information"
            ),
        ):
            """
            Show Syntra CLI information.

            Examples:
                syntra info
                syntra info --verbose
            """
            from syntra_pkg import __version__

            info_table = Table(title="Syntra CLI Information", show_header=True)
            info_table.add_column("Property", style="cyan")
            info_table.add_column("Value", style="green")

            # Basic info
            info_table.add_row("CLI Name", "syntra-cli")
            info_table.add_row("Version", __version__)
            info_table.add_row("Python Version", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
            info_table.add_row("API Server", settings.api.base_url)
            info_table.add_row("Config File", str(settings._user_config_file))

            console.print()
            console.print(info_table)

            if verbose:
                # Show paths
                console.print("\n[bold]Paths:[/bold]")
                console.print(f"  User config dir: [cyan]{settings._user_config_dir}[/cyan]")
                console.print(f"  User config: [cyan]{settings._user_config_file}[/cyan]")
                console.print(f"  Project config: [cyan]{settings._project_config_file}[/cyan]")
                console.print(f"  Skill paths: [cyan]{', '.join(settings.skills.paths)}[/cyan]")

                # Show enabled skills
                from syntra_pkg.skills import skill_registry

                console.print("\n[bold]Enabled Skills:[/bold]")
                for skill_name in settings.skills.enabled:
                    skill = skill_registry.get(skill_name)
                    if skill:
                        status = "✓" if not skill.hidden else "👻"
                        console.print(f"  {status} [cyan]{skill.name}[/cyan] v{skill.version}")
                    else:
                        console.print(f"  ✗ [dim]{skill_name}[/dim] (not found)")

                # Show current settings
                console.print("\n[bold]Current Settings:[/bold]")
                console.print(f"  Theme: [cyan]{settings.cli.theme}[/cyan]")
                console.print(f"  Prompt style: [cyan]{settings.cli.prompt_style}[/cyan]")
                console.print(f"  Output format: [cyan]{settings.output.format}[/cyan]")
                console.print(f"  Streaming: [cyan]{settings.output.stream}[/cyan]")

            console.print()


# Export skill instance
skill = InfoSkill()
