"""Agents skill - list and manage agents."""

from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from syntra_pkg.skills.base import Skill
from syntra_pkg.config import settings

console = Console()


class AgentsSkill(Skill):
    """Skill for managing Syntra agents."""

    name = "agents"
    version = "1.0.0"
    description = "List and manage Syntra AI agents"
    category = "core"

    def register(self, app: typer.Typer) -> None:
        @app.command()
        def agents(
            list_all: bool = typer.Option(
                True,
                "--list",
                "-l",
                help="List available agents"
            ),
            info: Optional[str] = typer.Option(
                None,
                "--info",
                "-i",
                help="Show detailed information about an agent"
            ),
        ):
            """
            List and manage Syntra AI agents.

            Examples:
                syntra agents
                syntra agents --info PlannerAgent
            """
            if info:
                self._show_agent_info(info)
            else:
                self._list_agents()

        @app.command(name="agent")
        def agent_cmd(
            name: str = typer.Argument(..., help="Agent name"),
            action: Optional[str] = typer.Option(
                None,
                "--action",
                "-a",
                help="Action to perform (enable/disable/status)"
            ),
        ):
            """
            Manage a specific agent.

            Examples:
                syntra agent PlannerAgent --action status
            """
            console.print(f"\n[bold]Agent: {name}[/bold]")
            console.print(f"Action: {action or 'info'}")
            console.print("\n[dim]Note: Agent management is coming soon![/dim]\n")

    def _list_agents(self) -> None:
        """List all available agents."""
        agents_table = Table(title="Available Agents", show_header=True)
        agents_table.add_column("Agent", style="cyan")
        agents_table.add_column("Description", style="white")
        agents_table.add_column("Status", style="yellow")

        agents_data = [
            ("PlannerAgent", "Plans tasks based on prompts", "🚧 Stub"),
            ("DevOpsAgent", "Executes DevOps operations", "🚧 Stub"),
            ("ReviewerAgent", "Reviews and validates results", "🚧 Stub"),
            ("DebugAgent", "Debugs issues and errors", "🚧 Stub"),
            ("CodeAgent", "Generates and modifies code", "🚧 Stub"),
        ]

        for agent, desc, status in agents_data:
            agents_table.add_row(agent, desc, status)

        console.print()
        console.print(agents_table)
        console.print()
        console.print("⚠ [dim]Note: All agents are currently in stub implementation[/dim]")

    def _show_agent_info(self, agent_name: str) -> None:
        """Show detailed information about an agent."""
        # Agent information database
        agent_info = {
            "PlannerAgent": {
                "description": "Analyzes prompts and creates execution plans",
                "capabilities": ["Task breakdown", "Dependency analysis", "Resource estimation"],
                "status": "🚧 Stub",
            },
            "DevOpsAgent": {
                "description": "Handles DevOps operations and infrastructure tasks",
                "capabilities": ["Kubernetes operations", "CI/CD management", "Monitoring"],
                "status": "🚧 Stub",
            },
            "ReviewerAgent": {
                "description": "Reviews results and validates outputs",
                "capabilities": ["Code review", "Output validation", "Quality checks"],
                "status": "🚧 Stub",
            },
        }

        info = agent_info.get(agent_name)
        if not info:
            console.print(f"✗ Unknown agent: {agent_name}", style="red")
            console.print("Run [cyan]syntra agents[/cyan] to see available agents")
            raise typer.Exit(1)

        console.print(f"\n[bold cyan]{agent_name}[/bold cyan]")
        console.print(f"Status: {info['status']}")
        console.print(f"\n{info['description']}\n")

        console.print("[bold]Capabilities:[/bold]")
        for cap in info["capabilities"]:
            console.print(f"  • {cap}")

        console.print()


# Export skill instance
skill = AgentsSkill()
