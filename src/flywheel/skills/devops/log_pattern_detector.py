"""
Log Pattern Detector

Detects patterns in logs, identifies anomalies, clusters similar entries,
and generates insights about log data.

Supports: Common log formats (Apache, Nginx, JSON, Syslog, Custom)
"""

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List

SEVERITY_LEVELS = {
    "trace": 0,
    "debug": 1,
    "info": 2,
    "warn": 3,
    "warning": 3,
    "error": 4,
    "err": 4,
    "critical": 5,
    "fatal": 6,
    "panic": 6,
}

LOG_PATTERNS = {
    "apache_combined": r'(?P<ip>[\d.]+) - (?P<user>[\w-]+) \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<path>[^\s]+) (?P<protocol>[^"]+)" (?P<status>\d+) (?P<size>[\d-]+) "(?P<referer>[^"]*)" "(?P<user_agent>[^"]*)"',
    "apache_common": r'(?P<ip>[\d.]+) - (?P<user>[\w-]+) \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<path>[^\s]+) (?P<protocol>[^"]+)" (?P<status>\d+) (?P<size>[\d-]+)',
    "nginx": r'(?P<ip>[\d.a-f:]+) - (?P<user>[\w-]+) \[(?P<timestamp>[^\]]+)\] "(?P<method>\w+) (?P<path>[^\s]+) (?P<protocol>[^"]+)" (?P<status>\d+) (?P<size>[\d]+) "(?P<referer>[^"]+)" "(?P<user_agent>[^"]+)" (?P<response_time>[\d.]+)',
    "syslog": r"(?P<timestamp>\w+\s+\d+\s+[\d:]+) (?P<host>\S+) (?P<process>\S+?)(?:\[(?P<pid>\d+)\])?: (?P<message>.*)",
    "python": r"(?P<timestamp>[\d-]+\s+[\d:,]+)\s+-\s+(?P<logger>\S+)\s+-\s+(?P<level>\w+)\s+-\s+(?P<message>.*)",
    "java": r"(?P<timestamp>[\d{}.:\s]+)\s+(?P<level>\w+)\s+\[(?P<thread>[^\]]+)\]\s+(?P<class>\S+)\s+-\s+(?P<message>.*)",
    "json": r'\{".*\}',
    "simple": r"\[(?P<timestamp>[^\]]+)\]\s*\[(?P<level>[^\]]+)\]\s*(?P<message>.*)",
    "generic": r"(?P<timestamp>\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}[^\s]*)\s+(?P<level>\w+)\s+(?P<message>.*)",
}


@dataclass
class LogEntry:
    raw: str
    timestamp: str | None = None
    level: str | None = None
    message: str | None = None
    source: str | None = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def detect_log_format(logs: str) -> str:
    """Detect the log format from the log content."""
    lines = logs.strip().split("\n")[:20]

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("{") and line.endswith("}"):
            try:
                json.loads(line)
                return "json"
            except json.JSONDecodeError:
                pass

        for fmt, pattern in LOG_PATTERNS.items():
            if re.search(pattern, line) and fmt != "json":
                return fmt

    return "generic"


def parse_json_logs(logs: str) -> List[LogEntry]:
    """Parse JSON-formatted logs."""
    entries = []
    for line in logs.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
            level = None
            if isinstance(data, dict):
                for key in ["level", "severity", "loglevel", "log_level"]:
                    if key in data:
                        level = data[key].lower()
                        break

                timestamp = (
                    data.get("timestamp") or data.get("time") or data.get("@timestamp")
                )
                message = data.get("message") or data.get("msg") or data.get("log")

                entries.append(
                    LogEntry(
                        raw=line,
                        timestamp=timestamp,
                        level=level,
                        message=message,
                        metadata=data,
                    )
                )
        except json.JSONDecodeError:
            entries.append(LogEntry(raw=line, message=line))
    return entries


def parse_structured_logs(logs: str, format_type: str) -> List[LogEntry]:
    """Parse structured log formats using regex patterns."""
    entries = []
    pattern = LOG_PATTERNS.get(format_type)

    if not pattern:
        return parse_unstructured_logs(logs)

    regex = re.compile(pattern)

    for line in logs.strip().split("\n"):
        line = line.strip()
        if not line:
            continue

        match = regex.search(line)
        if match:
            data = match.groupdict()
            level = data.get("level", "").lower() if data.get("level") else None

            entries.append(
                LogEntry(
                    raw=line,
                    timestamp=data.get("timestamp"),
                    level=level,
                    message=data.get("message") or data.get("path") or data.get("msg"),
                    source=data.get("host")
                    or data.get("process")
                    or data.get("logger"),
                    metadata=data,
                )
            )
        else:
            entries.append(LogEntry(raw=line, message=line))

    return entries


