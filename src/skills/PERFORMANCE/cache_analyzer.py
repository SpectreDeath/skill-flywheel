"""
Cache Analyzer: Caching effectiveness analysis skill

This module provides cache analysis capabilities:
- Detect cache decorators, Redis, memcached usage
- Analyze cache patterns (hit/miss, TTL, invalidation)
- Identify issues (cache thrashing, too small, wrong TTL)
- Suggest improvements and better strategies
- Calculate cache efficiency metrics
"""

import re
import ast
from typing import Dict, List, Any, Optional, Set, Tuple
from collections import defaultdict


def cache_analyzer(code: str, options: dict) -> dict:
    """
    Analyze Python code for caching effectiveness.

    Args:
        code: Python code with caching implementations
        options: Configuration options including:
            - detection_level: "basic", "standard", or "deep" (default: "standard")
            - check_performance: Whether to analyze performance implications

    Returns:
        Dictionary with analysis results containing:
            - status: "success" or "error"
            - caches: Detected cache usages
            - patterns: Cache pattern analysis
            - issues: Detected problems
            - suggestions: Improvement suggestions
            - metrics: Cache efficiency metrics
    """
    try:
        options = _normalize_options(options)
        caches = _detect_caches(code, options)
        patterns = _analyze_patterns(code, caches, options)
        issues = _identify_issues(caches, patterns, options)
        suggestions = _generate_suggestions(caches, patterns, issues, options)
        metrics = _calculate_metrics(caches, patterns, options)

        return {
            "status": "success",
            "caches": caches,
            "patterns": patterns,
            "issues": issues,
            "suggestions": suggestions,
            "metrics": metrics,
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to analyze cache implementation",
        }


def _normalize_options(options: dict) -> dict:
    defaults = {
        "detection_level": "standard",
        "check_performance": True,
    }
    return {**defaults, **options}


def _detect_caches(code: str, options: dict) -> List[dict]:
    caches = []
    detection_level = options.get("detection_level", "standard")

    caches.extend(_detect_decorator_caches(code))
    caches.extend(_detect_redis_caches(code))
    caches.extend(_detect_memcached_caches(code))
    caches.extend(_detect_custom_caches(code))

    if detection_level in ("standard", "deep"):
        caches.extend(_detect_django_caches(code))
        caches.extend(_detect_flask_caches(code))
        caches.extend(_detect_cachalot_caches(code))

    if detection_level == "deep":
        caches.extend(_detect_cache_methods(code))
        caches.extend(_detect_cache_variables(code))

    return caches


def _detect_decorator_caches(code: str) -> List[dict]:
    caches = []

    lru_pattern = r"@lru_cache(?:\(.*?\))?|@functools\.lru_cache(?:\(.*?\))?"
    for match in re.finditer(lru_pattern, code):
        line_num = code[: match.start()].count("\n") + 1
        caches.append(
            {
                "type": "lru_cache",
                "location": f"line {line_num}",
                "library": "functools",
                "severity": "info",
                "details": "LRU cache from functools module",
            }
        )

    cache_pattern = r"@cache(?:\(.*?\))?|@functools\.cache(?:\(.*?\))?"
    for match in re.finditer(cache_pattern, code):
        line_num = code[: match.start()].count("\n") + 1
        caches.append(
            {
                "type": "cache",
                "location": f"line {line_num}",
                "library": "functools",
                "severity": "info",
                "details": "Unbounded cache from functools module",
            }
        )

    cached_pattern = r"@cached(?:\(.*?\))?"
    for match in re.finditer(cached_pattern, code):
        line_num = code[: match.start()].count("\n") + 1
        caches.append(
            {
                "type": "cached",
                "location": f"line {line_num}",
                "library": "django",
                "severity": "info",
                "details": "Django cached decorator",
            }
        )

    cache_page_pattern = r"@cache_page(?:\(.*?\))?"
    for match in re.finditer(cache_page_pattern, code):
        line_num = code[: match.start()].count("\n") + 1
        caches.append(
            {
                "type": "cache_page",
                "location": f"line {line_num}",
                "library": "django",
                "severity": "info",
                "details": "Django view caching decorator",
            }
        )

    return caches


