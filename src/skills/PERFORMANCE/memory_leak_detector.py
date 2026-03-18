"""
Memory Leak Detector: Memory profiling analysis skill

This module provides memory leak detection capabilities:
- Parse memory dumps from Heapy, tracemalloc, memray
- Identify objects growing over time
- Find references holding onto memory
- Detect common leak patterns
- Suggest fixes for memory issues
"""

import re
import json
from typing import Dict, List, Any, Optional
from collections import defaultdict


def memory_leak_detector(memory_dump: str, options: dict) -> dict:
    """
    Analyze memory dump to detect memory leaks.

    Args:
        memory_dump: Memory profiling output (Heapy, tracemalloc, or memray)
        options: Configuration options including:
            - tool_type: "heapy", "tracemalloc", "memray", or "auto"
            - threshold: Minimum memory size in MB to report (default: 1.0)
            - top_n: Number of top leaks to return (default: 10)

    Returns:
        Dictionary with analysis results containing:
            - status: "success" or "error"
            - leaks: Detected memory leaks
            - growing_objects: Objects growing over time
            - references: Reference analysis
            - suggestions: Fix suggestions
    """
    try:
        options = _normalize_options(options)
        tool_type = options.get("tool_type", _detect_tool_type(memory_dump))

        if tool_type == "heapy":
            return _analyze_heapy(memory_dump, options)
        elif tool_type == "tracemalloc":
            return _analyze_tracemalloc(memory_dump, options)
        elif tool_type == "memray":
            return _analyze_memray(memory_dump, options)
        else:
            return _analyze_heapy(memory_dump, options)

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to analyze memory dump",
        }


def _normalize_options(options: dict) -> dict:
    defaults = {
        "tool_type": "auto",
        "threshold": 1.0,
        "top_n": 10,
    }
    return {**defaults, **options}


def _detect_tool_type(memory_dump: str) -> str:
    dump_lower = memory_dump.strip().lower()

    if memory_dump.startswith("[") or memory_dump.startswith("{"):
        try:
            json_data = json.loads(memory_dump)
            if "allocations" in json_data or "memory_usage" in json_data:
                return "memray"
            if "traceback" in str(json_data):
                return "tracemalloc"
        except:
            pass

    if "heapy" in dump_lower or "guppy" in dump_lower:
        return "heapy"
    if "tracemalloc" in dump_lower:
        return "tracemalloc"
    if "memray" in dump_lower:
        return "memray"
    if "partition" in dump_lower and "size" in dump_lower:
        return "heapy"
    if "filename:lineno" in dump_lower and "size" in dump_lower:
        return "tracemalloc"

    return "tracemalloc"


def _analyze_heapy(memory_dump: str, options: dict) -> dict:
    leaks = _parse_heapy_leaks(memory_dump, options)
    growing_objects = _identify_growing_objects_heapy(memory_dump, options)
    references = _find_references_heapy(memory_dump, options)
    patterns = _detect_leak_patterns(leaks, "heapy")
    suggestions = _generate_suggestions(leaks, patterns, "heapy")

    return {
        "status": "success",
        "tool_type": "heapy",
        "leaks": leaks,
        "growing_objects": growing_objects,
        "references": references,
        "suggestions": suggestions,
        "patterns_detected": patterns,
    }


def _analyze_tracemalloc(memory_dump: str, options: dict) -> dict:
    leaks = _parse_tracemalloc_leaks(memory_dump, options)
    growing_objects = _identify_growing_objects_tracemalloc(memory_dump, options)
    references = _find_references_tracemalloc(memory_dump, options)
    patterns = _detect_leak_patterns(leaks, "tracemalloc")
    suggestions = _generate_suggestions(leaks, patterns, "tracemalloc")

    return {
        "status": "success",
        "tool_type": "tracemalloc",
        "leaks": leaks,
        "growing_objects": growing_objects,
        "references": references,
        "suggestions": suggestions,
        "patterns_detected": patterns,
    }