def parse_unstructured_logs(logs: str) -> List[LogEntry]:
    """Parse unstructured logs by extracting timestamp and level patterns."""
    entries = []

    timestamp_patterns = [
        r"(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}[^\s]*)",
        r"(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})",
        r"(\w+\s+\d+\s+\d{2}:\d{2}:\d{2})",
        r"(\[\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}\s+[+-]\d{4}\])",
    ]

    level_pattern = (
        r"\b(TRACE|DEBUG|INFO|WARN(?:ING)?|ERROR|ERR|CRITICAL|FATAL|PANIC)\b"
    )

    for line in logs.strip().split("\n"):
        line = line.strip()
        if not line:
            continue

        timestamp = None
        for tp in timestamp_patterns:
            match = re.search(tp, line)
            if match:
                timestamp = match.group(1)
                break

        level_match = re.search(level_pattern, line, re.IGNORECASE)
        level = level_match.group(1).lower() if level_match else None

        entries.append(
            LogEntry(raw=line, timestamp=timestamp, level=level, message=line)
        )

    return entries


def parse_logs(logs: str, format_type: str | None = None) -> List[LogEntry]:
    """Parse log content into structured entries."""
    if not logs or not logs.strip():
        return []

    if format_type is None:
        format_type = detect_log_format(logs)

    if format_type == "json":
        return parse_json_logs(logs)
    elif format_type in LOG_PATTERNS:
        return parse_structured_logs(logs, format_type)
    else:
        return parse_unstructured_logs(logs)


def detect_patterns(entries: List[LogEntry]) -> List[Dict[str, Any]]:
    """Detect common patterns in log entries."""
    patterns = []

    message_templates = Counter()
    for entry in entries:
        if entry.message:
            template = extract_message_template(entry.message)
            message_templates[template] += 1

    for template, count in message_templates.most_common(10):
        if count > 1:
            patterns.append(
                {
                    "type": "message_template",
                    "template": template,
                    "count": count,
                    "percentage": round(count / len(entries) * 100, 2)
                    if entries
                    else 0,
                }
            )

    ip_pattern = re.compile(r"\b(?:[\d]{1,3}\.){3}[\d]{1,3}\b")
    ip_counts = Counter()
    for entry in entries:
        if entry.message:
            for ip in ip_pattern.findall(entry.message):
                ip_counts[ip] += 1

    for ip, count in ip_counts.most_common(5):
        if count > 1:
            patterns.append({"type": "ip_address", "ip": ip, "count": count})

    path_pattern = re.compile(r"(?:GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)\s+([^\s]+)")
    paths = Counter()
    for entry in entries:
        if entry.message:
            match = path_pattern.search(entry.message)
            if match:
                paths[match.group(1)] += 1

    for path, count in paths.most_common(5):
        if count > 1:
            patterns.append({"type": "http_path", "path": path, "count": count})

    status_pattern = re.compile(r"\b([1-5]\d{2})\b")
    status_counts = Counter()
    for entry in entries:
        if entry.message:
            for status in status_pattern.findall(entry.message):
                if len(status) == 3:
                    status_counts[status] += 1

    for status, count in status_counts.most_common():
        if count > 0:
            patterns.append(
                {
                    "type": "http_status",
                    "status": status,
                    "count": count,
                    "category": get_status_category(status),
                }
            )

    return patterns


def extract_message_template(message: str) -> str:
    """Extract a template from a log message by replacing dynamic values."""
    template = re.sub(r"[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}", "<IP>", message)
    template = re.sub(
        r"\b[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12}\b",
        "<UUID>",
        template,
    )
    template = re.sub(r"\b\d+\b", "<NUM>", template)
    template = re.sub(r'"[^"]*"', "<STRING>", template)
    template = re.sub(r"[^\s]{20,}", "<LONG>", template)
    return template


def get_status_category(status: str) -> str:
    """Get HTTP status category."""
    code = int(status[0])
    categories = {
        "1": "informational",
        "2": "success",
        "3": "redirection",
        "4": "client_error",
        "5": "server_error",
    }
    return categories.get(str(code), "unknown")


