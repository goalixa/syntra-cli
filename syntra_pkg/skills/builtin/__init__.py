"""Built-in skills for Syntra CLI.

This package contains all the core skills that ship with syntra-cli.
"""

# Import all built-in skills so they can be discovered
from syntra_pkg.skills.builtin.settings_skill import skill as settings_skill
from syntra_pkg.skills.builtin.ask_skill import skill as ask_skill
from syntra_pkg.skills.builtin.chat_skill import skill as chat_skill
from syntra_pkg.skills.builtin.health_skill import skill as health_skill
from syntra_pkg.skills.builtin.agents_skill import skill as agents_skill
from syntra_pkg.skills.builtin.info_skill import skill as info_skill

__all__ = [
    "settings_skill",
    "ask_skill",
    "chat_skill",
    "health_skill",
    "agents_skill",
    "info_skill",
]