def _analyze_memray(memory_dump: str, options: dict) -> dict:
    leaks = _parse_memray_leaks(memory_dump, options)
    growing_objects = _identify_growing_objects_memray(memory_dump, options)
    references = _find_references_memray(memory_dump, options)
    patterns = _detect_leak_patterns(leaks, "memray")
    suggestions = _generate_suggestions(leaks, patterns, "memray")

    return {
        "status": "success",
        "tool_type": "memray",
        "leaks": leaks,
        "growing_objects": growing_objects,
        "references": references,
        "suggestions": suggestions,
        "patterns_detected": patterns,
    }


def _parse_heapy_leaks(memory_dump: str, options: dict) -> List[dict]:
    leaks = []
    threshold_mb = options.get("threshold", 1.0)

    partition_pattern = (
        r"Partition of a set of (\d+) objects\. Total size = (\d+\.?\d*) (KB|MB|GB)\."
    )
    size_pattern = r"(\d+\.?\d*) (KB|MB|GB)\s+(.+?)\s+(\d+)"

    match = re.search(partition_pattern, memory_dump)
    if not match:
        return leaks

    total_objects = int(match.group(1))
    total_size = _convert_to_mb(float(match.group(2)), match.group(3))

    for line in re.finditer(size_pattern, memory_dump):
        size = _convert_to_mb(float(line.group(1)), line.group(2))
        if size >= threshold_mb:
            leaks.append(
                {
                    "type": line.group(3).strip(),
                    "size_mb": size,
                    "count": int(line.group(4)),
                    "severity": _calculate_severity(size, threshold_mb),
                }
            )

    leaks.sort(key=lambda x: x["size_mb"], reverse=True)
    return leaks[: options.get("top_n", 10)]


def _parse_tracemalloc_leaks(memory_dump: str, options: dict) -> List[dict]:
    leaks = []
    threshold_mb = options.get("threshold", 1.0)

    line_pattern = r"filename:lineno\(function\)\s+(\d+\.?\d*) (KB|MB|GB)\s+(\d+)"

    for line in re.finditer(line_pattern, memory_dump):
        size = _convert_to_mb(float(line.group(1)), line.group(2))
        if size >= threshold_mb:
            leaks.append(
                {
                    "location": line.group(0).split("(")[0].strip(),
                    "size_mb": size,
                    "count": int(line.group(3)),
                    "severity": _calculate_severity(size, threshold_mb),
                }
            )

    leaks.sort(key=lambda x: x["size_mb"], reverse=True)
    return leaks[: options.get("top_n", 10)]


def _parse_memray_leaks(memory_dump: str, options: dict) -> List[dict]:
    leaks = []
    threshold_mb = options.get("threshold", 1.0)

    try:
        data = json.loads(memory_dump)
        allocations = data.get("allocations", [])

        size_by_location = defaultdict(lambda: {"size": 0, "count": 0})
        for alloc in allocations:
            size = _convert_to_mb(alloc.get("size", 0), alloc.get("unit", "B"))
            location = f"{alloc.get('filename')}:{alloc.get('lineno')}"
            size_by_location[location]["size"] += size
            size_by_location[location]["count"] += 1

        for location, info in size_by_location.items():
            if info["size"] >= threshold_mb:
                leaks.append(
                    {
                        "location": location,
                        "size_mb": info["size"],
                        "count": info["count"],
                        "severity": _calculate_severity(info["size"], threshold_mb),
                    }
                )
    except json.JSONDecodeError:
        pass

    leaks.sort(key=lambda x: x["size_mb"], reverse=True)
    return leaks[: options.get("top_n", 10)]


