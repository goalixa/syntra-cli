"""Skill registry for managing available skills."""

from pathlib import Path
from typing import Dict, List, Optional, TYPE_CHECKING
import sys

if TYPE_CHECKING:
    import typer
    from syntra_pkg.skills.base import Skill

from syntra_pkg.config import settings


class SkillRegistry:
    """
    Registry for managing available skills.

    Handles skill discovery, loading, and dependency resolution.
    """

    def __init__(self):
        """Initialize the skill registry."""
        self._skills: Dict[str, "Skill"] = {}
        self._loaded = False

    @property
    def skills(self) -> Dict[str, "Skill"]:
        """Get all registered skills."""
        return self._skills.copy()

    def register(self, skill: "Skill") -> None:
        """
        Register a skill.

        Args:
            skill: The skill to register

        Raises:
            ValueError: If a skill with the same name is already registered
        """
        if skill.name in self._skills:
            raise ValueError(f"Skill '{skill.name}' is already registered")

        # Validate the skill
        is_valid, error = skill.validate()
        if not is_valid:
            raise ValueError(f"Skill '{skill.name}' validation failed: {error}")

        self._skills[skill.name] = skill

    def unregister(self, name: str) -> Optional["Skill"]:
        """
        Unregister a skill.

        Args:
            name: Name of the skill to unregister

        Returns:
            The unregistered skill, or None if not found
        """
        return self._skills.pop(name, None)

    def get(self, name: str) -> Optional["Skill"]:
        """Get a skill by name."""
        return self._skills.get(name)

    def list(
        self,
        include_hidden: bool = False,
        category: Optional[str] = None,
    ) -> List["Skill"]:
        """
        List registered skills.

        Args:
            include_hidden: Whether to include hidden skills
            category: Filter by category

        Returns:
            List of skills matching the criteria
        """
        skills = list(self._skills.values())

        if not include_hidden:
            skills = [s for s in skills if not s.hidden]

        if category:
            skills = [s for s in skills if s.category == category]

        return sorted(skills, key=lambda s: s.name)

    def get_load_order(self) -> List["Skill"]:
        """
        Get the order in which skills should be loaded.

        Resolves dependencies and returns skills in dependency order.

        Returns:
            List of skills in load order

        Raises:
            RuntimeError: If there are circular dependencies
        """
        loaded = set()
        order = []

        def load_skill(skill: "Skill") -> None:
            if skill.name in loaded:
                return

            # Check for circular dependency
            if skill.name in order:
                raise RuntimeError(f"Circular dependency detected for skill '{skill.name}'")

            # Load dependencies first
            for dep_name in skill.dependencies:
                dep = self._skills.get(dep_name)
                if not dep:
                    raise RuntimeError(
                        f"Skill '{skill.name}' depends on '{dep_name}' "
                        f"which is not registered"
                    )
                load_skill(dep)

            loaded.add(skill.name)
            order.append(skill)

        # Load all skills
        for skill in self._skills.values():
            load_skill(skill)

        return order

    def initialize_all(self, context) -> None:
        """
        Initialize all registered skills in dependency order.

        Args:
            context: Skill initialization context
        """
        if self._loaded:
            return

        for skill in self.get_load_order():
            skill.initialize(context)

        self._loaded = True

    def shutdown_all(self) -> None:
        """Shutdown all registered skills."""
        for skill in self._skills.values():
            try:
                skill.shutdown()
            except Exception:
                pass  # Ignore errors during shutdown

        self._loaded = False

    def discover_builtin(self) -> None:
        """Discover and register built-in skills."""
        builtin_path = Path(__file__).parent / "builtin"

        if not builtin_path.exists():
            return

        # Add to path if not already there
        builtin_str = str(builtin_path.parent)
        if builtin_str not in sys.path:
            sys.path.insert(0, builtin_str)

        # Import and register skills
        for skill_file in builtin_path.glob("*.py"):
            if skill_file.name.startswith("_"):
                continue

            module_name = f"syntra_pkg.skills.builtin.{skill_file.stem}"

            try:
                # Import the module
                __import__(module_name)

                # Get the skill class (convention: <Name>Skill)
                # The module should export a `skill` instance
                module = sys.modules[module_name]
                if hasattr(module, "skill"):
                    self.register(module.skill)

            except Exception as e:
                # Log but don't fail - missing skills shouldn't break the CLI
                if settings.dev.debug:
                    print(f"Warning: Failed to load skill from {skill_file.name}: {e}")

    def discover_user_skills(self) -> None:
        """Discover and register user-installed skills."""
        skill_paths = settings.skills.paths

        for path_str in skill_paths:
            skill_path = Path(path_str).expanduser()

            if not skill_path.exists():
                continue

            # Import skills from the path
            for skill_file in skill_path.glob("*.py"):
                if skill_file.name.startswith("_"):
                    continue

                # Load user skill
                # TODO: Implement user skill loading with proper isolation


# Global skill registry instance
skill_registry = SkillRegistry()