def find_anomalies(
    entries: List[LogEntry], severity_threshold: str = "info"
) -> List[Dict[str, Any]]:
    """Find anomalies in log entries."""
    anomalies = []
    threshold_level = SEVERITY_LEVELS.get(severity_threshold.lower(), 2)

    error_entries = []
    exception_entries = []
    critical_entries = []

    exception_patterns = [
        r"\b(Exception|Error|Err|Exception|Traceback|Caused by)",
        r"\b(?:NullPointer|Syntax|Timeout|Connection|Assertion)\s*[Ee]rror\b",
        r"\bstack\s*trace\b",
        r"\bfailed\b",
        r"\bfatal\b",
        r"\bpanic\b",
    ]

    for entry in entries:
        level = entry.level.lower() if entry.level else ""

        if level in SEVERITY_LEVELS and SEVERITY_LEVELS[level] >= threshold_level:
            if level in ["error", "err", "critical", "fatal", "panic"]:
                error_entries.append(entry)

        if entry.message:
            for pattern in exception_patterns:
                if re.search(pattern, entry.message, re.IGNORECASE):
                    exception_entries.append(entry)
                    break

            if any(
                word in entry.message.lower()
                for word in ["critical", "fatal", "panic", "crash"]
            ):
                critical_entries.append(entry)

    for entry in error_entries[:20]:
        anomalies.append(
            {
                "type": "error",
                "level": entry.level,
                "timestamp": entry.timestamp,
                "message": entry.message[:200] if entry.message else "",
                "raw": entry.raw[:200],
            }
        )

    for entry in exception_entries[:20]:
        if entry not in error_entries:
            anomalies.append(
                {
                    "type": "exception",
                    "level": entry.level or "unknown",
                    "timestamp": entry.timestamp,
                    "message": entry.message[:200] if entry.message else "",
                    "raw": entry.raw[:200],
                }
            )

    for entry in critical_entries[:10]:
        anomalies.append(
            {
                "type": "critical",
                "level": entry.level or "unknown",
                "timestamp": entry.timestamp,
                "message": entry.message[:200] if entry.message else "",
                "raw": entry.raw[:200],
            }
        )

    time_spikes = detect_time_spikes(entries)
    anomalies.extend(time_spikes)

    return anomalies


def detect_time_spikes(entries: List[LogEntry]) -> List[Dict[str, Any]]:
    """Detect time-based spikes in log volume."""
    time_counts = defaultdict(int)

    for entry in entries:
        if entry.timestamp:
            truncated_ts = (
                entry.timestamp[:13] if len(entry.timestamp) >= 13 else entry.timestamp
            )
            time_counts[truncated_ts] += 1

    if not time_counts:
        return []

    avg_count = sum(time_counts.values()) / len(time_counts)
    threshold = avg_count * 2

    spikes = []
    for ts, count in time_counts.items():
        if count > threshold and count > 5:
            spikes.append(
                {
                    "type": "volume_spike",
                    "timestamp": ts,
                    "count": count,
                    "threshold": round(threshold, 2),
                    "message": f"Log volume spike detected at {ts}: {count} entries",
                }
            )

    return spikes


def cluster_logs(
    entries: List[LogEntry], max_clusters: int = 10
) -> List[Dict[str, Any]]:
    """Cluster similar log entries together."""
    templates = defaultdict(list)

    for i, entry in enumerate(entries):
        if entry.message:
            template = extract_message_template(entry.message)
            templates[template].append(i)

    clusters = []
    for template, indices in sorted(
        templates.items(), key=lambda x: len(x[1]), reverse=True
    )[:max_clusters]:
        sample_entries = [entries[i].raw[:150] for i in indices[:3]]

        clusters.append(
            {
                "id": len(clusters) + 1,
                "template": template,
                "count": len(indices),
                "percentage": round(len(indices) / len(entries) * 100, 2)
                if entries
                else 0,
                "sample_entries": sample_entries,
            }
        )

    return clusters


