"""
Profiler Analyzer: Performance profiling analysis skill

This module provides profiler output analysis capabilities:
- Parse cProfile, py-spy, line_profiler output
- Identify performance hotspots
- Analyze call patterns
- Suggest optimizations
- Generate human-readable reports
"""

import json
import re
from collections import defaultdict
from typing import Any, Dict, List


def profiler_analyzer(profile_data: str, options: dict) -> dict:
    """
    Analyze profiler output and generate performance insights.

    Args:
        profile_data: Profiler output (cProfile, py-spy JSON, or line_profiler)
        options: Configuration options including:
            - profiler_type: "cprofile", "py-spy", "line_profiler" (auto-detected if missing)
            - threshold: Minimum time percentage to report (default: 1.0)
            - top_n: Number of hotspots to return (default: 10)
            - include_stdlib: Include standard library functions (default: False)

    Returns:
        Dictionary with analysis results containing:
            - status: "success" or "error"
            - hotspots: Top time-consuming functions
            - call_graph: Call relationship analysis
            - optimizations: Suggested optimizations
            - summary: Performance summary
    """
    try:
        options = _normalize_options(options)
        profiler_type = options.get(
            "profiler_type", _detect_profiler_type(profile_data)
        )

        if profiler_type == "cprofile":
            return _analyze_cprofile(profile_data, options)
        elif profiler_type == "py-spy":
            return _analyze_py_spy(profile_data, options)
        elif profiler_type == "line_profiler":
            return _analyze_line_profiler(profile_data, options)
        else:
            return _analyze_cprofile(profile_data, options)

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to analyze profiler output",
        }


def _normalize_options(options: dict) -> dict:
    defaults = {
        "profiler_type": "auto",
        "threshold": 1.0,
        "top_n": 10,
        "include_stdlib": False,
    }
    return {**defaults, **options}


def _detect_profiler_type(profile_data: str) -> str:
    profile_data_lower = profile_data.strip().lower()

    if profile_data.startswith("{") or profile_data.startswith("["):
        try:
            json_data = json.loads(profile_data)
            if "profiles" in json_data or "latency" in json_data:
                return "py-spy"
            if "timing" in json_data or "LineHits" in str(json_data):
                return "line_profiler"
        except:
            pass

    if "ncalls" in profile_data_lower and "tottime" in profile_data_lower:
        return "cprofile"
    if "line profiler" in profile_data_lower:
        return "line_profiler"
    if "py-spy" in profile_data_lower or "py-spy" in profile_data:
        return "py-spy"

    return "cprofile"


def _analyze_cprofile(profile_data: str, options: dict) -> dict:
    hotspots = _parse_cprofile(profile_data)
    total_time = sum(h["tottime"] for h in hotspots) if hotspots else 1

    filtered_hotspots = [
        h for h in hotspots if (h["tottime"] / total_time * 100) >= options["threshold"]
    ][: options["top_n"]]

    call_graph = _build_call_graph(hotspots)
    optimizations = _suggest_optimizations(filtered_hotspots, call_graph)
    summary = _generate_summary(filtered_hotspots, total_time, options)

    return {
        "status": "success",
        "profiler_type": "cprofile",
        "hotspots": filtered_hotspots,
        "call_graph": call_graph,
        "optimizations": optimizations,
        "summary": summary,
    }


def _parse_cprofile(profile_data: str) -> List[Dict[str, Any]]:
    lines = profile_data.strip().split("\n")
    functions = []

    header_pattern = re.compile(r"^\s*(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+(.+)$")

    for line in lines:
        line = line.strip()
        if not line or line.startswith("Ordered by:") or line.startswith("ncalls"):
            continue

        match = header_pattern.match(line)
        if match:
            ncalls = match.group(1)
            tottime = float(match.group(3))
            cumtime = float(match.group(4))
            func_name = match.group(5).strip()

            if (
                func_name
                and not func_name.startswith("{")
                and not func_name.startswith("<")
            ):
                functions.append(
                    {
                        "function": func_name,
                        "ncalls": int(ncalls),
                        "tottime": round(tottime, 4),
                        "cumtime": round(cumtime, 4),
                        "tottime_percent": 0.0,
                        "cumtime_percent": 0.0,
                    }
                )

    return functions