def _detect_redis_caches(code: str) -> List[dict]:
    caches = []

    redis_patterns = [
        (r"redis\.Redis\(", "redis.Redis"),
        (r"StrictRedis\(", "redis.StrictRedis"),
        (r"Redis\.from_url\(", "Redis.from_url"),
        (r"Redis\(.*?\)", "redis.Redis"),
    ]

    for pattern, name in redis_patterns:
        for match in re.finditer(pattern, code):
            line_num = code[: match.start()].count("\n") + 1
            caches.append(
                {
                    "type": "redis",
                    "location": f"line {line_num}",
                    "library": "redis-py",
                    "severity": "info",
                    "details": f"Redis client: {name}",
                }
            )

    if "redis" in code.lower():
        redis_set_pattern = r"\.set\(['\"](.+?)['\"]"
        for match in re.finditer(redis_set_pattern, code):
            line_num = code[: match.start()].count("\n") + 1
            caches.append(
                {
                    "type": "redis_set",
                    "location": f"line {line_num}",
                    "library": "redis-py",
                    "severity": "info",
                    "details": f"Redis set operation for key: {match.group(1)}",
                }
            )

    return caches


def _detect_memcached_caches(code: str) -> List[dict]:
    caches = []

    memcached_patterns = [
        (r"memcache\.Client\(", "python-memcached"),
        (r"pymemcache\.Client\(", "pymemcache"),
        (r"Client\(['\"].*?['\"]\).*?memcache", "memcache"),
    ]

    for pattern, name in memcached_patterns:
        for match in re.finditer(pattern, code):
            line_num = code[: match.start()].count("\n") + 1
            caches.append(
                {
                    "type": "memcached",
                    "location": f"line {line_num}",
                    "library": name,
                    "severity": "info",
                    "details": f"Memcached client: {name}",
                }
            )

    return caches


def _detect_custom_caches(code: str) -> List[dict]:
    caches = []

    class_pattern = r"class\s+(\w*[Cc]ache\w*)\s*:"
    for match in re.finditer(class_pattern, code):
        class_name = match.group(1)
        line_num = code[: match.start()].count("\n") + 1
        caches.append(
            {
                "type": "custom_cache_class",
                "location": f"line {line_num}",
                "library": "custom",
                "severity": "info",
                "details": f"Custom cache class: {class_name}",
            }
        )

    dict_cache_pattern = r"(\w+)\s*=\s*\{\}"
    for match in re.finditer(dict_cache_pattern, code):
        var_name = match.group(1)
        if "cache" in var_name.lower():
            line_num = code[: match.start()].count("\n") + 1
            caches.append(
                {
                    "type": "dict_cache",
                    "location": f"line {line_num}",
                    "library": "builtin",
                    "severity": "warning",
                    "details": f"Dictionary used as cache: {var_name}",
                }
            )

    return caches


def _detect_django_caches(code: str) -> List[dict]:
    caches = []

    django_cache_patterns = [
        (r"from django\.core\.cache import cache", "django.core.cache"),
        (r"from django\.core\.cache import caches", "django.core.cache.caches"),
        (r"cache\.(get|set|delete|clear)", "django cache operations"),
        (r"caches\[['\"]", "django multiple caches"),
    ]

    for pattern, name in django_cache_patterns:
        if re.search(pattern, code):
            caches.append(
                {
                    "type": "django_cache",
                    "location": "import/usage",
                    "library": "django",
                    "severity": "info",
                    "details": f"Django caching: {name}",
                }
            )

    return caches


def _detect_flask_caches(code: str) -> List[dict]:
    caches = []

    flask_cache_patterns = [
        (r"from flask_caching import Cache", "flask-caching"),
        (r"Cache\(.*?\)", "flask-caching initialization"),
    ]

    for pattern, name in flask_cache_patterns:
        for match in re.finditer(pattern, code):
            line_num = code[: match.start()].count("\n") + 1
            caches.append(
                {
                    "type": "flask_cache",
                    "location": f"line {line_num}",
                    "library": "flask-caching",
                    "severity": "info",
                    "details": f"Flask caching: {name}",
                }
            )

    return caches


def _detect_cachalot_caches(code: str) -> List[dict]:
    caches = []

    if "cachalot" in code.lower() or "django-cachalot" in code.lower():
        caches.append(
            {
                "type": "cachalot",
                "location": "import/usage",
                "library": "django-cachalot",
                "severity": "info",
                "details": "Automatic ORM caching via cachalot",
            }
        )

    return caches