def generate_insights(
    entries: List[LogEntry],
    patterns: List[Dict],
    anomalies: List[Dict],
    clusters: List[Dict],
) -> List[str]:
    """Generate insights from log analysis."""
    insights = []

    if not entries:
        insights.append("No log entries found to analyze")
        return insights

    level_counts = Counter()
    for entry in entries:
        if entry.level:
            level_counts[entry.level.lower()] += 1

    total = len(entries)
    error_count = sum(
        level_counts.get(l, 0) for l in ["error", "err", "critical", "fatal", "panic"]
    )

    if error_count > 0:
        error_rate = (error_count / total) * 100
        insights.append(
            f"Error rate: {error_rate:.2f}% ({error_count}/{total} entries)"
        )

        if error_rate > 10:
            insights.append(
                "High error rate detected - investigate error patterns immediately"
            )
        elif error_rate > 5:
            insights.append(
                "Moderate error rate - consider investigating top error patterns"
            )

    if level_counts.get("warn") or level_counts.get("warning"):
        warn_count = level_counts.get("warn", 0) + level_counts.get("warning", 0)
        insights.append(f"Warnings present: {warn_count} warning entries")

    if patterns:
        http_paths = [p for p in patterns if p.get("type") == "http_path"]
        if http_paths:
            top_path = http_paths[0]
            insights.append(
                f"Most accessed endpoint: {top_path.get('path')} ({top_path.get('count')} hits)"
            )

        http_statuses = [p for p in patterns if p.get("type") == "http_status"]
        error_statuses = [
            s
            for s in http_statuses
            if s.get("category") in ["client_error", "server_error"]
        ]
        if error_statuses:
            for status_info in error_statuses[:3]:
                insights.append(
                    f"HTTP {status_info.get('status')} errors: {status_info.get('count')} occurrences"
                )

    if clusters:
        top_cluster = clusters[0]
        insights.append(
            f"Most common log pattern: {top_cluster.get('template')[:50]}... ({top_cluster.get('count')} occurrences)"
        )

        if top_cluster.get("percentage", 0) > 50:
            insights.append(
                f"High repetition: single pattern accounts for {top_cluster.get('percentage')}% of logs"
            )

    if anomalies:
        critical_anomalies = [a for a in anomalies if a.get("type") == "critical"]
        if critical_anomalies:
            insights.append(
                f"Critical issues detected: {len(critical_anomalies)} critical events require immediate attention"
            )

        spike_anomalies = [a for a in anomalies if a.get("type") == "volume_spike"]
        if spike_anomalies:
            insights.append(
                f"Volume spikes detected: {len(spike_anomalies)} time periods with unusual log activity"
            )

    if not insights:
        insights.append("Logs appear healthy with no significant issues detected")

    return insights


def generate_summary(
    entries: List[LogEntry],
    patterns: List[Dict],
    anomalies: List[Dict],
    clusters: List[Dict],
) -> Dict[str, Any]:
    """Generate summary statistics."""
    level_counts = Counter()
    for entry in entries:
        if entry.level:
            level_counts[entry.level.lower()] += 1

    sources = Counter()
    for entry in entries:
        if entry.source:
            sources[entry.source] += 1

    return {
        "total_entries": len(entries),
        "unique_patterns": len(
            {extract_message_template(e.message or "") for e in entries if e.message}
        ),
        "severity_breakdown": dict(level_counts),
        "top_sources": dict(sources.most_common(5)),
        "patterns_found": len(patterns),
        "anomalies_found": len(anomalies),
        "clusters_formed": len(clusters),
        "time_range": {
            "earliest": min(
                (e.timestamp for e in entries if e.timestamp), default=None
            ),
            "latest": max((e.timestamp for e in entries if e.timestamp), default=None),
        },
    }


def log_pattern_detector(logs: str, options: dict = None) -> dict:
    """
    Main function to detect patterns in logs.

    Args:
        logs: Log content to analyze
        options: Optional configuration
            - format: Log format (auto-detected if not specified)
            - severity_threshold: Minimum severity to flag as anomaly (default: info)

    Returns:
        Dictionary with:
            - status: "success" or "error"
            - patterns: Detected log patterns
            - anomalies: Anomalies found
            - clusters: Log clusters
            - insights: Key insights
            - summary: Summary statistics
    """
    if options is None:
        options = {}

    try:
        format_type = options.get("format")
        severity_threshold = options.get("severity_threshold", "info")

        entries = parse_logs(logs, format_type)

        if not entries:
            return {
                "status": "success",
                "patterns": [],
                "anomalies": [],
                "clusters": [],
                "insights": ["No log entries found to analyze"],
                "summary": {"total_entries": 0},
            }

        detected_format = detect_log_format(logs)

        patterns = detect_patterns(entries)

        anomalies = find_anomalies(entries, severity_threshold)

        clusters = cluster_logs(entries)

        insights = generate_insights(entries, patterns, anomalies, clusters)

        summary = generate_summary(entries, patterns, anomalies, clusters)
        summary["detected_format"] = detected_format

        return {
            "status": "success",
            "patterns": patterns,
            "anomalies": anomalies,
            "clusters": clusters,
            "insights": insights,
            "summary": summary,
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "patterns": [],
            "anomalies": [],
            "clusters": [],
            "insights": [],
            "summary": {},
        }


def invoke(payload: dict) -> dict:
    """MCP skill invocation."""
    logs = payload.get("logs", "")
    options = payload.get("options", {})

    result = log_pattern_detector(logs, options)

    return {"result": result}


def register_skill():
    """Return skill metadata."""
    return {
        "name": "log-pattern-detector",
        "description": "Detects patterns in logs, identifies anomalies, clusters similar entries, and generates insights about log data",
        "version": "1.0.0",
        "domain": "DEVOPS",
    }