def _identify_growing_objects_heapy(memory_dump: str, options: dict) -> List[dict]:
    growing = []

    snapshot_pattern = r"Snapshot (\d+).*?Total size = (\d+\.?\d*) (KB|MB|GB)"
    matches = re.findall(snapshot_pattern, memory_dump)

    if len(matches) >= 2:
        for i in range(len(matches) - 1):
            size1 = _convert_to_mb(float(matches[i][1]), matches[i][2])
            size2 = _convert_to_mb(float(matches[i + 1][1]), matches[i + 1][2])
            growth = size2 - size1
            if growth > 0:
                growing.append(
                    {
                        "snapshot_from": matches[i][0],
                        "snapshot_to": matches[i + 1][0],
                        "growth_mb": round(growth, 2),
                        "growth_percentage": round(
                            (growth / size1 * 100) if size1 > 0 else 0, 2
                        ),
                    }
                )

    return growing


def _identify_growing_objects_tracemalloc(
    memory_dump: str, options: dict
) -> List[dict]:
    growing = []

    stat_pattern = r"(Top \d+ memory allocations|tracemalloc snapshot)"
    if "Top 10 differences" in memory_dump or "Top differences" in memory_dump:
        diff_pattern = r"\+ (\d+\.?\d*) (KB|MB|GB)\s+(.+?)(?:\n|$)"
        for match in re.finditer(diff_pattern, memory_dump):
            size = _convert_to_mb(float(match.group(1)), match.group(2))
            growing.append(
                {
                    "object": match.group(3).strip(),
                    "size_mb": size,
                    "type": "difference",
                }
            )

    return growing[:10]


def _identify_growing_objects_memray(memory_dump: str, options: dict) -> List[dict]:
    growing = []

    try:
        data = json.loads(memory_dump)
        timeline = data.get("timeline", [])

        if len(timeline) >= 2:
            for i in range(len(timeline) - 1):
                size1 = timeline[i].get("memory", 0)
                size2 = timeline[i + 1].get("memory", 0)
                growth = _convert_to_mb(size2 - size1, "B")
                if growth > 0:
                    growing.append(
                        {
                            "timestamp": timeline[i + 1].get("timestamp"),
                            "growth_mb": round(growth, 2),
                        }
                    )
    except:
        pass

    return growing[:10]


def _find_references_heapy(memory_dump: str, options: dict) -> List[dict]:
    references = []

    ref_pattern = r"(\w+)\s+->\s+(\w+).*?(\d+\.?\d*) (KB|MB|GB)"
    for match in re.finditer(ref_pattern, memory_dump):
        size = _convert_to_mb(float(match.group(3)), match.group(4))
        references.append(
            {
                "holder": match.group(1),
                "held": match.group(2),
                "size_mb": size,
            }
        )

    return references[:10]


def _find_references_tracemalloc(memory_dump: str, options: dict) -> List[dict]:
    references = []

    tb_pattern = r"File \"([^\"]+)\", line (\d+).*?(?:File \"([^\"]+)\", line (\d+))*"
    for match in re.finditer(tb_pattern, memory_dump):
        frames = []
        for i in range(1, len(match.groups()), 2):
            if match.group(i):
                frames.append(f"{match.group(i)}:{match.group(i + 1)}")
        if frames:
            references.append(
                {
                    "traceback": " -> ".join(frames),
                    "type": "allocation_site",
                }
            )

    return references[:10]


def _find_references_memray(memory_dump: str, options: dict) -> List[dict]:
    references = []

    try:
        data = json.loads(memory_dump)
        allocations = data.get("allocations", [])

        by_thread = defaultdict(list)
        for alloc in allocations:
            thread = alloc.get("thread", "main")
            by_thread[thread].append(alloc)

        for thread, allocs in by_thread.items():
            total_size = sum(alloc.get("size", 0) for alloc in allocs)
            references.append(
                {
                    "thread": thread,
                    "allocation_count": len(allocs),
                    "total_size_mb": round(_convert_to_mb(total_size, "B"), 2),
                }
            )
    except:
        pass

    return references[:10]


