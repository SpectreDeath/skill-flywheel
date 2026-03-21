"""
Image Metadata Skill

Extract metadata from images (PNG, JPEG, etc.).
"""
import logging
import os
from datetime import datetime
from typing import Any, Dict
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _get_pillow():
    try:
        from PIL import Image
        return Image
    except ImportError:
        return None

def _get_exif():
    try:
        from PIL import Image
        return Image
    except ImportError:
        return None

def extract_metadata(file_path: str) -> Dict[str, Any]:
    """Extract metadata from image."""
    PIL = _get_pillow()
    if PIL is None:
        raise ImportError("Pillow not installed: pip install Pillow")
    
    img = PIL.Image.open(file_path)
    
    result = {
        "format": img.format,
        "mode": img.mode,
        "size": img.size,
        "width": img.width,
        "height": img.height,
    }
    
    if hasattr(img, '_getexif') and img._getexif():
        exif = img._getexif()
        if exif:
            exif_data = {}
            for tag, value in exif.items():
                if isinstance(value, bytes):
                    continue
                exif_data[str(tag)] = str(value)[:100]
            result["exif"] = exif_data
    
    return result

def extract_png_info(file_path: str) -> Dict[str, Any]:
    """Extract PNG-specific metadata."""
    PIL = _get_pillow()
    if PIL is None:
        raise ImportError("Pillow not installed")
    
    img = PIL.Image.open(file_path)
    
    result = {
        "format": img.format,
        "mode": img.mode,
        "size": img.size,
        "info": {}
    }
    
    if hasattr(img, 'info'):
        info = img.info
        result["info"] = {k: str(v)[:100] for k, v in info.items() if not isinstance(v, bytes)}
    
    return result

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    start_time = time.time()
    timestamp = datetime.now().isoformat()
    
    action = payload.get("action", "extract")
    file_path = payload.get("file_path")
    
    try:
        if not file_path or not os.path.exists(file_path):
            return {"result": {"error": f"File not found: {file_path}"}, "metadata": {"timestamp": timestamp}}
        
        ext = os.path.splitext(file_path)[1].lower()
        
        if action == "extract":
            if ext in (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"):
                data = extract_metadata(file_path)
            else:
                return {"result": {"error": f"Unsupported format: {ext}"}, "metadata": {"timestamp": timestamp}}
            return {"result": data, "metadata": {"timestamp": timestamp}}
        
        elif action == "dimensions":
            PIL = _get_pillow()
            if PIL is None:
                return {"result": {"error": "Pillow not installed"}}
            
            img = PIL.Image.open(file_path)
            return {"result": {"width": img.width, "height": img.height}, "metadata": {"timestamp": timestamp}}
        
        else:
            return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"timestamp": timestamp}}
    
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"timestamp": timestamp}}

def register_skill():
    return {"name": "image-metadata", "description": "Extract metadata from images (PNG, JPEG, etc.)", "version": "1.0.0", "domain": "DATA_FORMAT_HANDLING"}
