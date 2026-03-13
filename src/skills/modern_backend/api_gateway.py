#!/usr/bin/env python3
"""
Skill: api-gateway
Domain: modern_backend
Description: API Gateway and request routing system
"""

import asyncio
import logging
import time
import uuid
import json
import re
from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
from collections import defaultdict
import hashlib
import jwt
from pathlib import Path

logger = logging.getLogger(__name__)

class HTTPMethod(Enum):
    """HTTP methods"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"

class RouteType(Enum):
    """Route types"""
    STATIC = "static"
    DYNAMIC = "dynamic"
    WILDCARD = "wildcard"
    REGEX = "regex"

class MiddlewareType(Enum):
    """Middleware types"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    RATE_LIMITING = "rate_limiting"
    VALIDATION = "validation"
    LOGGING = "logging"
    TRANSFORMATION = "transformation"

class GatewayStatus(Enum):
    """Gateway status"""
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    DEGRADED = "degraded"
    OFFLINE = "offline"

@dataclass
class Route:
    """Represents an API route"""
    route_id: str
    path: str
    method: HTTPMethod
    route_type: RouteType
    target_service: str
    target_path: str
    middleware: List[str]
    rate_limit: Optional[int]
    timeout: int
    retries: int
    created_at: float

@dataclass
class Middleware:
    """Represents middleware configuration"""
    middleware_id: str
    name: str
    middleware_type: MiddlewareType
    config: Dict[str, Any]
    priority: int
    enabled: bool
    created_at: float

@dataclass
class Service:
    """Represents a backend service"""
    service_id: str
    name: str
    url: str
    health_check_url: Optional[str]
    load_balancing: str  # round_robin, least_connections, ip_hash
    circuit_breaker: bool
    timeout: int
    retries: int
    created_at: float

@dataclass
class RequestLog:
    """Represents a request log entry"""
    log_id: str
    timestamp: float
    method: HTTPMethod
    path: str
    status_code: int
    response_time: float
    client_ip: str
    user_agent: Optional[str]
    service_id: Optional[str]
    error_message: Optional[str]

@dataclass
class RateLimit:
    """Represents rate limiting configuration"""
    limit_id: str
    client_id: str
    window_size: int  # seconds
    max_requests: int
    current_requests: int
    reset_time: float
    created_at: float

