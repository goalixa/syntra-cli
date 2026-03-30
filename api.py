"""API client for Syntra backend."""

import httpx
from typing import Optional, Dict, Any
from rich.console import Console

console = Console()


class SyntraAPIError(Exception):
    """Custom exception for API errors."""

    pass


class SyntraAPI:
    """API client for Syntra backend."""

    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        """Initialize async client."""
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close async client."""
        if self.client:
            await self.client.aclose()

    async def ask(self, prompt: str) -> Dict[str, Any]:
        """
        Send a prompt to Syntra AI.

        Args:
            prompt: User's prompt/question

        Returns:
            API response dictionary

        Raises:
            SyntraAPIError: If the request fails
        """
        try:
            response = await self.client.post(
                "/api/ask",
                json={"prompt": prompt},
            )
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            raise SyntraAPIError(f"Failed to connect to Syntra API: {e}")

        except Exception as e:
            raise SyntraAPIError(f"Unexpected error: {e}")

    async def health(self) -> Dict[str, Any]:
        """
        Check API health status.

        Returns:
            Health status dictionary
        """
        try:
            response = await self.client.get("/")
            response.raise_for_status()
            return response.json()

        except httpx.HTTPError as e:
            raise SyntraAPIError(f"Failed to check API health: {e}")
