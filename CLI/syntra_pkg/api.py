#!/usr/bin/env python3
"""
Syntra API Server - Start the FastAPI server.

Usage:
    syntra-api
    syntra-api --port 8080
    syntra-api --host 0.0.0.0
"""


def main():
    """Main entry point for syntra-api command."""
    import uvicorn
    import typer

    app = typer.Typer()

    @app.command()
    def start(
        host: str = typer.Option("0.0.0.0", "--host", "-h", help="Host to bind to"),
        port: int = typer.Option(8000, "--port", "-p", help="Port to bind to"),
        reload: bool = typer.Option(False, "--reload", "-r", help="Enable auto-reload"),
        workers: int = typer.Option(1, "--workers", "-w", help="Number of workers"),
    ):
        """Start the Syntra API server."""
        typer.echo(f"🚀 Starting Syntra API server on {host}:{port}")
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=reload,
            workers=workers if not reload else None,
        )

    app()


if __name__ == "__main__":
    main()
