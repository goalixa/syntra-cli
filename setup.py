"""Setup configuration for Syntra CLI package."""

from setuptools import setup, find_packages

setup(
    name="syntra-cli",
    version="0.1.0",
    packages=find_packages(where="."),
    package_dir={"": "."},
    include_package_data=True,
    install_requires=[
        "typer[all]>=0.9.0",
        "rich>=14.0.0",
        "httpx>=0.25.0",
    ],
    entry_points={
        "console_scripts": [
            "syntra-cli=syntra_pkg.cli:main",
        ],
    },
)