def _analyze_py_spy(profile_data: str, options: dict) -> dict:
    try:
        data = json.loads(profile_data)
    except json.JSONDecodeError:
        return {"status": "error", "error": "Invalid JSON format"}

    events = data.get("profiles", [])
    if not events:
        events = data.get("latency", [])

    function_times = defaultdict(lambda: {"time": 0, "count": 0})

    for event in events:
        if isinstance(event, dict):
            for key, value in event.items():
                if isinstance(value, (int, float)):
                    function_times[key]["time"] += value
                    function_times[key]["count"] += 1

    hotspots = []
    total_time = sum(v["time"] for v in function_times.values())

    for func, stats in function_times.items():
        hotspots.append(
            {
                "function": func,
                "tottime": round(stats["time"], 4),
                "ncalls": stats["count"],
                "tottime_percent": round(stats["time"] / total_time * 100, 2)
                if total_time > 0
                else 0,
            }
        )

    hotspots.sort(key=lambda x: x["tottime"], reverse=True)
    filtered_hotspots = [
        h for h in hotspots if h["tottime_percent"] >= options["threshold"]
    ][: options["top_n"]]

    call_graph = _build_call_graph_from_py_spy(hotspots)
    optimizations = _suggest_optimizations(filtered_hotspots, call_graph)
    summary = _generate_summary(filtered_hotspots, total_time, options)

    return {
        "status": "success",
        "profiler_type": "py-spy",
        "hotspots": filtered_hotspots,
        "call_graph": call_graph,
        "optimizations": optimizations,
        "summary": summary,
    }


def _analyze_line_profiler(profile_data: str, options: dict) -> dict:
    lines = profile_data.strip().split("\n")
    hotspots = []
    current_file = ""

    line_pattern = re.compile(r"^(\d+):\s*(.+)$")
    file_pattern = re.compile(r"^File:\s*(.+)$")
    timer_pattern = re.compile(r"Timer:\s*(.+)$")

    total_time = 0.0

    for line in lines:
        file_match = file_pattern.match(line)
        if file_match:
            current_file = file_match.group(1)
            continue

        timer_match = timer_pattern.match(line)
        if timer_match:
            continue

        line_match = line_pattern.match(line)
        if line_match and current_file:
            line_num = int(line_match.group(1))
            code = line_match.group(2).strip()
            time_match = re.search(r"([\d.]+)\s*s", code)

            if time_match:
                time_val = float(time_match.group(1))
                total_time += time_val
                hotspots.append(
                    {
                        "file": current_file,
                        "line": line_num,
                        "code": code.split("s")[0].strip() if "s" in code else code,
                        "tottime": round(time_val, 4),
                    }
                )

    for h in hotspots:
        h["tottime_percent"] = (
            round(h["tottime"] / total_time * 100, 2) if total_time > 0 else 0
        )

    hotspots.sort(key=lambda x: x["tottime"], reverse=True)
    filtered_hotspots = [
        h for h in hotspots if h["tottime_percent"] >= options["threshold"]
    ][: options["top_n"]]

    optimizations = _suggest_line_optimizations(filtered_hotspots)
    summary = {
        "total_time": round(total_time, 4),
        "hotspot_count": len(filtered_hotspots),
        "file": current_file,
        "profiler_type": "line_profiler",
    }

    return {
        "status": "success",
        "profiler_type": "line_profiler",
        "hotspots": filtered_hotspots,
        "call_graph": {},
        "optimizations": optimizations,
        "summary": summary,
    }


def _build_call_graph(functions: List[Dict[str, Any]]) -> Dict[str, Any]:
    graph = {
        "nodes": [],
        "edges": [],
        "max_depth": 0,
    }

    func_names = set()
    for func in functions:
        name = func.get("function", "")
        func_names.add(name)

        parts = name.split("->")
        if len(parts) > 1:
            caller = parts[0].strip()
            callee = parts[-1].strip()
            depth = len(parts) - 1
            graph["max_depth"] = max(graph["max_depth"], depth)

            if caller not in [e["caller"] for e in graph["edges"]]:
                graph["edges"].append(
                    {
                        "caller": caller,
                        "callee": callee,
                        "count": func.get("ncalls", 1),
                    }
                )

    for name in func_names:
        graph["nodes"].append({"id": name, "label": name})

    return graph