def _detect_cache_methods(code: str) -> List[dict]:
    caches = []

    method_patterns = [
        r"def\s+(get|set|delete|clear|invalidate|evict)_\w*(?:cache)?\(",
        r"def\s+\w*cache\w*\(",
    ]

    for pattern in method_patterns:
        for match in re.finditer(pattern, code):
            method_name = match.group(0).strip()
            line_num = code[: match.start()].count("\n") + 1
            caches.append(
                {
                    "type": "cache_method",
                    "location": f"line {line_num}",
                    "library": "custom",
                    "severity": "info",
                    "details": f"Cache method: {method_name}",
                }
            )

    return caches


def _detect_cache_variables(code: str) -> List[dict]:
    caches = []

    patterns = [
        r"(CACHE|Cache|TTL|ttl)\s*=\s*",
        r"(CACHE_TTL|CACHE_TIMEOUT)\s*=\s*",
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, code):
            var_name = match.group(1)
            line_num = code[: match.start()].count("\n") + 1
            value_match = re.search(
                rf"{var_name}\s*=\s*(.+?)(?:\n|#)", code[match.start() :]
            )
            value = value_match.group(1).strip() if value_match else "unknown"
            caches.append(
                {
                    "type": "cache_config",
                    "location": f"line {line_num}",
                    "library": "config",
                    "severity": "info",
                    "details": f"Cache config: {var_name} = {value}",
                }
            )

    return caches


def _analyze_patterns(code: str, caches: List[dict], options: dict) -> List[dict]:
    patterns = []

    if not caches:
        return [
            {
                "pattern": "no_cache_detected",
                "description": "No caching implementation detected",
                "severity": "medium",
            }
        ]

    patterns.extend(_detect_hit_miss_patterns(code))
    patterns.extend(_detect_ttl_patterns(code))
    patterns.extend(_detect_invalidation_patterns(code))
    patterns.extend(_detect_key_patterns(code))
    patterns.extend(_detect_serialization_patterns(code))

    return patterns


def _detect_hit_miss_patterns(code: str) -> List[dict]:
    patterns = []

    hit_miss_patterns = [
        (r"\.get\(['\"].*?['\"]\)", "cache_get"),
        (r"cache\.get", "django_cache_get"),
    ]

    has_get = False
    has_set = False

    for pattern, name in hit_miss_patterns:
        if re.search(pattern, code):
            has_get = True
            break

    if re.search(r"\.set\(|cache\.set", code):
        has_set = True

    if has_get and not has_set:
        patterns.append(
            {
                "pattern": "read_only_cache",
                "description": "Cache appears to be read-only with no explicit writes",
                "severity": "low",
            }
        )

    if re.search(r"hit_rate|cache_hit|cache_miss", code, re.IGNORECASE):
        patterns.append(
            {
                "pattern": "hit_miss_tracking",
                "description": "Code tracks cache hit/miss metrics",
                "severity": "info",
            }
        )

    return patterns


def _detect_ttl_patterns(code: str) -> List[dict]:
    patterns = []

    ttl_patterns = [
        r"ttl\s*=\s*(\d+)",
        r"timeout\s*=\s*(\d+)",
        r"expire\s*=\s*(\d+)",
        r"CACHE_TTL\s*=\s*(\d+)",
        r"@lru_cache\(maxsize=(\d+)\)",
    ]

    has_ttl = False
    for pattern in ttl_patterns:
        if re.search(pattern, code):
            has_ttl = True
            break

    if not has_ttl:
        patterns.append(
            {
                "pattern": "no_ttl",
                "description": "No TTL/expiration detected - cache entries never expire",
                "severity": "high",
            }
        )

    short_ttl = r"timeout\s*=\s*(\d+)\b(?!\d)"
    for match in re.finditer(short_ttl, code):
        ttl_value = int(match.group(1))
        if ttl_value < 60:
            patterns.append(
                {
                    "pattern": "short_ttl",
                    "description": f"Very short TTL ({ttl_value} seconds) may cause cache thrashing",
                    "severity": "medium",
                    "details": f"TTL value: {ttl_value}s",
                }
            )

    return patterns


def _detect_invalidation_patterns(code: str) -> List[dict]:
    patterns = []

    invalidation_patterns = [
        (r"\.delete\(", "delete"),
        (r"\.clear\(", "clear"),
        (r"\.invalidate\(", "invalidate"),
        (r"\.evict\(", "evict"),
        (r"cache\.clear", "django_clear"),
    ]

    has_invalidation = False
    for pattern, name in invalidation_patterns:
        if re.search(pattern, code):
            has_invalidation = True
            break

    if not has_invalidation:
        patterns.append(
            {
                "pattern": "no_invalidation",
                "description": "No cache invalidation mechanism detected",
                "severity": "high",
                "details": "Cache entries cannot be explicitly invalidated",
            }
        )

    if re.search(r"delete.*for.*in|for.*in.*delete", code):
        patterns.append(
            {
                "pattern": "bulk_invalidation",
                "description": "Bulk cache invalidation detected",
                "severity": "low",
            }
        )

    return patterns


