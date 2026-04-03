"""Settings management skill."""

import json
import os
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from rich import print as rprint

from syntra_pkg.skills.base import Skill
from syntra_pkg.config import settings

console = Console()


class SettingsSkill(Skill):
    """Skill for managing Syntra CLI settings."""

    name = "settings"
    version = "1.0.0"
    description = "Manage CLI configuration and settings"
    category = "core"

    def register(self, app: typer.Typer) -> None:
        @app.command(name="settings")
        def settings_cmd(
            key: Optional[str] = typer.Argument(
                None,
                help="Configuration key to view or set (e.g., 'api.base_url')"
            ),
            value: Optional[str] = typer.Argument(
                None,
                help="Configuration value to set"
            ),
            unset: bool = typer.Option(
                False,
                "--unset",
                "-u",
                help="Unset (remove) a configuration value"
            ),
            edit: bool = typer.Option(
                False,
                "--edit",
                "-e",
                help="Open configuration in editor"
            ),
            list_all: bool = typer.Option(
                False,
                "--all",
                "-a",
                help="List all configuration including defaults"
            ),
            export: bool = typer.Option(
                False,
                "--export",
                help="Export configuration as JSON"
            ),
            validate: bool = typer.Option(
                False,
                "--validate",
                help="Validate configuration"
            ),
            reset: bool = typer.Option(
                False,
                "--reset",
                help="Reset configuration to defaults"
            ),
        ):
            """
            Manage Syntra CLI configuration.

            Configuration hierarchy (highest to lowest priority):
            1. Environment variables (SYNTRA_* prefix)
            2. User config (~/.syntra/config.json)
            3. Project config (.syntra/config.local.json)
            4. Built-in defaults

            Examples:
                syntra settings                           # Show user config
                syntra settings api.base_url              # Get a value
                syntra settings api.base_url https://...  # Set a value
                syntra settings api.base_url --unset      # Remove a value
                syntra settings --all                     # Show all config
                syntra settings --edit                    # Open in editor
            """
            if validate:
                _validate_cmd()
                return

            if reset:
                _reset_cmd(key)
                return

            if export:
                _export_cmd()
                return

            if edit:
                _edit_cmd()
                return

            if key is None:
                # List all configuration
                _list_cmd(list_all)
                return

            if unset:
                # Unset a configuration value
                settings.unset(key)
                console.print(f"✓ Unset [cyan]{key}[/cyan]", style="green")
                return

            if value is None:
                # Get a single configuration value
                val = settings.get(key)
                if val is None:
                    console.print(
                        f"[dim]Configuration key '[cyan]{key}[/cyan]' not set.[/dim]"
                    )
                    console.print(
                        f"Use: [cyan]syntra settings {key} <value>[/cyan] to set it."
                    )
                else:
                    rprint(f"[cyan]{key}[/cyan] = [green]{val}[/green]")
            else:
                # Set a configuration value
                settings.set(key, value)
                console.print(
                    f"✓ Set [cyan]{key}[/cyan] = [green]{value}[/green]",
                    style="green"
                )


# Helper functions (module-level for closure access)

def _list_cmd(include_defaults: bool) -> None:
    """List all configuration values."""
    all_config = settings.get_all(include_defaults=include_defaults)

    if not all_config:
        console.print("[dim]No custom configuration set.[/dim]")
        console.print(
            f"\n[cyan]Default API URL:[/cyan] {settings.api.base_url}"
        )
        console.print(
            f"[cyan]Config file:[/cyan] {settings._user_config_file}"
        )
        return

    table = Table(title="Syntra Configuration", show_header=True)
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Source", style="dim")

    # Determine source for each key
    for k, v in all_config.items():
        # Check where the value comes from
        env_key = f"SYNTRA_{k.replace('.', '_').upper()}"
        source = "default"  # default
        if env_key in os.environ:
            source = "env"
        elif settings._get_nested(settings._user_config, k):
            source = "user"
        elif settings._get_nested(settings._project_config, k):
            source = "project"

        # Format value for display
        if isinstance(v, (list, dict)):
            value_str = json.dumps(v, ensure_ascii=False)
            if len(value_str) > 50:
                value_str = value_str[:47] + "..."
        else:
            value_str = str(v)

        table.add_row(k, value_str, source)

    console.print()
    console.print(table)
    console.print()


def _validate_cmd() -> None:
    """Validate configuration."""
    is_valid, errors = settings.validate()

    if is_valid:
        console.print("✓ Configuration is valid", style="green")
    else:
        console.print("✗ Configuration errors:", style="red")
        for error in errors:
            console.print(f"  • {error}", style="red")
        raise typer.Exit(1)


def _export_cmd() -> None:
    """Export configuration as JSON."""
    config_json = settings.export()
    console.print(config_json)


def _edit_cmd() -> None:
    """Open configuration in editor."""
    import subprocess
    import tempfile

    # Get current config
    current_config = settings.get_all(include_defaults=True)

    # Create temp file with current config
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        delete=False,
    ) as f:
        json.dump(current_config, f, indent=2)
        temp_path = f.name

    try:
        # Open in editor
        editor = settings.cli.editor or os.getenv("EDITOR", "vim")
        console.print(f"Opening [cyan]{editor}[/cyan]...")

        subprocess.call([editor, temp_path])

        # Ask if user wants to save changes
        if Confirm.ask("Apply changes from editor?"):
            with open(temp_path, "r") as f:
                new_config = json.load(f)

            settings.import_config(json.dumps(new_config), merge=False)
            console.print("✓ Configuration applied", style="green")
        else:
            console.print("Changes discarded", style="dim")

    finally:
        # Clean up temp file
        Path(temp_path).unlink(missing_ok=True)


def _reset_cmd(key: Optional[str]) -> None:
    """Reset configuration to defaults."""
    if key is None:
        # Reset all
        if Confirm.ask(
            "This will reset all settings to defaults. Continue?",
            default=False,
        ):
            settings.reset()
            console.print("✓ All settings reset to defaults", style="green")
    else:
        # Reset specific key
        settings.reset(key)
        console.print(f"✓ Reset [cyan]{key}[/cyan] to default", style="green")


# Export skill instance
skill = SettingsSkill()