def _build_call_graph_from_py_spy(functions: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "nodes": [
            {"id": f["function"], "label": f["function"]} for f in functions[:20]
        ],
        "edges": [],
        "max_depth": 1,
    }


def _suggest_optimizations(
    hotspots: List[Dict[str, Any]], call_graph: Dict[str, Any]
) -> List[Dict[str, Any]]:
    optimizations = []

    for _i, hotspot in enumerate(hotspots):
        func_name = hotspot.get("function", "")
        tottime = hotspot.get("tottime", 0)
        tottime_pct = hotspot.get("tottime_percent", 0)

        suggestions = []

        if tottime_pct > 20:
            suggestions.append(
                {
                    "priority": "high",
                    "title": f"Critical hotspot: {func_name}",
                    "description": f"This function consumes {tottime_pct:.1f}% of total execution time ({tottime:.3f}s). Consider optimizing or refactoring.",
                    "actions": [
                        "Profile at line level to identify specific slow lines",
                        "Consider caching results if called repeatedly",
                        "Check for unnecessary computations in the hot path",
                    ],
                }
            )

        if "loop" in func_name.lower() or any("for " in f for f in [func_name]):
            suggestions.append(
                {
                    "priority": "medium",
                    "title": "Loop optimization opportunity",
                    "description": "This function appears to contain loops. Consider loop optimization techniques.",
                    "actions": [
                        "Move invariant computations outside loops",
                        "Consider list comprehensions vs explicit loops",
                        "Use iterators for large datasets",
                    ],
                }
            )

        if "sort" in func_name.lower() or "sorted" in func_name.lower():
            suggestions.append(
                {
                    "priority": "medium",
                    "title": "Sorting optimization",
                    "description": "Sorting operations detected. Consider using more efficient algorithms.",
                    "actions": [
                        "Use key function instead of cmp",
                        "Consider sorted() vs sort() for your use case",
                        "Check if data is already partially sorted",
                    ],
                }
            )

        if (
            "json" in func_name.lower()
            or "loads" in func_name.lower()
            or "dumps" in func_name.lower()
        ):
            suggestions.append(
                {
                    "priority": "medium",
                    "title": "JSON parsing optimization",
                    "description": "JSON serialization/deserialization detected.",
                    "actions": [
                        "Consider caching parsed results",
                        "Use orjson for faster JSON processing",
                        "Batch operations when possible",
                    ],
                }
            )

        if (
            "db" in func_name.lower()
            or "query" in func_name.lower()
            or "sql" in func_name.lower()
        ):
            suggestions.append(
                {
                    "priority": "high",
                    "title": "Database query optimization",
                    "description": "Database operations detected. Query optimization may yield significant gains.",
                    "actions": [
                        "Add appropriate indexes",
                        "Use query optimization (EXPLAIN)",
                        "Consider connection pooling",
                        "Batch queries where possible",
                    ],
                }
            )

        if (
            "requests" in func_name.lower()
            or "http" in func_name.lower()
            or "urllib" in func_name.lower()
        ):
            suggestions.append(
                {
                    "priority": "high",
                    "title": "Network call optimization",
                    "description": "Network I/O detected. Consider async or connection pooling.",
                    "actions": [
                        "Use connection pooling (requests.Session)",
                        "Consider async requests",
                        "Implement caching for repeated calls",
                    ],
                }
            )

        ncalls = hotspot.get("ncalls", 0)
        if ncalls > 1000 and tottime > 0.1:
            suggestions.append(
                {
                    "priority": "high",
                    "title": "High call frequency",
                    "description": f"Function called {ncalls} times. Consider memoization or caching.",
                    "actions": [
                        "Implement memoization with functools.lru_cache",
                        "Batch operations when possible",
                        "Consider lazy evaluation",
                    ],
                }
            )

        if suggestions:
            optimizations.extend(suggestions)
        else:
            optimizations.append(
                {
                    "priority": "low",
                    "title": f"Minor optimization: {func_name}",
                    "description": f"Function takes {tottime_pct:.1f}% of time. Profile line-by-line for details.",
                    "actions": [
                        "Review function implementation",
                        "Consider algorithmic improvements",
                    ],
                }
            )

    optimizations.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}[x["priority"]])

    return optimizations[:10]


