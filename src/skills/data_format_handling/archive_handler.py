"""
Archive Handler Skill

Extract and inspect ZIP, TAR, and GZ archives.
"""
import gzip
import json
import logging
import os
import tarfile
from datetime import datetime
from typing import Any, Dict, List
import zipfile
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def list_zip_contents(file_path: str) -> Dict[str, Any]:
    with zipfile.ZipFile(file_path, 'r') as zf:
        files = []
        for info in zf.filelist:
            files.append({"name": info.filename, "size": info.file_size, "compressed": info.compress_size})
        return {"files": files, "count": len(files), "format": "zip"}

def list_tar_contents(file_path: str) -> Dict[str, Any]:
    with tarfile.open(file_path, 'r:*') as tf:
        files = []
        for member in tf.getmembers():
            files.append({"name": member.name, "size": member.size, "type": "dir" if member.isdir() else "file"})
        return {"files": files, "count": len(files), "format": "tar"}

def extract_zip(file_path: str, output_dir: str) -> str:
    with zipfile.ZipFile(file_path, 'r') as zf:
        zf.extractall(output_dir)
    return output_dir

def extract_tar(file_path: str, output_dir: str) -> str:
    with tarfile.open(file_path, 'r:*') as tf:
        tf.extractall(output_dir)
    return output_dir

def read_gz(file_path: str) -> str:
    with gzip.open(file_path, 'rt') as f:
        return f.read()

async def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    start_time = time.time()
    timestamp = datetime.now().isoformat()
    
    action = payload.get("action", "list")
    file_path = payload.get("file_path")
    output_dir = payload.get("output_dir")
    
    try:
        if not file_path or not os.path.exists(file_path):
            return {"result": {"error": f"File not found: {file_path}"}, "metadata": {"timestamp": timestamp}}
        
        ext = os.path.splitext(file_path)[1].lower()
        
        if action == "list":
            if ext == ".zip":
                data = list_zip_contents(file_path)
            elif ext in (".tar", ".tgz", ".tar.gz", ".tar.bz2"):
                data = list_tar_contents(file_path)
            else:
                return {"result": {"error": f"Unsupported format: {ext}"}, "metadata": {"timestamp": timestamp}}
            return {"result": data, "metadata": {"timestamp": timestamp}}
        
        elif action == "extract":
            if not output_dir:
                return {"result": {"error": "output_dir required"}, "metadata": {"timestamp": timestamp}}
            
            os.makedirs(output_dir, exist_ok=True)
            
            if ext == ".zip":
                extract_zip(file_path, output_dir)
            elif ext in (".tar", ".tgz", ".tar.gz", ".tar.bz2"):
                extract_tar(file_path, output_dir)
            else:
                return {"result": {"error": f"Unsupported format: {ext}"}, "metadata": {"timestamp": timestamp}}
            
            return {"result": {"extracted_to": output_dir}, "metadata": {"timestamp": timestamp}}
        
        elif action == "read_gz":
            if ext == ".gz":
                content = read_gz(file_path)
                return {"result": {"content": content[:1000], "truncated": len(content) > 1000}, "metadata": {"timestamp": timestamp}}
            else:
                return {"result": {"error": "Only .gz files supported for read_gz"}, "metadata": {"timestamp": timestamp}}
        
        else:
            return {"result": {"error": f"Unknown action: {action}"}, "metadata": {"timestamp": timestamp}}
    
    except Exception as e:
        return {"result": {"error": str(e)}, "metadata": {"timestamp": timestamp}}

def register_skill():
    return {"name": "archive-handler", "description": "Extract and inspect ZIP, TAR, and GZ archives", "version": "1.0.0", "domain": "DATA_FORMAT_HANDLING"}