def _detect_leak_patterns(leaks: List[dict], tool_type: str) -> List[dict]:
    patterns = []

    for leak in leaks:
        leak_type = leak.get("type", "")
        location = leak.get("location", "")
        size = leak.get("size_mb", 0)

        if any(x in leak_type.lower() for x in ["list", "dict", "set"]):
            patterns.append(
                {
                    "pattern": "collection_accumulation",
                    "description": f"Collection type '{leak_type}' accumulating objects",
                    "severity": "high" if size > 10 else "medium",
                    "leak": leak,
                }
            )

        if "cache" in leak_type.lower() or "cache" in location.lower():
            patterns.append(
                {
                    "pattern": "cache_growth",
                    "description": "Unbounded cache growing without eviction",
                    "severity": "high",
                    "leak": leak,
                }
            )

        if "string" in leak_type.lower():
            patterns.append(
                {
                    "pattern": "string_concatenation",
                    "description": "String concatenation causing memory bloat",
                    "severity": "medium",
                    "leak": leak,
                }
            )

        if "closure" in leak_type.lower() or "function" in leak_type.lower():
            patterns.append(
                {
                    "pattern": "closure_capture",
                    "description": "Closure capturing large objects",
                    "severity": "medium",
                    "leak": leak,
                }
            )

        if "thread" in leak_type.lower():
            patterns.append(
                {
                    "pattern": "thread_local",
                    "description": "Thread-local storage not being cleaned up",
                    "severity": "high",
                    "leak": leak,
                }
            )

        if "global" in leak_type.lower():
            patterns.append(
                {
                    "pattern": "global_reference",
                    "description": "Global variable holding reference to large object",
                    "severity": "high",
                    "leak": leak,
                }
            )

    common_patterns = [
        {
            "pattern": "circular_reference",
            "description": "Objects referencing each other preventing garbage collection",
            "severity": "medium",
            "suggestion": "Use weakref for circular references",
        },
        {
            "pattern": "event_listener",
            "description": "Event listeners not being removed",
            "severity": "medium",
            "suggestion": "Remove event listeners when no longer needed",
        },
        {
            "pattern": "database_connection",
            "description": "Database connections not being closed",
            "severity": "high",
            "suggestion": "Use context managers for database connections",
        },
        {
            "pattern": "file_handle",
            "description": "File handles not being closed",
            "severity": "high",
            "suggestion": "Use context managers for file operations",
        },
    ]

    return patterns + common_patterns[:3]