def _detect_key_patterns(code: str) -> List[dict]:
    patterns = []

    key_pattern = r"['\"](.+?)['\"]\s*(?:\)|,|\.)"
    keys = set()
    for match in re.finditer(key_pattern, code):
        key = match.group(1)
        if len(key) > 100:
            keys.add(key[:20] + "...")

    if len(keys) > 10:
        patterns.append(
            {
                "pattern": "many_keys",
                "description": f"Many cache keys detected ({len(keys)}+) - check for key explosion",
                "severity": "medium",
            }
        )

    if re.search(r"user\.|session\.|request\.", code):
        patterns.append(
            {
                "pattern": "user_based_keys",
                "description": "User/session-based cache keys detected",
                "severity": "info",
                "details": "May lead to cache fragmentation per user",
            }
        )

    return patterns


def _detect_serialization_patterns(code: str) -> List[dict]:
    patterns = []

    serializers = [
        (r"pickle\.", "pickle"),
        (r"json\.dumps", "json"),
        (r"msgpack\.", "msgpack"),
        (r"orjson\.", "orjson"),
        (r"ujson\.", "ujson"),
    ]

    for pattern, name in serializers:
        if re.search(pattern, code):
            patterns.append(
                {
                    "pattern": "serialization",
                    "description": f"Using {name} for serialization",
                    "severity": "info",
                    "details": f"Serialization method: {name}",
                }
            )

    return patterns


def _identify_issues(
    caches: List[dict], patterns: List[dict], options: dict
) -> List[dict]:
    issues = []

    cache_types = [c.get("type") for c in caches]

    if "cache" in cache_types and "lru_cache" not in cache_types:
        issues.append(
            {
                "issue": "unbounded_cache",
                "description": "Using unbounded @cache decorator - no size limit",
                "severity": "high",
                "suggestion": "Use @lru_cache(maxsize=N) to limit cache size",
            }
        )

    if "dict_cache" in cache_types:
        issues.append(
            {
                "issue": "dict_cache_usage",
                "description": "Using plain dictionary as cache without eviction",
                "severity": "high",
                "suggestion": "Use collections.OrderedDict with maxsize or functools.lru_cache",
            }
        )

    if any(p.get("pattern") == "no_ttl" for p in patterns):
        issues.append(
            {
                "issue": "missing_ttl",
                "description": "Cache entries have no expiration time",
                "severity": "high",
                "suggestion": "Add TTL to prevent stale data accumulation",
            }
        )

    if any(p.get("pattern") == "no_invalidation" for p in patterns):
        issues.append(
            {
                "issue": "no_invalidation_strategy",
                "description": "No cache invalidation mechanism found",
                "severity": "medium",
                "suggestion": "Implement cache invalidation for data updates",
            }
        )

    if any(p.get("pattern") == "short_ttl" for p in patterns):
        issues.append(
            {
                "issue": "short_ttl_issue",
                "description": "Very short TTL may cause excessive cache misses",
                "severity": "medium",
                "suggestion": "Consider increasing TTL based on data update frequency",
            }
        )

    if "redis" in cache_types and "memcached" in cache_types:
        issues.append(
            {
                "issue": "multiple_cache_systems",
                "description": "Using both Redis and Memcached - may cause inconsistency",
                "severity": "low",
                "suggestion": "Consider using a single cache backend",
            }
        )

    if any(p.get("pattern") == "read_only_cache" for p in patterns):
        issues.append(
            {
                "issue": "read_only_cache",
                "description": "Cache is read but never explicitly written to",
                "severity": "low",
                "suggestion": "Ensure cache is properly populated on cache miss",
            }
        )

    if "custom_cache_class" in cache_types:
        class_count = cache_types.count("custom_cache_class")
        if class_count > 3:
            issues.append(
                {
                    "issue": "multiple_custom_caches",
                    "description": f"{class_count} custom cache classes found - consider using a shared cache",
                    "severity": "low",
                }
            )

    return issues


