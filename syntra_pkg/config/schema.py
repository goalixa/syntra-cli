"""Configuration schema validation using Pydantic."""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class APIConfig(BaseModel):
    """API configuration."""

    base_url: str = "http://localhost:8000"
    timeout: float = Field(default=30.0, gt=0, le=300)
    max_retries: int = Field(default=3, ge=0, le=10)
    verify_ssl: bool = True

    @field_validator("base_url")
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        """Ensure base_url doesn't have trailing slash."""
        return v.rstrip("/")


class CLIConfig(BaseModel):
    """CLI configuration."""

    theme: str = Field(default="default", pattern="^(default|dark|light|minimal|hacker)$")
    color_scheme: str = Field(default="auto", pattern="^(auto|never|always)$")
    prompt_style: str = Field(default="fancy", pattern="^(fancy|minimal|context|custom)$")
    enable_completion: bool = True
    editor: Optional[str] = None


class SessionConfig(BaseModel):
    """Session configuration."""

    persist_context: bool = True
    max_history: int = Field(default=1000, ge=0, le=10000)
    timeout: int = Field(default=1800, ge=0, le=86400)  # Max 24 hours
    auto_save: bool = True


class SkillsConfig(BaseModel):
    """Skills configuration."""

    enabled: List[str] = Field(default_factory=list)
    paths: List[str] = Field(default_factory=lambda: ["~/.syntra/skills", ".syntra/skills"])
    auto_discover: bool = True


class OutputConfig(BaseModel):
    """Output configuration."""

    format: str = Field(default="rich", pattern="^(rich|json|markdown|plain)$")
    stream: bool = True
    show_metadata: bool = False
    timestamp: bool = False


class DevConfig(BaseModel):
    """Development configuration."""

    debug: bool = False
    log_level: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    trace_requests: bool = False


class UIConfig(BaseModel):
    """UI configuration."""

    spinner_style: str = Field(default="dots", pattern="^(dots|lines|dots2|bouncing)$")
    progress_bar_style: str = Field(default="bar", pattern="^(bar|blocks|fill)$")
    table_style: str = Field(
        default="rounded",
        pattern="^(rounded|square|rounded_edge|minimal|simple)$"
    )


class SyntraConfig(BaseModel):
    """Complete Syntra configuration."""

    api: APIConfig = Field(default_factory=APIConfig)
    cli: CLIConfig = Field(default_factory=CLIConfig)
    session: SessionConfig = Field(default_factory=SessionConfig)
    skills: SkillsConfig = Field(default_factory=SkillsConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)
    dev: DevConfig = Field(default_factory=DevConfig)
    ui: UIConfig = Field(default_factory=UIConfig)

    class Config:
        """Pydantic config."""

        validate_assignment = True
        extra = "allow"  # Allow extra fields for forward compatibility