class APIGateway:
    """API Gateway and request routing system"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the API Gateway
        
        Args:
            config: Configuration dictionary with:
                - port: Gateway port
                - host: Gateway host
                - max_concurrent_requests: Maximum concurrent requests
                - default_timeout: Default request timeout
                - enable_logging: Enable request logging
        """
        self.port = config.get("port", 8080)
        self.host = config.get("host", "0.0.0.0")
        self.max_concurrent_requests = config.get("max_concurrent_requests", 1000)
        self.default_timeout = config.get("default_timeout", 30)
        self.enable_logging = config.get("enable_logging", True)
        
        self.routes: Dict[str, Route] = {}
        self.middleware: Dict[str, Middleware] = {}
        self.services: Dict[str, Service] = {}
        self.request_logs: List[RequestLog] = []
        self.rate_limits: Dict[str, RateLimit] = {}
        
        self.active_requests = 0
        self.gateway_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0.0,
            "error_rate": 0.0,
            "active_connections": 0
        }
        
        self.gateway_status = GatewayStatus.ACTIVE
        self.logger = logging.getLogger(__name__)
        
        # Start background services
        self._gateway_task = asyncio.create_task(self._gateway_loop())
        self._cleanup_task = asyncio.create_task(self._cleanup_loop())
    
    def add_route(self,
                 path: str,
                 method: HTTPMethod,
                 target_service: str,
                 target_path: str,
                 middleware: Optional[List[str]] = None,
                 rate_limit: Optional[int] = None,
                 timeout: int = 30,
                 retries: int = 3) -> str:
        """
        Add a route to the gateway
        
        Args:
            path: Route path
            method: HTTP method
            target_service: Target service ID
            target_path: Target path on service
            middleware: List of middleware IDs
            rate_limit: Rate limit (requests per minute)
            timeout: Request timeout in seconds
            retries: Number of retries
            
        Returns:
            Route ID
        """
        route_id = str(uuid.uuid4())
        
        # Determine route type
        route_type = RouteType.STATIC
        if "{" in path or "}" in path:
            route_type = RouteType.DYNAMIC
        elif "*" in path:
            route_type = RouteType.WILDCARD
        elif path.startswith("^") and path.endswith("$"):
            route_type = RouteType.REGEX
        
        route = Route(
            route_id=route_id,
            path=path,
            method=method,
            route_type=route_type,
            target_service=target_service,
            target_path=target_path,
            middleware=middleware or [],
            rate_limit=rate_limit,
            timeout=timeout,
            retries=retries,
            created_at=time.time()
        )
        
        self.routes[route_id] = route
        self.logger.info(f"Added route: {route_id} -> {target_service}")
        return route_id
    
    def add_middleware(self,
                      name: str,
                      middleware_type: MiddlewareType,
                      config: Dict[str, Any],
                      priority: int = 100,
                      enabled: bool = True) -> str:
        """
        Add middleware to the gateway
        
        Args:
            name: Middleware name
            middleware_type: Type of middleware
            config: Middleware configuration
            priority: Execution priority (lower = earlier)
            enabled: Whether middleware is enabled
            
        Returns:
            Middleware ID
        """
        middleware_id = str(uuid.uuid4())
        
        middleware = Middleware(
            middleware_id=middleware_id,
            name=name,
            middleware_type=middleware_type,
            config=config,
            priority=priority,
            enabled=enabled,
            created_at=time.time()
        )
        
        self.middleware[middleware_id] = middleware
        self.logger.info(f"Added middleware: {middleware_id} ({name})")
        return middleware_id
    
    def add_service(self,
                   name: str,
                   url: str,
                   health_check_url: Optional[str] = None,
                   load_balancing: str = "round_robin",
                   circuit_breaker: bool = True,
                   timeout: int = 30,
                   retries: int = 3) -> str:
        """
        Add a backend service
        
        Args:
            name: Service name
            url: Service URL
            health_check_url: Health check URL
            load_balancing: Load balancing strategy
            circuit_breaker: Enable circuit breaker
            timeout: Request timeout
            retries: Number of retries
            
        Returns:
            Service ID
        """
        service_id = str(uuid.uuid4())
        
        service = Service(
            service_id=service_id,
            name=name,
            url=url,
            health_check_url=health_check_url,
            load_balancing=load_balancing,
            circuit_breaker=circuit_breaker,
            timeout=timeout,
            retries=retries,
            created_at=time.time()
        )
        
        self.services[service_id] = service
        self.logger.info(f"Added service: {service_id} ({name})")
        return service_id
    
    def route_request(self,
                     method: HTTPMethod,
                     path: str,
                     headers: Dict[str, str],
                     body: Optional[str] = None,
                     client_ip: str = "127.0.0.1") -> Dict[str, Any]:
        """
        Route a request through the gateway
        
        Args:
            method: HTTP method
            path: Request path
            headers: Request headers
            body: Request body
            client_ip: Client IP address
            
        Returns:
            Response dictionary
        """
        start_time = time.time()
        
        try:
            # Check rate limiting
            if not self._check_rate_limit(client_ip):
                return self._create_error_response(429, "Rate limit exceeded")
            
            # Find matching route
            route = self._find_route(method, path)
            if not route:
                return self._create_error_response(404, "Route not found")
            
            # Execute middleware
            middleware_result = self._execute_middleware(route, headers, body)
            if not middleware_result["success"]:
                return self._create_error_response(401, middleware_result["message"])
            
            # Route to service
            response = self._forward_to_service(route, headers, body)
            
            # Log request
            if self.enable_logging:
                self._log_request(method, path, response["status_code"], 
                                time.time() - start_time, client_ip, 
                                headers.get("User-Agent"), route.target_service)
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error routing request: {e}")
            return self._create_error_response(500, str(e))
    
    def get_gateway_stats(self) -> Dict[str, Any]:
        """Get gateway statistics"""
        return {
            "total_requests": self.gateway_stats["total_requests"],
            "successful_requests": self.gateway_stats["successful_requests"],
            "failed_requests": self.gateway_stats["failed_requests"],
            "average_response_time": self.gateway_stats["average_response_time"],
            "error_rate": self.gateway_stats["error_rate"],
            "active_connections": self.gateway_stats["active_connections"],
            "gateway_status": self.gateway_status.value,
            "total_routes": len(self.routes),
            "total_middleware": len(self.middleware),
            "total_services": len(self.services)
        }
    
    def get_request_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get request logs"""
        return [
            {
                "log_id": log.log_id,
                "timestamp": datetime.fromtimestamp(log.timestamp).isoformat(),
                "method": log.method.value,
                "path": log.path,
                "status_code": log.status_code,
                "response_time": log.response_time,
                "client_ip": log.client_ip,
                "user_agent": log.user_agent,
                "service_id": log.service_id,
                "error_message": log.error_message
            }
            for log in self.request_logs[-limit:]
        ]
    
    def set_gateway_status(self, status: GatewayStatus):
        """Set gateway status"""
        self.gateway_status = status
        self.logger.info(f"Gateway status changed to: {status.value}")
    
    def _find_route(self, method: HTTPMethod, path: str) -> Optional[Route]:
        """Find matching route for request"""
        # Sort routes by priority (static first, then dynamic, etc.)
        routes_by_type = defaultdict(list)
        for route in self.routes.values():
            if route.method == method:
                routes_by_type[route.route_type].append(route)
        
        # Check static routes first
        for route in routes_by_type[RouteType.STATIC]:
            if route.path == path:
                return route
        
        # Check dynamic routes
        for route in routes_by_type[RouteType.DYNAMIC]:
            if self._match_dynamic_route(route.path, path):
                return route
        
        # Check wildcard routes
        for route in routes_by_type[RouteType.WILDCARD]:
            if self._match_wildcard_route(route.path, path):
                return route
        
        # Check regex routes
        for route in routes_by_type[RouteType.REGEX]:
            if self._match_regex_route(route.path, path):
                return route
        
        return None
    
    def _match_dynamic_route(self, route_path: str, request_path: str) -> bool:
        """Match dynamic route with parameters"""
        # Convert {param} to named groups
        pattern = re.escape(route_path).replace(r'\{', '(?P<').replace(r'\}', '>[^/]+)')
        pattern = f"^{pattern}$"
        
        match = re.match(pattern, request_path)
        return match is not None
    
    def _match_wildcard_route(self, route_path: str, request_path: str) -> bool:
        """Match wildcard route"""
        pattern = route_path.replace("*", ".*")
        pattern = f"^{pattern}$"
        
        match = re.match(pattern, request_path)
        return match is not None
    
    def _match_regex_route(self, route_path: str, request_path: str) -> bool:
        """Match regex route"""
        pattern = route_path.strip("^$")  # Remove anchors if present
        pattern = f"^{pattern}$"
        
        match = re.match(pattern, request_path)
        return match is not None
    
    def _execute_middleware(self, route: Route, headers: Dict[str, str], body: Optional[str]) -> Dict[str, Any]:
        """Execute middleware chain"""
        # Get middleware for this route
        route_middleware = [self.middleware[mid] for mid in route.middleware if mid in self.middleware]
        
        # Sort by priority
        route_middleware.sort(key=lambda m: m.priority)
        
        # Execute middleware
        for middleware in route_middleware:
            if not middleware.enabled:
                continue
            
            try:
                if middleware.middleware_type == MiddlewareType.AUTHENTICATION:
                    result = self._auth_middleware(middleware, headers)
                elif middleware.middleware_type == MiddlewareType.AUTHORIZATION:
                    result = self._authz_middleware(middleware, headers, route)
                elif middleware.middleware_type == MiddlewareType.RATE_LIMITING:
                    result = self._rate_limit_middleware(middleware, headers)
                elif middleware.middleware_type == MiddlewareType.VALIDATION:
                    result = self._validation_middleware(middleware, headers, body)
                elif middleware.middleware_type == MiddlewareType.TRANSFORMATION:
                    result = self._transformation_middleware(middleware, headers, body)
                else:
                    result = {"success": True}
                
                if not result["success"]:
                    return result
                    
            except Exception as e:
                self.logger.error(f"Middleware {middleware.name} failed: {e}")
                return {"success": False, "message": f"Middleware error: {str(e)}"}
        
        return {"success": True}
    
    def _auth_middleware(self, middleware: Middleware, headers: Dict[str, str]) -> Dict[str, Any]:
        """Authentication middleware"""
        auth_header = headers.get("Authorization", "")
        
        if not auth_header.startswith("Bearer "):
            return {"success": False, "message": "Missing or invalid authorization header"}
        
        token = auth_header[7:]  # Remove "Bearer " prefix
        
        try:
            # In a real implementation, this would validate the JWT token
            # For now, simulate validation
            if len(token) < 10:
                return {"success": False, "message": "Invalid token"}
            
            return {"success": True, "user_id": "user123"}
            
        except Exception:
            return {"success": False, "message": "Token validation failed"}
    
    def _authz_middleware(self, middleware: Middleware, headers: Dict[str, str], route: Route) -> Dict[str, Any]:
        """Authorization middleware"""
        # In a real implementation, this would check user permissions
        # For now, simulate authorization
        return {"success": True}
    
    def _rate_limit_middleware(self, middleware: Middleware, headers: Dict[str, str]) -> Dict[str, Any]:
        """Rate limiting middleware"""
        client_ip = headers.get("X-Forwarded-For", headers.get("X-Real-IP", "127.0.0.1"))
        
        if not self._check_rate_limit(client_ip):
            return {"success": False, "message": "Rate limit exceeded"}
        
        return {"success": True}
    
    def _validation_middleware(self, middleware: Middleware, headers: Dict[str, str], body: Optional[str]) -> Dict[str, Any]:
        """Request validation middleware"""
        # In a real implementation, this would validate request body against schema
        # For now, simulate validation
        return {"success": True}
    
    def _transformation_middleware(self, middleware: Middleware, headers: Dict[str, str], body: Optional[str]) -> Dict[str, Any]:
        """Request/response transformation middleware"""
        # In a real implementation, this would transform requests/responses
        # For now, simulate transformation
        return {"success": True}
    
    def _check_rate_limit(self, client_ip: str) -> bool:
        """Check rate limiting for client"""
        current_time = time.time()
        window_size = 60  # 1 minute window
        max_requests = 100  # 100 requests per minute
        
        if client_ip not in self.rate_limits:
            self.rate_limits[client_ip] = RateLimit(
                limit_id=str(uuid.uuid4()),
                client_id=client_ip,
                window_size=window_size,
                max_requests=max_requests,
                current_requests=0,
                reset_time=current_time + window_size,
                created_at=current_time
            )
        
        rate_limit = self.rate_limits[client_ip]
        
        # Reset window if expired
        if current_time >= rate_limit.reset_time:
            rate_limit.current_requests = 0
            rate_limit.reset_time = current_time + window_size
        
        # Check limit
        if rate_limit.current_requests >= rate_limit.max_requests:
            return False
        
        rate_limit.current_requests += 1
        return True
    
    def _forward_to_service(self, route: Route, headers: Dict[str, str], body: Optional[str]) -> Dict[str, Any]:
        """Forward request to backend service"""
        service = self.services[route.target_service]
        
        # In a real implementation, this would make HTTP requests to the service
        # For now, simulate the request
        import random
        
        # Simulate different response times and errors
        response_time = random.uniform(0.1, 2.0)
        status_code = random.choices([200, 404, 500], weights=[80, 15, 5])[0]
        
        if status_code == 200:
            response_body = {"message": "Success", "data": {"id": 123}}
        elif status_code == 404:
            response_body = {"error": "Not found"}
        else:
            response_body = {"error": "Internal server error"}
        
        return {
            "status_code": status_code,
            "headers": {"Content-Type": "application/json"},
            "body": response_body,
            "response_time": response_time
        }
    
    def _create_error_response(self, status_code: int, message: str) -> Dict[str, Any]:
        """Create error response"""
        return {
            "status_code": status_code,
            "headers": {"Content-Type": "application/json"},
            "body": {"error": message},
            "response_time": 0.0
        }
    
    def _log_request(self,
                    method: HTTPMethod,
                    path: str,
                    status_code: int,
                    response_time: float,
                    client_ip: str,
                    user_agent: Optional[str],
                    service_id: Optional[str]):
        """Log request details"""
        log = RequestLog(
            log_id=str(uuid.uuid4()),
            timestamp=time.time(),
            method=method,
            path=path,
            status_code=status_code,
            response_time=response_time,
            client_ip=client_ip,
            user_agent=user_agent,
            service_id=service_id,
            error_message=None if status_code < 400 else "Request failed"
        )
        
        self.request_logs.append(log)
        
        # Update statistics
        self.gateway_stats["total_requests"] += 1
        if status_code < 400:
            self.gateway_stats["successful_requests"] += 1
        else:
            self.gateway_stats["failed_requests"] += 1
        
        # Update average response time
        total_time = self.gateway_stats["average_response_time"] * (self.gateway_stats["total_requests"] - 1)
        self.gateway_stats["average_response_time"] = (total_time + response_time) / self.gateway_stats["total_requests"]
        
        # Update error rate
        self.gateway_stats["error_rate"] = (self.gateway_stats["failed_requests"] / self.gateway_stats["total_requests"]) * 100
    
    async def _gateway_loop(self):
        """Background gateway monitoring loop"""
        while True:
            try:
                await self._monitor_gateway()
                await asyncio.sleep(30)
            except Exception as e:
                self.logger.error(f"Error in gateway loop: {e}")
                await asyncio.sleep(30)
    
    async def _monitor_gateway(self):
        """Monitor gateway health"""
        # Check service health
        for service_id, service in self.services.items():
            if service.health_check_url:
                try:
                    # In a real implementation, this would make HTTP requests
                    # For now, simulate health check
                    pass
                except Exception:
                    self.logger.warning(f"Service {service.name} health check failed")
    
    async def _cleanup_loop(self):
        """Background cleanup loop"""
        while True:
            try:
                await self._cleanup_old_logs()
                await asyncio.sleep(3600)  # Run every hour
            except Exception as e:
                self.logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(3600)
    
    async def _cleanup_old_logs(self):
        """Clean up old request logs"""
        cutoff_time = time.time() - (24 * 3600)  # Keep 24 hours of logs
        
        self.request_logs = [
            log for log in self.request_logs if log.timestamp > cutoff_time
        ]

# Global API Gateway instance
_api_gateway = APIGateway({})

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for skill invocation.
    
    Args:
        payload: dict of input parameters including:
            - action: "add_route", "add_middleware", "add_service", 
                     "route_request", "get_stats", "get_logs", "set_status"
            - route_data: Route configuration
            - middleware_data: Middleware configuration
            - service_data: Service configuration
            - request_data: Request data
            
    Returns:
        dict with 'result' key and optional 'metadata'
    """
    action = payload.get("action", "get_stats")
    
    try:
        if action == "add_route":
            route_data = payload.get("route_data", {})
            
            route_id = _api_gateway.add_route(
                path=route_data.get("path", "/"),
                method=HTTPMethod(route_data.get("method", "GET")),
                target_service=route_data.get("target_service", ""),
                target_path=route_data.get("target_path", "/"),
                middleware=route_data.get("middleware", []),
                rate_limit=route_data.get("rate_limit"),
                timeout=route_data.get("timeout", 30),
                retries=route_data.get("retries", 3)
            )
            
            return {
                "result": {
                    "route_id": route_id,
                    "message": f"Added route: {route_id}"
                },
                "metadata": {
                    "action": "add_route",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "add_middleware":
            middleware_data = payload.get("middleware_data", {})
            
            middleware_id = _api_gateway.add_middleware(
                name=middleware_data.get("name", "Middleware"),
                middleware_type=MiddlewareType(middleware_data.get("middleware_type", "logging")),
                config=middleware_data.get("config", {}),
                priority=middleware_data.get("priority", 100),
                enabled=middleware_data.get("enabled", True)
            )
            
            return {
                "result": {
                    "middleware_id": middleware_id,
                    "message": f"Added middleware: {middleware_id}"
                },
                "metadata": {
                    "action": "add_middleware",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "add_service":
            service_data = payload.get("service_data", {})
            
            service_id = _api_gateway.add_service(
                name=service_data.get("name", "Service"),
                url=service_data.get("url", ""),
                health_check_url=service_data.get("health_check_url"),
                load_balancing=service_data.get("load_balancing", "round_robin"),
                circuit_breaker=service_data.get("circuit_breaker", True),
                timeout=service_data.get("timeout", 30),
                retries=service_data.get("retries", 3)
            )
            
            return {
                "result": {
                    "service_id": service_id,
                    "message": f"Added service: {service_id}"
                },
                "metadata": {
                    "action": "add_service",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "route_request":
            request_data = payload.get("request_data", {})
            
            response = _api_gateway.route_request(
                method=HTTPMethod(request_data.get("method", "GET")),
                path=request_data.get("path", "/"),
                headers=request_data.get("headers", {}),
                body=request_data.get("body"),
                client_ip=request_data.get("client_ip", "127.0.0.1")
            )
            
            return {
                "result": response,
                "metadata": {
                    "action": "route_request",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_stats":
            stats = _api_gateway.get_gateway_stats()
            
            return {
                "result": stats,
                "metadata": {
                    "action": "get_stats",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "get_logs":
            limit = payload.get("limit", 100)
            logs = _api_gateway.get_request_logs(limit)
            
            return {
                "result": logs,
                "metadata": {
                    "action": "get_logs",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        elif action == "set_status":
            status_data = payload.get("status_data", {})
            status = GatewayStatus(status_data.get("status", "active"))
            _api_gateway.set_gateway_status(status)
            
            return {
                "result": {
                    "status": status.value,
                    "message": f"Gateway status set to: {status.value}"
                },
                "metadata": {
                    "action": "set_status",
                    "timestamp": datetime.now().isoformat()
                }
            }
        
        else:
            return {
                "result": {
                    "error": f"Unknown action: {action}"
                },
                "metadata": {
                    "action": action,
                    "timestamp": datetime.now().isoformat()
                }
            }
    
    except Exception as e:
        logger.error(f"Error in api_gateway: {e}")
        return {
            "result": {
                "error": str(e)
            },
            "metadata": {
                "action": action,
                "timestamp": datetime.now().isoformat()
            }
        }

# Example usage function
async def example_usage():
    """Example of how to use the API Gateway skill"""
    
    # Add services
    user_service = await invoke({
        "action": "add_service",
        "service_data": {
            "name": "User Service",
            "url": "http://localhost:3001",
            "health_check_url": "http://localhost:3001/health",
            "load_balancing": "round_robin",
            "circuit_breaker": True,
            "timeout": 30,
            "retries": 3
        }
    })
    
    order_service = await invoke({
        "action": "add_service",
        "service_data": {
            "name": "Order Service",
            "url": "http://localhost:3002",
            "health_check_url": "http://localhost:3002/health",
            "load_balancing": "round_robin",
            "circuit_breaker": True,
            "timeout": 30,
            "retries": 3
        }
    })
    
    print(f"Added services: {user_service['result']['service_id']}, {order_service['result']['service_id']}")
    
    # Add middleware
    auth_middleware = await invoke({
        "action": "add_middleware",
        "middleware_data": {
            "name": "Authentication",
            "middleware_type": "authentication",
            "config": {"secret_key": "my-secret"},
            "priority": 10,
            "enabled": True
        }
    })
    
    rate_limit_middleware = await invoke({
        "action": "add_middleware",
        "middleware_data": {
            "name": "Rate Limiting",
            "middleware_type": "rate_limiting",
            "config": {"max_requests": 100, "window_size": 60},
            "priority": 20,
            "enabled": True
        }
    })
    
    print(f"Added middleware: {auth_middleware['result']['middleware_id']}, {rate_limit_middleware['result']['middleware_id']}")
    
    # Add routes
    user_route = await invoke({
        "action": "add_route",
        "route_data": {
            "path": "/api/users",
            "method": "GET",
            "target_service": user_service['result']['service_id'],
            "target_path": "/users",
            "middleware": [auth_middleware['result']['middleware_id'], rate_limit_middleware['result']['middleware_id']],
            "rate_limit": 100,
            "timeout": 30,
            "retries": 3
        }
    })
    
    order_route = await invoke({
        "action": "add_route",
        "route_data": {
            "path": "/api/orders/{id}",
            "method": "GET",
            "target_service": order_service['result']['service_id'],
            "target_path": "/orders/{id}",
            "middleware": [auth_middleware['result']['middleware_id']],
            "rate_limit": 50,
            "timeout": 30,
            "retries": 3
        }
    })
    
    print(f"Added routes: {user_route['result']['route_id']}, {order_route['result']['route_id']}")
    
    # Route requests
    response1 = await invoke({
        "action": "route_request",
        "request_data": {
            "method": "GET",
            "path": "/api/users",
            "headers": {
                "Authorization": "Bearer valid-token-123",
                "Content-Type": "application/json"
            },
            "client_ip": "192.168.1.100"
        }
    })
    
    response2 = await invoke({
        "action": "route_request",
        "request_data": {
            "method": "GET",
            "path": "/api/orders/123",
            "headers": {
                "Authorization": "Bearer valid-token-456",
                "Content-Type": "application/json"
            },
            "client_ip": "192.168.1.101"
        }
    })
    
    print(f"Request 1 response: {response1['result']}")
    print(f"Request 2 response: {response2['result']}")
    
    # Get gateway statistics
    stats = await invoke({"action": "get_stats"})
    print(f"Gateway stats: {stats['result']}")
    
    # Get request logs
    logs = await invoke({"action": "get_logs", "limit": 10})
    print(f"Recent logs: {len(logs['result'])} entries")

if __name__ == "__main__":
    asyncio.run(example_usage())