def _generate_suggestions(
    caches: List[dict], patterns: List[dict], issues: List[dict], options: dict
) -> List[dict]:
    suggestions = []
    cache_types = [c.get("type") for c in caches]

    suggestions.extend(
        [
            {
                "issue": "Use LRU cache with size limit",
                "fix": "Replace @cache with @lru_cache(maxsize=128) to bound memory usage",
                "code_example": "from functools import lru_cache\n\n@lru_cache(maxsize=128)\ndef expensive_function(arg):\n    return compute(arg)",
            },
            {
                "issue": "Add TTL to cache entries",
                "fix": "Configure expiration time for cache entries",
                "code_example": "cache.set('key', value, timeout=300)  # 5 minutes",
            },
            {
                "issue": "Implement cache invalidation",
                "fix": "Add invalidation on data updates",
                "code_example": "def update_data(key, value):\n    db.update(key, value)\n    cache.delete(key)",
            },
        ]
    )

    if "redis" in cache_types:
        suggestions.append(
            {
                "issue": "Consider Redis optimizations",
                "fix": "Use Redis pipelines for batch operations",
                "code_example": "pipe = redis.pipeline()\npipe.set('key1', 'value1')\npipe.set('key2', 'value2')\npipe.execute()",
            }
        )

    if "dict_cache" in cache_types:
        suggestions.append(
            {
                "issue": "Replace dict cache with proper LRU",
                "fix": "Use OrderedDict-based LRU or functools.lru_cache",
                "code_example": "from functools import lru_cache\nfrom collections import OrderedDict\n\nclass LRUCache:\n    def __init__(self, capacity):\n        self.cache = OrderedDict()\n        self.capacity = capacity\n    \n    def get(self, key):\n        if key in self.cache:\n            self.cache.move_to_end(key)\n            return self.cache[key]\n        return None",
            }
        )

    for issue in issues:
        issue_type = issue.get("issue")
        if issue_type == "no_ttl":
            suggestions.append(
                {
                    "issue": "Add TTL configuration",
                    "fix": "Set expiration times for all cache entries",
                    "code_example": "CACHE_TTL = 300  # 5 minutes in settings",
                }
            )
        elif issue_type == "no_invalidation_strategy":
            suggestions.append(
                {
                    "issue": "Implement cache invalidation",
                    "fix": "Add invalidation on data modifications",
                    "code_example": "def invalidate_user_cache(user_id):\n    cache.delete(f'user:{user_id}')",
                }
            )
        elif issue_type == "short_ttl_issue":
            suggestions.append(
                {
                    "issue": "Optimize TTL value",
                    "fix": "Match TTL to data update frequency",
                    "code_example": "# For data updated every hour:\nCACHE_TTL = 1800  # 30 minutes",
                }
            )

    return suggestions


def _calculate_metrics(
    caches: List[dict], patterns: List[dict], options: dict
) -> Dict[str, Any]:
    metrics = {}

    cache_types = [c.get("type") for c in caches]

    efficiency_score = 100

    if not caches:
        efficiency_score = 0
    else:
        if "lru_cache" in cache_types:
            efficiency_score -= 10
        if "cache" in cache_types:
            efficiency_score -= 20
        if "dict_cache" in cache_types:
            efficiency_score -= 30

        if any(p.get("pattern") == "no_ttl" for p in patterns):
            efficiency_score -= 25
        if any(p.get("pattern") == "no_invalidation" for p in patterns):
            efficiency_score -= 20
        if any(p.get("pattern") == "short_ttl" for p in patterns):
            efficiency_score -= 15
        if any(p.get("pattern") == "hit_miss_tracking" for p in patterns):
            efficiency_score += 10

    efficiency_score = max(0, min(100, efficiency_score))

    metrics["efficiency_score"] = efficiency_score
    metrics["cache_types_detected"] = list(set(cache_types))
    metrics["total_cache_locations"] = len(caches)

    hit_rate = 0
    if any(p.get("pattern") == "hit_miss_tracking" for p in patterns):
        hit_rate = 75
    elif caches:
        hit_rate = 60

    metrics["estimated_hit_rate"] = hit_rate

    metrics["recommendations"] = []
    if efficiency_score >= 80:
        metrics["recommendations"].append("Cache implementation is well-optimized")
    elif efficiency_score >= 50:
        metrics["recommendations"].append(
            "Cache implementation needs some improvements"
        )
    else:
        metrics["recommendations"].append(
            "Cache implementation requires significant improvements"
        )

    return metrics