def _generate_suggestions(
    leaks: List[dict], patterns: List[dict], tool_type: str
) -> List[dict]:
    suggestions = []

    for pattern in patterns:
        pattern_name = pattern.get("pattern", "")

        if pattern_name == "collection_accumulation":
            suggestions.append(
                {
                    "issue": "Collection accumulating objects",
                    "fix": "Use bounded collections (maxsize in LRU cache) or clear collections periodically",
                    "code_example": "from functools import lru_cache\n\n@lru_cache(maxsize=128)\ndef expensive_function(arg):\n    return compute(arg)",
                }
            )
        elif pattern_name == "cache_growth":
            suggestions.append(
                {
                    "issue": "Unbounded cache",
                    "fix": "Implement cache eviction policy or use LRU cache",
                    "code_example": "from functools import lru_cache\nfrom collections import OrderedDict\n\nclass LRUCache:\n    def __init__(self, capacity):\n        self.cache = OrderedDict()\n        self.capacity = capacity\n    \n    def get(self, key):\n        if key in self.cache:\n            self.cache.move_to_end(key)\n            return self.cache[key]\n        return None",
                }
            )
        elif pattern_name == "string_concatenation":
            suggestions.append(
                {
                    "issue": "String concatenation in loop",
                    "fix": "Use join() or StringIO for string building",
                    "code_example": "# Bad:\ns = ''\nfor item in items:\n    s += str(item)\n\n# Good:\ns = ''.join(str(item) for item in items)",
                }
            )
        elif pattern_name == "closure_capture":
            suggestions.append(
                {
                    "issue": "Closure capturing large objects",
                    "fix": "Avoid closures for large objects or use weakref",
                    "code_example": "import weakref\n\nclass LargeObject:\n    pass\n\nobj = LargeObject()\nweak_ref = weakref.ref(obj)",
                }
            )
        elif pattern_name == "thread_local":
            suggestions.append(
                {
                    "issue": "Thread-local storage leak",
                    "fix": "Clean up thread-local variables or use thread pools",
                    "code_example": "import threading\n\nlocal = threading.local()\n# Clean up when done:\nif hasattr(local, 'data'):\n    del local.data",
                }
            )
        elif pattern_name == "global_reference":
            suggestions.append(
                {
                    "issue": "Global variable holding large object",
                    "fix": "Use class attributes or pass objects explicitly",
                    "code_example": "# Instead of global large_data\nclass DataProcessor:\n    def __init__(self):\n        self.large_data = None\n    \n    def process(self, data):\n        self.large_data = data\n        # Process and clear\n        result = self._process()\n        self.large_data = None  # Release reference\n        return result",
                }
            )
        elif pattern_name == "circular_reference":
            suggestions.append(
                {
                    "issue": "Circular references",
                    "fix": "Use weakref or break cycles explicitly",
                    "code_example": "import weakref\n\nclass Node:\n    def __init__(self):\n        self.parent = None\n        self.children = []\n    \n    def add_child(self, child):\n        self.children.append(child)\n        child.parent = weakref.ref(self)",
                }
            )
        elif pattern_name == "event_listener":
            suggestions.append(
                {
                    "issue": "Event listeners not removed",
                    "fix": "Remove listeners when done or use weak references",
                    "code_example": "class Emitter:\n    def __init__(self):\n        self.listeners = []\n    \n    def remove_listener(self, listener):\n        if listener in self.listeners:\n            self.listeners.remove(listener)",
                }
            )
        elif pattern_name == "database_connection":
            suggestions.append(
                {
                    "issue": "Database connection leak",
                    "fix": "Use context managers for connections",
                    "code_example": "import contextlib\n\n@contextlib.contextmanager\ndef get_connection():\n    conn = create_connection()\n    try:\n        yield conn\n    finally:\n        conn.close()\n\n# Usage:\nwith get_connection() as conn:\n    conn.execute(query)",
                }
            )
        elif pattern_name == "file_handle":
            suggestions.append(
                {
                    "issue": "File handle leak",
                    "fix": "Use context managers for files",
                    "code_example": "# Instead of:\nf = open('file.txt')\n# process...\nf.close()\n\n# Use:\nwith open('file.txt') as f:\n    # process...\n# Automatically closed",
                }
            )

    for leak in leaks[:3]:
        if leak.get("severity") == "high" and not any(
            s.get("issue", "").lower() in str(leak.get("type", "")).lower()
            for s in suggestions
        ):
            suggestions.append(
                {
                    "issue": f"High memory usage: {leak.get('type', 'Unknown')}",
                    "fix": f"Investigate {leak.get('type', 'object')} for potential leaks",
                    "severity": "high",
                }
            )

    return suggestions


def _convert_to_mb(size: float, unit: str) -> float:
    unit = unit.upper()
    if unit == "B":
        return size / (1024 * 1024)
    elif unit == "KB":
        return size / 1024
    elif unit == "MB":
        return size
    elif unit == "GB":
        return size * 1024
    return size


def _calculate_severity(size_mb: float, threshold_mb: float) -> str:
    ratio = size_mb / threshold_mb if threshold_mb > 0 else 0
    if ratio > 100:
        return "critical"
    elif ratio > 50:
        return "high"
    elif ratio > 10:
        return "medium"
    else:
        return "low"


