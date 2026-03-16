#!/usr/bin/env python3
"""
API Integration Skill

This skill provides API integration capabilities including:
- REST API calls
- Authentication handling
- Rate limiting
- Error handling and retries
- Data transformation
"""

import requests
import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import asyncio
from functools import wraps

logger = logging.getLogger(__name__)


class AuthType(Enum):
    NONE = "none"
    BASIC = "basic"
    BEARER = "bearer"
    API_KEY = "api_key"
    OAUTH2 = "oauth2"


@dataclass
class APIConfig:
    """Configuration for API integration"""

    base_url: str
    auth_type: AuthType = AuthType.NONE
    api_key: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    bearer_token: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    rate_limit_delay: float = 0.1
    headers: Dict[str, str] = None


class APIError(Exception):
    """Custom exception for API errors"""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator for retrying API calls on failure"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds..."
                        )
                        await asyncio.sleep(delay * (2**attempt))  # Exponential backoff
                    else:
                        logger.error(f"All {max_retries + 1} attempts failed.")
                        raise e

            raise last_exception

        return wrapper

    return decorator


class APIIntegration:
    """Advanced API integration with authentication and error handling"""

    def __init__(self, config: APIConfig):
        self.config = config
        self.session = requests.Session()
        self._setup_session()
        self.last_request_time = 0

    def _setup_session(self):
        """Setup the requests session with headers and authentication"""
        # Set default headers
        default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "EnhancedMCP/2.0",
        }

        if self.config.headers:
            default_headers.update(self.config.headers)

        self.session.headers.update(default_headers)

        # Setup authentication
        if self.config.auth_type == AuthType.BASIC:
            if not self.config.username or not self.config.password:
                raise ValueError("Username and password required for basic auth")
            self.session.auth = (self.config.username, self.config.password)

        elif self.config.auth_type == AuthType.BEARER:
            if not self.config.bearer_token:
                raise ValueError("Bearer token required")
            self.session.headers["Authorization"] = f"Bearer {self.config.bearer_token}"

        elif self.config.auth_type == AuthType.API_KEY:
            if not self.config.api_key:
                raise ValueError("API key required")
            self.session.headers["X-API-Key"] = self.config.api_key

    def _rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.config.rate_limit_delay:
            sleep_time = self.config.rate_limit_delay - time_since_last
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    @retry_on_failure(max_retries=3, delay=1.0)
    async def make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request with error handling and retries

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            headers: Additional headers

        Returns:
            Response data
        """
        url = f"{self.config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        # Apply rate limiting
        self._rate_limit()

        # Prepare request
        request_kwargs = {"url": url, "timeout": self.config.timeout}

        if data:
            request_kwargs["json"] = data

        if params:
            request_kwargs["params"] = params

        if headers:
            request_kwargs["headers"] = headers

        try:
            # Make synchronous request in thread
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: self.session.request(method.upper(), **request_kwargs)
            )

            # Check for HTTP errors
            response.raise_for_status()

            # Parse response
            try:
                return response.json()
            except json.JSONDecodeError:
                return {"text": response.text, "status_code": response.status_code}

        except requests.exceptions.Timeout:
            raise APIError(
                f"Request timed out after {self.config.timeout} seconds", 408
            )
        except requests.exceptions.ConnectionError:
            raise APIError("Connection error occurred", 0)
        except requests.exceptions.HTTPError as e:
            raise APIError(
                f"HTTP error: {e}", response.status_code if response else None
            )
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {e}", 0)

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make a GET request"""
        return await self.make_request("GET", endpoint, params=params, headers=headers)

    async def post(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make a POST request"""
        return await self.make_request(
            "POST", endpoint, data=data, params=params, headers=headers
        )

    async def put(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make a PUT request"""
        return await self.make_request(
            "PUT", endpoint, data=data, params=params, headers=headers
        )

    async def delete(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make a DELETE request"""
        return await self.make_request(
            "DELETE", endpoint, params=params, headers=headers
        )

    async def patch(
        self,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make a PATCH request"""
        return await self.make_request(
            "PATCH", endpoint, data=data, params=params, headers=headers
        )


async def batch_api_calls(
    calls: List[Dict[str, Any]], config: APIConfig, concurrency_limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Execute multiple API calls concurrently with rate limiting

    Args:
        calls: List of API call configurations
        config: API configuration
        concurrency_limit: Maximum concurrent requests

    Returns:
        List of responses
    """
    api_client = APIIntegration(config)

    async def invoke_call(call_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single API call"""
        try:
            method = call_config.get("method", "GET").upper()
            endpoint = call_config["endpoint"]
            data = call_config.get("data")
            params = call_config.get("params")
            headers = call_config.get("headers")

            response = await api_client.make_request(
                method, endpoint, data=data, params=params, headers=headers
            )
            return {"success": True, "response": response, "call": call_config}

        except Exception as e:
            return {"success": False, "error": str(e), "call": call_config}

    # Create semaphore for concurrency control
    semaphore = asyncio.Semaphore(concurrency_limit)

    async def limited_call(call_config: Dict[str, Any]):
        async with semaphore:
            return await invoke_call(call_config)

    # Execute all calls concurrently
    tasks = [limited_call(call) for call in calls]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    return results


def transform_data(
    data: Dict[str, Any],
    mapping: Dict[str, str],
    filters: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """
    Transform API response data according to mapping rules

    Args:
        data: Input data
        mapping: Field mapping dictionary (source_field -> target_field)
        filters: List of filter operations

    Returns:
        Transformed data
    """
    transformed = {}

    # Apply field mapping
    for source_field, target_field in mapping.items():
        if source_field in data:
            transformed[target_field] = data[source_field]

    # Apply filters
    if filters:
        for filter_config in filters:
            operation = filter_config.get("operation")
            field = filter_config.get("field")
            value = filter_config.get("value")

            if operation == "exclude" and field in transformed:
                del transformed[field]
            elif operation == "include" and field not in transformed:
                if value is not None:
                    transformed[field] = value
            elif operation == "rename" and field in transformed:
                new_name = filter_config.get("new_name")
                if new_name:
                    transformed[new_name] = transformed.pop(field)
            elif operation == "transform" and field in transformed:
                transform_func = filter_config.get("function")
                if transform_func == "uppercase":
                    transformed[field] = str(transformed[field]).upper()
                elif transform_func == "lowercase":
                    transformed[field] = str(transformed[field]).lower()
                elif transform_func == "round":
                    transformed[field] = round(float(transformed[field]))

    return transformed


async def health_check(config: APIConfig) -> Dict[str, Any]:
    """
    Perform health check on the API endpoint

    Args:
        config: API configuration

    Returns:
        Health check results
    """
    try:
        api_client = APIIntegration(config)

        # Try to make a simple GET request to the base URL
        response = await api_client.get("")

        return {
            "status": "healthy",
            "response_time": 0,  # Would need timing implementation
            "response_data": response,
        }

    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


# Example usage and common API configurations
def create_github_api_config(token: str) -> APIConfig:
    """Create configuration for GitHub API"""
    return APIConfig(
        base_url="https://api.github.com",
        auth_type=AuthType.BEARER,
        bearer_token=token,
        headers={"Accept": "application/vnd.github.v3+json"},
    )


def create_openai_api_config(api_key: str) -> APIConfig:
    """Create configuration for OpenAI API"""
    return APIConfig(
        base_url="https://api.openai.com/v1",
        auth_type=AuthType.BEARER,
        bearer_token=api_key,
        headers={"OpenAI-Beta": "assistants=v2"},
    )


# Example usage function
async def example_usage():
    """Example of how to use the API integration skill"""

    # Create API configuration
    config = APIConfig(
        base_url="https://jsonplaceholder.typicode.com",
        auth_type=AuthType.NONE,
        timeout=10,
        max_retries=3,
    )

    api_client = APIIntegration(config)

    try:
        # Make GET request
        posts = await api_client.get("/posts")
        print(f"Retrieved {len(posts)} posts")

        # Make POST request
        new_post = {"title": "Test Post", "body": "This is a test post", "userId": 1}
        created_post = await api_client.post("/posts", data=new_post)
        print(f"Created post with ID: {created_post.get('id')}")

        # Batch requests
        batch_calls = [
            {"method": "GET", "endpoint": "/posts/1"},
            {"method": "GET", "endpoint": "/posts/2"},
            {"method": "GET", "endpoint": "/posts/3"},
        ]

        results = await batch_api_calls(batch_calls, config)
        print(f"Batch results: {len(results)} responses")

    except APIError as e:
        print(f"API Error: {e}")


async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.

    Args:
        payload: dict of input parameters including:
            - action: "make_request", "batch_calls", "transform_data", "health_check"
            - request_data: Request configuration for make_request
            - batch_data: Batch call configuration
            - transform_data: Data transformation configuration
            - config_data: API configuration

    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "health_check")

    try:
        if action == "make_request":
            request_data = payload.get("request_data", {})

            # Create API configuration
            config_data = request_data.get("config", {})
            config = APIConfig(
                base_url=config_data.get(
                    "base_url", "https://jsonplaceholder.typicode.com"
                ),
                auth_type=AuthType(config_data.get("auth_type", "none")),
                api_key=config_data.get("api_key"),
                username=config_data.get("username"),
                password=config_data.get("password"),
                bearer_token=config_data.get("bearer_token"),
                timeout=config_data.get("timeout", 30),
                max_retries=config_data.get("max_retries", 3),
                retry_delay=config_data.get("retry_delay", 1.0),
                rate_limit_delay=config_data.get("rate_limit_delay", 0.1),
                headers=config_data.get("headers"),
            )

            api_client = APIIntegration(config)

            # Make request
            response = await api_client.make_request(
                method=request_data.get("method", "GET"),
                endpoint=request_data.get("endpoint", "/"),
                data=request_data.get("data"),
                params=request_data.get("params"),
                headers=request_data.get("headers"),
            )

            return {
                "result": response,
                "metadata": {
                    "action": "make_request",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "batch_calls":
            batch_data = payload.get("batch_data", {})

            # Create API configuration
            config_data = batch_data.get("config", {})
            config = APIConfig(
                base_url=config_data.get(
                    "base_url", "https://jsonplaceholder.typicode.com"
                ),
                auth_type=AuthType(config_data.get("auth_type", "none")),
                api_key=config_data.get("api_key"),
                username=config_data.get("username"),
                password=config_data.get("password"),
                bearer_token=config_data.get("bearer_token"),
                timeout=config_data.get("timeout", 30),
                max_retries=config_data.get("max_retries", 3),
                retry_delay=config_data.get("retry_delay", 1.0),
                rate_limit_delay=config_data.get("rate_limit_delay", 0.1),
                headers=config_data.get("headers"),
            )

            calls = batch_data.get("calls", [])
            results = await batch_api_calls(calls, config)

            return {
                "result": results,
                "metadata": {
                    "action": "batch_calls",
                    "timestamp": datetime.now().isoformat(),
                    "call_count": len(calls),
                },
            }

        elif action == "transform_data":
            transform_data = payload.get("transform_data", {})

            data = transform_data.get("data", {})
            mapping = transform_data.get("mapping", {})
            filters = transform_data.get("filters", [])

            transformed = transform_data(data, mapping, filters)

            return {
                "result": transformed,
                "metadata": {
                    "action": "transform_data",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        elif action == "health_check":
            config_data = payload.get("config_data", {})

            config = APIConfig(
                base_url=config_data.get(
                    "base_url", "https://jsonplaceholder.typicode.com"
                ),
                auth_type=AuthType(config_data.get("auth_type", "none")),
                api_key=config_data.get("api_key"),
                username=config_data.get("username"),
                password=config_data.get("password"),
                bearer_token=config_data.get("bearer_token"),
                timeout=config_data.get("timeout", 10),
                max_retries=config_data.get("max_retries", 3),
                retry_delay=config_data.get("retry_delay", 1.0),
                rate_limit_delay=config_data.get("rate_limit_delay", 0.1),
                headers=config_data.get("headers"),
            )

            result = await health_check(config)

            return {
                "result": result,
                "metadata": {
                    "action": "health_check",
                    "timestamp": datetime.now().isoformat(),
                },
            }

        else:
            return {
                "result": {"error": f"Unknown action: {action}"},
                "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
            }

    except Exception as e:
        logger.error(f"Error in api_integration: {e}")
        return {
            "result": {"error": str(e)},
            "metadata": {"action": action, "timestamp": datetime.now().isoformat()},
        }


if __name__ == "__main__":
    asyncio.run(example_usage())
