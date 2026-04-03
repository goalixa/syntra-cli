"""Base skill class and interfaces."""

from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import typer


class Skill(ABC):
    """
    Base class for all Syntra CLI skills.

    A skill represents a set of related CLI commands. Skills can be
    built-in (shipped with syntra-cli) or user-installed.

    Example:
        class MySkill(Skill):
            name = "my-skill"
            version = "1.0.0"
            description = "My custom skill"

            def register(self, app: typer.Typer) -> None:
                @app.command()
                def my_command():
                    print("Hello from my skill!")
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique skill identifier.

        Must be lowercase, alphanumeric, with hyphens allowed.
        Used as: syntra <name> ...
        """
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Skill version following semantic versioning."""
        pass

    @property
    def description(self) -> str:
        """Human-readable description of what this skill does."""
        return ""

    @property
    def category(self) -> str:
        """
        Skill category for organization.

        Examples: "core", "devops", "development", "utility"
        """
        return "utility"

    @property
    def dependencies(self) -> List[str]:
        """
        List of skill names this skill depends on.

        These skills will be loaded before this skill.
        """
        return []

    @property
    def hidden(self) -> bool:
        """
        Whether this skill should be hidden from listings.

        Useful for internal skills or skills under development.
        """
        return False

    @abstractmethod
    def register(self, app: "typer.Typer") -> None:
        """
        Register this skill's commands with the Typer app.

        This is where you define your skill's CLI commands.

        Args:
            app: The Typer application instance
        """
        pass

    def initialize(self, context: "SkillContext") -> None:
        """
        Called when the skill is loaded.

        Use this for setup operations like validating dependencies
        or initializing resources.

        Args:
            context: Skill initialization context
        """
        pass

    def shutdown(self) -> None:
        """Called when the CLI is shutting down."""
        pass

    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate that the skill can be loaded.

        Override this to check for required dependencies, files, etc.

        Returns:
            Tuple of (is_valid, error_message)
        """
        return True, None


class SkillContext:
    """
    Context provided to skills during initialization.

    Contains information about the CLI environment and configuration.
    """

    def __init__(
        self,
        settings,
        config_dir,
        project_dir,
        debug_mode: bool = False,
    ):
        self.settings = settings
        self.config_dir = config_dir
        self.project_dir = project_dir
        self.debug_mode = debug_mode