def invoke(payload: dict) -> dict:
    """
    Main entry point for MCP skill invocation.

    Expected payload format:
    {
        "memory_dump": "..." or {"file": "path/to/memory_dump.txt"},
        "options": {
            "tool_type": "heapy|tracemalloc|memray|auto",
            "threshold": 1.0,
            "top_n": 10,
        },
        "generate_report": false  // optional, generates text report
    }
    """
    memory_dump = payload.get("memory_dump", "")

    if isinstance(memory_dump, dict):
        file_path = memory_dump.get("file")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    memory_dump = f.read()
            except Exception as e:
                return {
                    "status": "error",
                    "error": f"Failed to read memory dump file: {e}",
                }
        else:
            memory_dump = json.dumps(memory_dump)

    if not memory_dump:
        return {"status": "error", "error": "No memory dump provided"}

    options = payload.get("options", {})
    result = memory_leak_detector(memory_dump, options)

    if payload.get("generate_report", False):
        result["report"] = generate_report(result)

    return {"result": result}


def generate_report(analysis: dict) -> str:
    """Generate human-readable memory leak report."""
    lines = []
    lines.append("=" * 60)
    lines.append("MEMORY LEAK ANALYSIS REPORT")
    lines.append("=" * 60)
    lines.append(f"Tool Type: {analysis.get('tool_type', 'unknown')}")
    lines.append("")

    leaks = analysis.get("leaks", [])
    if leaks:
        lines.append("DETECTED LEAKS:")
        lines.append("-" * 40)
        for i, leak in enumerate(leaks[:10], 1):
            lines.append(f"{i}. {leak.get('type', leak.get('location', 'Unknown'))}")
            lines.append(f"   Size: {leak.get('size_mb', 0):.2f} MB")
            lines.append(f"   Count: {leak.get('count', 'N/A')}")
            lines.append(f"   Severity: {leak.get('severity', 'unknown')}")
            lines.append("")

    growing = analysis.get("growing_objects", [])
    if growing:
        lines.append("GROWING OBJECTS:")
        lines.append("-" * 40)
        for obj in growing[:5]:
            lines.append(f"  Growth: {obj.get('growth_mb', 0):.2f} MB")
            if "growth_percentage" in obj:
                lines.append(f"  Percentage: {obj.get('growth_percentage', 0):.2f}%")
            lines.append("")

    suggestions = analysis.get("suggestions", [])
    if suggestions:
        lines.append("SUGGESTED FIXES:")
        lines.append("-" * 40)
        for i, suggestion in enumerate(suggestions[:5], 1):
            lines.append(f"{i}. {suggestion.get('issue', 'Unknown issue')}")
            lines.append(f"   Fix: {suggestion.get('fix', 'No fix suggested')}")
            if "code_example" in suggestion:
                lines.append(f"   Example: {suggestion['code_example'][:100]}...")
            lines.append("")

    return "\n".join(lines)


def register_skill():
    """Return skill metadata for MCP registration."""
    return {
        "name": "memory-leak-detector",
        "description": "Detect memory leaks by analyzing memory dumps from Heapy, tracemalloc, and memray - identifies growing objects, finds references, detects leak patterns, and suggests fixes",
        "version": "1.0.0",
        "domain": "PERFORMANCE",
        "capabilities": [
            "Parse Heapy memory dumps",
            "Parse tracemalloc output",
            "Parse memray JSON output",
            "Identify growing objects over time",
            "Find references holding memory",
            "Detect common leak patterns",
            "Generate fix suggestions with code examples",
            "Create human-readable reports",
        ],
        "options": {
            "tool_type": "Type of memory profiler (heapy, tracemalloc, memray, auto)",
            "threshold": "Minimum memory size in MB to report (default: 1.0)",
            "top_n": "Number of top leaks to return (default: 10)",
        },
    }


if __name__ == "__main__":
    test_heapy = """
Partition of a set of 15234 objects. Total size = 15.67 MB.
  8.45 MB: list object at 0x7f8a3c0>
  5.23 MB: dict object at 0x7f8a3d0>
  2.01 MB: str object at 0x7f8a3e0>
  1.50 MB: set object at 0x7f8a3f0>
    """

    result = memory_leak_detector(test_heapy, {"threshold": 1.0, "top_n": 5})
    print(json.dumps(result, indent=2))
