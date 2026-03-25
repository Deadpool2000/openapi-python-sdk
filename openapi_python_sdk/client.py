import base64
import json
from typing import Any, Dict, List, Optional

import httpx

OAUTH_BASE_URL = "https://oauth.openapi.it"
TEST_OAUTH_BASE_URL = "https://test.oauth.openapi.it"


class OauthClient:
    """
    Synchronous client for handling Openapi authentication and token management.
    """

    def __init__(self, username: str, apikey: str, test: bool = False):
        self.client = httpx.Client()
        self.url: str = TEST_OAUTH_BASE_URL if test else OAUTH_BASE_URL
        self.auth_header: str = (
            "Basic " + base64.b64encode(f"{username}:{apikey}".encode("utf-8")).decode()
        )
        self.headers: Dict[str, Any] = {
            "Authorization": self.auth_header,
            "Content-Type": "application/json",
        }

    def __enter__(self):
        """Enable use as a synchronous context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure the underlying HTTP client is closed on exit."""
        self.client.close()

    def close(self):
        """Manually close the underlying HTTP client."""
        self.client.close()

    def get_scopes(self, limit: bool = False) -> Dict[str, Any]:
        """Retrieve available scopes for the current user."""
        params = {"limit": int(limit)}
        url = f"{self.url}/scopes"
        return self.client.get(url=url, headers=self.headers, params=params).json()

    def create_token(self, scopes: List[str] = [], ttl: int = 0) -> Dict[str, Any]:
        """Create a new bearer token with specified scopes and TTL."""
        payload = {"scopes": scopes, "ttl": ttl}
        url = f"{self.url}/token"
        return self.client.post(url=url, headers=self.headers, json=payload).json()

    def get_token(self, scope: str = None) -> Dict[str, Any]:
        """Retrieve an existing token, optionally filtered by scope."""
        params = {"scope": scope or ""}
        url = f"{self.url}/token"
        return self.client.get(url=url, headers=self.headers, params=params).json()

    def delete_token(self, id: str) -> Dict[str, Any]:
        """Revoke/Delete a specific token by ID."""
        url = f"{self.url}/token/{id}"
        return self.client.delete(url=url, headers=self.headers).json()

    def get_counters(self, period: str, date: str) -> Dict[str, Any]:
        """Retrieve usage counters for a specific period and date."""
        url = f"{self.url}/counters/{period}/{date}"
        return self.client.get(url=url, headers=self.headers).json()


class AsyncOauthClient:
    """
    Asynchronous client for handling Openapi authentication and token management.
    Suitable for use with FastAPI, aiohttp, etc.
    """

    def __init__(self, username: str, apikey: str, test: bool = False):
        self.client = httpx.AsyncClient()
        self.url: str = TEST_OAUTH_BASE_URL if test else OAUTH_BASE_URL
        self.auth_header: str = (
            "Basic " + base64.b64encode(f"{username}:{apikey}".encode("utf-8")).decode()
        )
        self.headers: Dict[str, Any] = {
            "Authorization": self.auth_header,
            "Content-Type": "application/json",
        }

    async def __aenter__(self):
        """Enable use as an asynchronous context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Ensure the underlying HTTP client is closed on exit (async)."""
        await self.client.aclose()

    async def aclose(self):
        """Manually close the underlying HTTP client (async)."""
        await self.client.aclose()

    async def get_scopes(self, limit: bool = False) -> Dict[str, Any]:
        """Retrieve available scopes for the current user (async)."""
        params = {"limit": int(limit)}
        url = f"{self.url}/scopes"
        resp = await self.client.get(url=url, headers=self.headers, params=params)
        return resp.json()

    async def create_token(self, scopes: List[str] = [], ttl: int = 0) -> Dict[str, Any]:
        """Create a new bearer token with specified scopes and TTL (async)."""
        payload = {"scopes": scopes, "ttl": ttl}
        url = f"{self.url}/token"
        resp = await self.client.post(url=url, headers=self.headers, json=payload)
        return resp.json()

    async def get_token(self, scope: str = None) -> Dict[str, Any]:
        """Retrieve an existing token, optionally filtered by scope (async)."""
        params = {"scope": scope or ""}
        url = f"{self.url}/token"
        resp = await self.client.get(url=url, headers=self.headers, params=params)
        return resp.json()

    async def delete_token(self, id: str) -> Dict[str, Any]:
        """Revoke/Delete a specific token by ID (async)."""
        url = f"{self.url}/token/{id}"
        resp = await self.client.delete(url=url, headers=self.headers)
        return resp.json()

    async def get_counters(self, period: str, date: str) -> Dict[str, Any]:
        """Retrieve usage counters for a specific period and date (async)."""
        url = f"{self.url}/counters/{period}/{date}"
        resp = await self.client.get(url=url, headers=self.headers)
        return resp.json()


class Client:
    """
    Synchronous client for making authenticated requests to Openapi endpoints.
    """

    def __init__(self, token: str):
        self.client = httpx.Client()
        self.auth_header: str = f"Bearer {token}"
        self.headers: Dict[str, str] = {
            "Authorization": self.auth_header,
            "Content-Type": "application/json",
        }

    def __enter__(self):
        """Enable use as a synchronous context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensure the underlying HTTP client is closed on exit."""
        self.client.close()

    def close(self):
        """Manually close the underlying HTTP client."""
        self.client.close()

    def request(
        self,
        method: str = "GET",
        url: str = None,
        payload: Dict[str, Any] = None,
        params: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Make a synchronous HTTP request to the specified Openapi endpoint.
        """
        payload = payload or {}
        params = params or {}
        url = url or ""
        data = self.client.request(
            method=method,
            url=url,
            headers=self.headers,
            json=payload,
            params=params,
        ).json()

        # Handle cases where the API might return a JSON-encoded string instead of an object
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                pass

        return data


class AsyncClient:
    """
    Asynchronous client for making authenticated requests to Openapi endpoints.
    Suitable for use with FastAPI, aiohttp, etc.
    """

    def __init__(self, token: str):
        self.client = httpx.AsyncClient()
        self.auth_header: str = f"Bearer {token}"
        self.headers: Dict[str, str] = {
            "Authorization": self.auth_header,
            "Content-Type": "application/json",
        }

    async def __aenter__(self):
        """Enable use as an asynchronous context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Ensure the underlying HTTP client is closed on exit (async)."""
        await self.client.aclose()

    async def aclose(self):
        """Manually close the underlying HTTP client (async)."""
        await self.client.aclose()

    async def request(
        self,
        method: str = "GET",
        url: str = None,
        payload: Dict[str, Any] = None,
        params: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Make an asynchronous HTTP request to the specified Openapi endpoint.
        """
        payload = payload or {}
        params = params or {}
        url = url or ""
        resp = await self.client.request(
            method=method,
            url=url,
            headers=self.headers,
            json=payload,
            params=params,
        )
        data = resp.json()

        # Handle cases where the API might return a JSON-encoded string instead of an object
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                pass

        return data