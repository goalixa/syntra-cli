#!/usr/bin/env python3
"""
Syntra CLI - Main entry point for installed package.

Usage:
    syntra --help
    syntra ask "list pods"
    syntra interactive
"""

from syntra_pkg._cli_impl import app


def main():
    """Main entry point for syntra command."""
    app()


if __name__ == "__main__":
    main()
