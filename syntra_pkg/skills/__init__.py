"""Skill system for Syntra CLI.

The skill system allows extensible commands through a plugin architecture.
Skills can be built-in or installed by users.
"""

from syntra_pkg.skills.base import Skill, SkillContext
from syntra_pkg.skills.registry import SkillRegistry, skill_registry

__all__ = ["Skill", "SkillContext", "SkillRegistry", "skill_registry"]
