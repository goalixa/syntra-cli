"""Setup configuration for Syntra package."""

from setuptools import setup, find_packages

setup(
    name="syntra",
    version="0.1.0",
    packages=find_packages(exclude=["tests.*", "tests", "*.tests.*", "*.tests", "CLI.syntra_pkg"]),
    include_package_data=True,
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "typer[all]>=0.9.0",
        "rich>=14.0.0",
        "httpx>=0.25.0",
        "aiohttp>=3.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.12.0",
            "ruff>=0.1.0",
        ],
        "full": [
            "crewai>=0.1.0",
            "langchain>=0.1.0",
            "chromadb>=0.4.0",
            "redis>=5.0.0",
            "kubernetes>=28.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "syntra=CLI.syntra_pkg.cli:main",
            "syntra-repl=CLI.syntra_pkg.repl:main",
        ],
    },
)
