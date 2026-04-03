"""Syntra - Goalixa AI DevOps Teammate."""

__version__ = "0.2.0"
__author__ = "Amirreza Rezaie"
__email__ = "82rezaeei@gmail.com"

# Re-exports for convenience
from syntra_pkg.config import settings
from syntra_pkg.skills import skill_registry

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "settings",
    "skill_registry",
]