def invoke(payload: dict) -> dict:
    """
    Main entry point for MCP skill invocation.

    Expected payload format:
    {
        "code": "..." or {"file": "path/to/code.py"},
        "options": {
            "detection_level": "basic|standard|deep",
            "check_performance": true,
        },
        "generate_report": false,
    }
    """
    code = payload.get("code", "")

    if isinstance(code, dict):
        file_path = code.get("file")
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    code = f.read()
            except Exception as e:
                return {
                    "status": "error",
                    "error": f"Failed to read code file: {e}",
                }
        else:
            import json

            code = json.dumps(code)

    if not code:
        return {"status": "error", "error": "No code provided"}

    options = payload.get("options", {})
    result = cache_analyzer(code, options)

    if payload.get("generate_report", False):
        result["report"] = generate_report(result)

    return {"result": result}


def generate_report(analysis: dict) -> str:
    """Generate human-readable cache analysis report."""
    lines = []
    lines.append("=" * 60)
    lines.append("CACHE ANALYSIS REPORT")
    lines.append("=" * 60)

    metrics = analysis.get("metrics", {})
    lines.append(f"\nEfficiency Score: {metrics.get('efficiency_score', 0)}/100")
    lines.append(f"Estimated Hit Rate: {metrics.get('estimated_hit_rate', 0)}%")

    caches = analysis.get("caches", [])
    if caches:
        lines.append("\nDETECTED CACHES:")
        lines.append("-" * 40)
        for cache in caches:
            lines.append(
                f"  - {cache.get('type', 'unknown')} ({cache.get('library', 'unknown')})"
            )
            lines.append(f"    Location: {cache.get('location', 'N/A')}")
            lines.append(f"    Details: {cache.get('details', 'N/A')}")
            lines.append("")

    patterns = analysis.get("patterns", [])
    if patterns:
        lines.append("CACHE PATTERNS:")
        lines.append("-" * 40)
        for pattern in patterns:
            lines.append(f"  - {pattern.get('pattern', 'unknown')}")
            lines.append(f"    {pattern.get('description', '')}")
            lines.append("")

    issues = analysis.get("issues", [])
    if issues:
        lines.append("DETECTED ISSUES:")
        lines.append("-" * 40)
        for issue in issues:
            lines.append(
                f"  [{issue.get('severity', 'unknown').upper()}] {issue.get('issue', 'unknown')}"
            )
            lines.append(f"    {issue.get('description', '')}")
            lines.append("")

    suggestions = analysis.get("suggestions", [])
    if suggestions:
        lines.append("SUGGESTIONS:")
        lines.append("-" * 40)
        for i, suggestion in enumerate(suggestions[:5], 1):
            lines.append(f"{i}. {suggestion.get('issue', 'Unknown')}")
            lines.append(f"   Fix: {suggestion.get('fix', 'No fix suggested')}")
            if "code_example" in suggestion:
                lines.append(f"   Example: {suggestion['code_example'][:80]}...")
            lines.append("")

    return "\n".join(lines)


def register_skill():
    """Return skill metadata for MCP registration."""
    return {
        "name": "cache-analyzer",
        "description": "Analyze caching effectiveness in Python code - detects cache decorators, Redis, memcached, analyzes patterns, identifies issues like cache thrashing and wrong TTL, suggests improvements, and calculates efficiency metrics",
        "version": "1.0.0",
        "domain": "PERFORMANCE",
        "capabilities": [
            "Detect @lru_cache, @cache decorators",
            "Detect Redis cache usage (redis-py)",
            "Detect Memcached usage (python-memcached, pymemcache)",
            "Detect Django cache framework usage",
            "Detect Flask-Caching usage",
            "Detect custom cache implementations",
            "Analyze TTL and expiration patterns",
            "Analyze cache invalidation strategies",
            "Identify missing TTL issues",
            "Identify unbounded cache issues",
            "Identify cache thrashing potential",
            "Calculate efficiency score",
            "Generate improvement suggestions with code examples",
            "Create human-readable reports",
        ],
        "options": {
            "detection_level": "Level of cache detection (basic, standard, deep)",
            "check_performance": "Whether to analyze performance implications",
        },
    }


if __name__ == "__main__":
    test_code = """
from functools import lru_cache
import redis

@cache
def get_user(user_id):
    return fetch_from_db(user_id)

@cached
def expensive_computation(x, y):
    return x + y

class MyCache:
    def __init__(self):
        self.cache = {}
"""

    result = cache_analyzer(test_code, {"detection_level": "standard"})
    import json

    print(json.dumps(result, indent=2))
