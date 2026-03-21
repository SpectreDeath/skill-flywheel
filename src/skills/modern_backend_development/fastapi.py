"""
Auto-generated skill for fastapi

This skill wraps the public API of the fastapi library.
Generated on: 2026-03-20T19:12:04.087478
Library version: 0.128.4

Wrapped components: 19

Usage:
    Invoke without action to list available wrappers:
        await invoke({"action": None})
    
    Invoke a specific wrapper:
        await invoke({"action": "function_name", "args": [arg1, arg2], "kwargs": {"key": "value"}})
"""
import inspect
import logging
from typing import Any, Dict, List

import time
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WRAPPED_NAMES = ["APIRouter", "BackgroundTasks", "Body", "Cookie", "Depends", "FastAPI", "File", "Form", "HTTPException", "Header", "Path", "Query", "Request", "Response", "Security", "UploadFile", "WebSocket", "WebSocketDisconnect", "WebSocketException"]

async def APIRouter_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.APIRouter
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "APIRouter")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def BackgroundTasks_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.BackgroundTasks
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "BackgroundTasks")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Body_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.Body
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "Body")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Cookie_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.Cookie
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "Cookie")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Depends_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.Depends
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "Depends")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def FastAPI_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.FastAPI
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "FastAPI")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def File_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.File
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "File")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Form_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.Form
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "Form")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def HTTPException_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.HTTPException
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "HTTPException")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Header_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.Header
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "Header")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Path_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.Path
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "Path")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Query_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.Query
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "Query")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Request_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.Request
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "Request")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Response_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.Response
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "Response")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def Security_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.Security
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "Security")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def UploadFile_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.UploadFile
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "UploadFile")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def WebSocket_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.WebSocket
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "WebSocket")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def WebSocketDisconnect_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.WebSocketDisconnect
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "WebSocketDisconnect")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def WebSocketException_wrapper(args: list, kwargs: dict):
    """
    Wrapper for fastapi.WebSocketException
    
    For classes: instantiates the class with provided args/kwargs and returns the instance.
    For functions: calls the function with provided args/kwargs and returns the result.
    
    Args:
        args: Positional arguments to pass to the function/class
        kwargs: Keyword arguments to pass to the function/class
    
    Returns:
        Result from calling the function or instantiating the class
    """
    try:
        import fastapi
        member = getattr(fastapi, "WebSocketException")
        if inspect.isclass(member):
            instance = member(*args, **kwargs)
            return {"instance": str(instance), "type": type(instance).__name__}
        else:
            return member(*args, **kwargs)
    except Exception as e:
        return {"error": str(e)}

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for skill invocation.
    
    Expected payload:
        - action: str (optional): Name of wrapper to call. If omitted, returns list of available wrappers
        - args: list (optional): Positional arguments for the wrapper
        - kwargs: dict (optional): Keyword arguments for the wrapper
    
    Returns:
        dict with 'result' and 'metadata' keys
    """
    start_time = time.time()
    timestamp = datetime.datetime.now().isoformat()
    
    action = payload.get("action")
    args = payload.get("args", [])
    kwargs = payload.get("kwargs", {})
    
    if action is None:
        return {
            "result": {
                "available_wrappers": list(WRAPPED_NAMES),
                "message": "Available wrappers. Use action parameter to call a specific wrapper."
            },
            "metadata": {
                "timestamp": timestamp,
                "library": "fastapi",
                "function_count": len(WRAPPED_NAMES)
            }
        }
    
    if action not in WRAPPED_NAMES:
        return {
            "result": {"error": "Unknown action: " + action},
            "metadata": {
                "timestamp": timestamp,
                "error": "Action not found in wrapped names"
            }
        }
    
    wrappers = {
        "APIRouter": APIRouter_wrapper,
        "BackgroundTasks": BackgroundTasks_wrapper,
        "Body": Body_wrapper,
        "Cookie": Cookie_wrapper,
        "Depends": Depends_wrapper,
        "FastAPI": FastAPI_wrapper,
        "File": File_wrapper,
        "Form": Form_wrapper,
        "HTTPException": HTTPException_wrapper,
        "Header": Header_wrapper,
        "Path": Path_wrapper,
        "Query": Query_wrapper,
        "Request": Request_wrapper,
        "Response": Response_wrapper,
        "Security": Security_wrapper,
        "UploadFile": UploadFile_wrapper,
        "WebSocket": WebSocket_wrapper,
        "WebSocketDisconnect": WebSocketDisconnect_wrapper,
        "WebSocketException": WebSocketException_wrapper,
    }
    
    try:
        result = await wrappers[action](args, kwargs)
        elapsed = time.time() - start_time
        
        return {
            "result": result,
            "metadata": {
                "timestamp": timestamp,
                "library": "fastapi",
                "library_version": "0.128.4" if "0.128.4" != "None" else None,
                "action": action,
                "elapsed_seconds": elapsed
            }
        }
    except Exception as e:
        logger.error("Error invoking {}: {}".format(action, str(e)))
        return {
            "result": {"error": str(e)},
            "metadata": {
                "timestamp": timestamp,
                "library": "fastapi",
                "error": str(e)
            }
        }


def register_skill():
    """Return skill metadata for registration"""
    return {
        "name": "fastapi-wrapper",
        "description": "Auto-generated skill wrapping fastapi public API",
        "domain": "modern_backend_development",
        "version": "1.0.0",
    }
