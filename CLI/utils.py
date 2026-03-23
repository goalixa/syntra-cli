"""Utility functions for CLI."""

import asyncio
from typing import Callable, Any
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.text import Text

console = Console()


async def run_with_spinner(
    func: Callable,
    message: str = "Processing...",
    *args,
    **kwargs
) -> Any:
    """
    Run an async function with a spinner.

    Args:
        func: Async function to run
        message: Message to display
        *args: Arguments to pass to func
        **kwargs: Keyword arguments to pass to func

    Returns:
        Result of func
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(message, total=None)
        result = await func(*args, **kwargs)
        progress.remove_task(task)
        return result


def format_output(text: str, style: str = "primary") -> None:
    """
    Format and print text with style.

    Args:
        text: Text to print
        style: Rich style name
    """
    console.print(text, style=style)


def print_panel(
    content: str,
    title: str = "",
    border_style: str = "primary",
) -> None:
    """
    Print content in a panel.

    Args:
        content: Panel content
        title: Panel title
        border_style: Border style
    """
    panel = Panel(content, title=title, border_style=border_style)
    console.print(panel)


def print_header(text: str) -> None:
    """
    Print a styled header.

    Args:
        text: Header text
    """
    header = Text(text, style="header")
    console.print()
    console.print(header)
    console.print()


def print_success(text: str) -> None:
    """Print success message."""
    console.print(f"✓ {text}", style="success")


def print_error(text: str) -> None:
    """Print error message."""
    console.print(f"✗ {text}", style="error")


def print_warning(text: str) -> None:
    """Print warning message."""
    console.print(f"⚠ {text}", style="warning")


def print_info(text: str) -> None:
    """Print info message."""
    console.print(f"ℹ {text}", style="info")