def _suggest_line_optimizations(hotspots: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    optimizations = []

    for hotspot in hotspots:
        code = hotspot.get("code", "").lower()

        if "for " in code or "while " in code:
            optimizations.append(
                {
                    "priority": "high",
                    "title": f"Line {hotspot['line']}: Loop optimization",
                    "description": f"Code: {hotspot['code'][:50]}",
                    "actions": [
                        "Move invariant computations outside loop",
                        "Consider vectorization with NumPy",
                    ],
                }
            )

        if "re.compile" in code or "re.match" in code or "re.search" in code:
            optimizations.append(
                {
                    "priority": "medium",
                    "title": f"Line {hotspot['line']}: Regex optimization",
                    "description": "Regex operations detected at line level.",
                    "actions": [
                        "Pre-compile regular expressions",
                        "Use simpler patterns when possible",
                    ],
                }
            )

        if "+=" in code or ".append" in code:
            optimizations.append(
                {
                    "priority": "low",
                    "title": f"Line {hotspot['line']}: String/List operation",
                    "description": "String concatenation or list operation.",
                    "actions": [
                        "Use list join for string building",
                        "Consider pre-allocating list size",
                    ],
                }
            )

    return optimizations[:10]


def _generate_summary(
    hotspots: List[Dict[str, Any]], total_time: float, options: dict
) -> Dict[str, Any]:
    total_hotspot_time = sum(h.get("tottime", 0) for h in hotspots)

    summary = {
        "total_time_analyzed": round(total_time, 4),
        "hotspot_time": round(total_hotspot_time, 4),
        "hotspot_coverage": round(total_hotspot_time / total_time * 100, 2)
        if total_time > 0
        else 0,
        "hotspot_count": len(hotspots),
        "threshold_used": options.get("threshold", 1.0),
        "top_function": hotspots[0].get("function", "N/A") if hotspots else "N/A",
        "top_function_time": hotspots[0].get("tottime", 0) if hotspots else 0,
        "recommendation": _generate_recommendation(hotspots, total_time),
    }

    return summary


def _generate_recommendation(hotspots: List[Dict[str, Any]], total_time: float) -> str:
    if not hotspots:
        return "No hotspots detected. Application appears well-optimized."

    top_hotspot = hotspots[0]
    top_time_pct = top_hotspot.get("tottime_percent", 0)
    top_func = top_hotspot.get("function", "unknown")

    if top_time_pct > 30:
        return f"Focus on optimizing '{top_func}' which takes {top_time_pct:.1f}% of execution time. This single function is the primary performance bottleneck."
    elif top_time_pct > 15:
        return f"The top hotspot '{top_func}' takes {top_time_pct:.1f}% of time. Review and optimize this function first, then address secondary hotspots."
    elif len(hotspots) > 5:
        return f"Multiple hotspots detected. Consider addressing the top {min(3, len(hotspots))} functions for cumulative performance gains."
    else:
        return "Performance is relatively balanced across functions. Consider algorithmic improvements for top hotspots."


def _calculate_cumulative_percentage(
    hotspots: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    total = sum(h.get("tottime", 0) for h in hotspots)
    cumulative = 0

    for h in hotspots:
        cumulative += h.get("tottime", 0)
        h["cumulative_percent"] = round(cumulative / total * 100, 2) if total > 0 else 0

    return hotspots


def generate_report(analysis_result: dict) -> str:
    """
    Generate a human-readable performance report from analysis results.

    Args:
        analysis_result: Result from profiler_analyzer function

    Returns:
        Formatted text report
    """
    if analysis_result.get("status") != "success":
        return f"Error: {analysis_result.get('message', 'Unknown error')}"

    lines = []
    lines.append("=" * 60)
    lines.append("PERFORMANCE ANALYSIS REPORT")
    lines.append("=" * 60)
    lines.append("")

    summary = analysis_result.get("summary", {})
    lines.append("SUMMARY")
    lines.append("-" * 40)
    lines.append(f"Total Time Analyzed: {summary.get('total_time_analyzed', 0):.4f}s")
    lines.append(f"Hotspot Time: {summary.get('hotspot_time', 0):.4f}s")
    lines.append(f"Hotspot Coverage: {summary.get('hotspot_coverage', 0):.1f}%")
    lines.append(f"Top Function: {summary.get('top_function', 'N/A')}")
    lines.append(f"Top Function Time: {summary.get('top_function_time', 0):.4f}s")
    lines.append("")
    lines.append(f"Recommendation: {summary.get('recommendation', '')}")
    lines.append("")

    hotspots = analysis_result.get("hotspots", [])
    if hotspots:
        lines.append("TOP HOTSPOTS")
        lines.append("-" * 40)
        for i, h in enumerate(hotspots[:10], 1):
            func = h.get("function", "unknown")[:50]
            tottime = h.get("tottime", 0)
            pct = h.get("tottime_percent", 0)
            ncalls = h.get("ncalls", 0)
            lines.append(f"{i:2}. {func}")
            lines.append(f"    Time: {tottime:.4f}s ({pct:.1f}%) | Calls: {ncalls}")
        lines.append("")

    optimizations = analysis_result.get("optimizations", [])
    if optimizations:
        lines.append("OPTIMIZATION SUGGESTIONS")
        lines.append("-" * 40)
        for i, opt in enumerate(optimizations[:5], 1):
            priority = opt.get("priority", "low").upper()
            title = opt.get("title", "Optimization")
            lines.append(f"{i}. [{priority}] {title}")
            desc = opt.get("description", "")
            if desc:
                lines.append(f"   {desc[:60]}...")
        lines.append("")

    lines.append("=" * 60)

    return "\n".join(lines)


def invoke(payload: dict) -> dict:
    """
    Main entry point for MCP skill invocation.

    Expected payload format:
    {
        "profile_data": "..." or {"file": "path/to/profile.dat"},
        "options": {
            "profiler_type": "cprofile|py-spy|line_profiler|auto",
            "threshold": 1.0,
            "top_n": 10,
            "include_stdlib": false,
        },
        "generate_report": false  // optional, generates text report
    }
    """
    profile_data = payload.get("profile_data", "")

    if isinstance(profile_data, dict):
        file_path = profile_data.get("file")
        if file_path:
            try:
                with open(file_path, encoding="utf-8") as f:
                    profile_data = f.read()
            except Exception as e:
                return {"status": "error", "error": f"Failed to read profile file: {e}"}
        else:
            profile_data = json.dumps(profile_data)

    if not profile_data:
        return {"status": "error", "error": "No profile data provided"}

    options = payload.get("options", {})
    result = profiler_analyzer(profile_data, options)

    if payload.get("generate_report", False):
        result["report"] = generate_report(result)

    return {"result": result}


def register_skill():
    """Return skill metadata for MCP registration."""
    return {
        "name": "profiler-analyzer",
        "description": "Analyze profiler output from cProfile, py-spy, and line_profiler to identify hotspots, call patterns, and suggest optimizations",
        "version": "1.0.0",
        "domain": "PERFORMANCE",
        "capabilities": [
            "Parse cProfile pstats output",
            "Parse py-spy JSON output",
            "Parse line_profiler text output",
            "Identify time-consuming function hotspots",
            "Build call relationship graphs",
            "Generate optimization suggestions",
            "Create human-readable performance reports",
        ],
        "options": {
            "profiler_type": "Type of profiler output (cprofile, py-spy, line_profiler, auto)",
            "threshold": "Minimum time percentage to include in results (default: 1.0)",
            "top_n": "Number of hotspots to return (default: 10)",
            "include_stdlib": "Include standard library functions (default: False)",
        },
    }


if __name__ == "__main__":
    test_cprofile = """         10000 function calls in 0.135 seconds
    
      Ordered by: cumulative time
    
      ncalls  tottime  percall  cumtime  percall filename:lineno(function)
            1    0.001    0.001    0.135    0.135 profile_test.py:1(<module>)
            1    0.010    0.010    0.120    0.120 profile_test.py:5(process_data)
         1000    0.050    0.000    0.080    0.000 profile_test.py:10(heavy_computation)
         2000    0.030    0.000    0.030    0.000 {method 'append' of 'list' objects}
         1000    0.010    0.000    0.020    0.000 profile_test.py:15(helper_func)
    """

    result = profiler_analyzer(test_cprofile, {"top_n": 5})
    print(json.dumps(result, indent=2))
