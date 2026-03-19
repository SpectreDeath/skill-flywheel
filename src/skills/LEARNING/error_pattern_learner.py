import hashlib
import re
from collections import defaultdict
from datetime import datetime


class ErrorPatternLearner:
    def __init__(self):
        self.patterns = []
        self.clusters = defaultdict(list)
        self.learned_fixes = {}
        self.error_history = []
        self.pattern_weights = defaultdict(lambda: 1.0)

    def collect_errors(self, errors: str) -> list[dict]:
        error_list = []

        if isinstance(errors, str):
            lines = errors.split("\n")
            for line in lines:
                if self._is_error_line(line):
                    error_dict = self._parse_error_line(line)
                    if error_dict:
                        error_list.append(error_dict)
        elif isinstance(errors, list):
            for item in errors:
                if isinstance(item, str):
                    error_dict = self._parse_error_line(item)
                    if error_dict:
                        error_list.append(error_dict)
                elif isinstance(item, dict):
                    error_list.append(item)

        self.error_history.extend(error_list)
        return error_list

    def _is_error_line(self, line: str) -> bool:
        error_indicators = [
            "error",
            "exception",
            "fail",
            "traceback",
            "raised",
            "failed",
        ]
        return any(indicator in line.lower() for indicator in error_indicators)

    def _parse_error_line(self, line: str) -> dict:
        error_type_match = re.search(
            r"(\w+(?:\.\w+)*(?:Error|Exception|Failure))", line
        )
        error_type = error_type_match.group(1) if error_type_match else "UnknownError"

        message_match = re.search(r'["\']([^"\']+)["\']', line)
        message = message_match.group(1) if message_match else line.strip()

        return {
            "type": error_type,
            "message": message,
            "raw": line,
            "timestamp": datetime.now().isoformat(),
            "hash": self._hash_error(message),
        }

    def _hash_error(self, message: str) -> str:
        return hashlib.md5(message.encode()).hexdigest()[:8]

    def identify_patterns(self) -> list[dict]:
        type_counts = defaultdict(int)
        for error in self.error_history:
            type_counts[error["type"]] += 1

        self.patterns = []
        for error_type, count in sorted(
            type_counts.items(), key=lambda x: x[1], reverse=True
        ):
            pattern = {
                "type": error_type,
                "count": count,
                "frequency": count / len(self.error_history)
                if self.error_history
                else 0,
                "severity": self._estimate_severity(error_type),
            }
            self.patterns.append(pattern)

        return self.patterns

    def _estimate_severity(self, error_type: str) -> str:
        critical = ["RuntimeError", "SystemError", "MemoryError", "RecursionError"]
        high = ["KeyError", "ValueError", "AttributeError", "TypeError"]
        medium = ["ImportError", "ModuleNotFoundError", "FileNotFoundError"]

        if error_type in critical:
            return "critical"
        elif error_type in high:
            return "high"
        elif error_type in medium:
            return "medium"
        return "low"

    def cluster_errors(self) -> dict[str, list[dict]]:
        message_patterns = defaultdict(list)

        for error in self.error_history:
            normalized = self._normalize_message(error["message"])
            cluster_key = self._extract_cluster_key(normalized)
            message_patterns[cluster_key].append(error)

        self.clusters = {}
        for idx, (key, errors) in enumerate(message_patterns.items()):
            cluster_id = f"cluster_{idx}"
            self.clusters[cluster_id] = {
                "key": key,
                "errors": errors,
                "size": len(errors),
                "representative": errors[0] if errors else None,
            }

        return self.clusters

    def _normalize_message(self, message: str) -> str:
        normalized = re.sub(r"\d+", "N", message)
        normalized = re.sub(r"0x[0-9a-fA-F]+", "0xHEX", normalized)
        normalized = re.sub(r"[<\[{].*?[>\]}]", "VAR", normalized)
        return normalized.lower()

    def _extract_cluster_key(self, normalized: str) -> str:
        words = normalized.split()[:3]
        return "_".join(words) if words else "unknown"

    def learn_fixes(self, fixes: dict[str, str]) -> dict[str, str]:
        for error_hash, fix in fixes.items():
            self.learned_fixes[error_hash] = {
                "fix": fix,
                "timestamp": datetime.now().isoformat(),
                "success_count": 1,
            }
        return self.learned_fixes

    def record_successful_fix(self, error_hash: str, fix: str) -> None:
        if error_hash in self.learned_fixes:
            self.learned_fixes[error_hash]["success_count"] += 1
            self.learned_fixes[error_hash]["timestamp"] = datetime.now().isoformat()
        else:
            self.learned_fixes[error_hash] = {
                "fix": fix,
                "timestamp": datetime.now().isoformat(),
                "success_count": 1,
            }
        self.pattern_weights[error_hash] *= 1.1

    def predict_fixes(self, new_errors: list[dict]) -> list[dict]:
        predictions = []

        for error in new_errors:
            error_hash = self._hash_error(error.get("message", error.get("raw", "")))
            error_type = error.get("type", "UnknownError")

            prediction = {
                "error": error,
                "suggested_fixes": [],
                "confidence": 0.0,
                "similar_errors": [],
            }

            if error_hash in self.learned_fixes:
                fix_data = self.learned_fixes[error_hash]
                prediction["suggested_fixes"].append(fix_data["fix"])
                prediction["confidence"] = min(1.0, fix_data["success_count"] * 0.2)

            similar = self._find_similar_errors(error)
            for sim_error in similar[:3]:
                sim_hash = sim_error.get("hash", "")
                if sim_hash in self.learned_fixes:
                    fix = self.learned_fixes[sim_hash]["fix"]
                    if fix not in prediction["suggested_fixes"]:
                        prediction["suggested_fixes"].append(fix)

            if prediction["suggested_fixes"]:
                prediction["confidence"] = min(1.0, prediction["confidence"] + 0.3)

            prediction["similar_errors"] = similar[:3]
            predictions.append(prediction)

        return predictions

    def _find_similar_errors(self, error: dict) -> list[dict]:
        target_normalized = self._normalize_message(error.get("message", ""))
        similar = []

        for existing in self.error_history:
            existing_normalized = self._normalize_message(existing.get("message", ""))
            similarity = self._calculate_similarity(
                target_normalized, existing_normalized
            )
            if similarity > 0.5:
                existing["similarity"] = similarity
                similar.append(existing)

        return sorted(similar, key=lambda x: x.get("similarity", 0), reverse=True)

    def _calculate_similarity(self, s1: str, s2: str) -> float:
        words1 = set(s1.split())
        words2 = set(s2.split())
        if not words1 or not words2:
            return 0.0
        intersection = words1 & words2
        union = words1 | words2
        return len(intersection) / len(union) if union else 0.0

    def get_summary(self) -> dict:
        return {
            "total_errors": len(self.error_history),
            "unique_patterns": len(self.patterns),
            "clusters": len(self.clusters),
            "learned_fixes": len(self.learned_fixes),
            "top_patterns": self.patterns[:5],
        }


_learner_instance = ErrorPatternLearner()


def error_pattern_learner(errors: str, options: dict = None) -> dict:
    options = options or {}
    mode = options.get("mode", "analyze")
    persist = options.get("persist", False)

    try:
        collected = _learner_instance.collect_errors(errors)

        if not collected:
            return {
                "status": "success",
                "patterns": [],
                "clusters": {},
                "learned_fixes": {},
                "predictions": [],
                "message": "No errors detected in input",
            }

        patterns = _learner_instance.identify_patterns()
        clusters = _learner_instance.cluster_errors()

        if mode == "learn" and "fixes" in options:
            _learner_instance.learn_fixes(options["fixes"])

        predictions = _learner_instance.predict_fixes(collected)

        result = {
            "status": "success",
            "patterns": patterns,
            "clusters": clusters,
            "learned_fixes": _learner_instance.learned_fixes,
            "predictions": predictions,
            "summary": _learner_instance.get_summary(),
        }

        if persist:
            _persist_data()

        return result

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "patterns": [],
            "clusters": {},
            "learned_fixes": {},
            "predictions": [],
        }


def _persist_data() -> None:
    data = {
        "patterns": _learner_instance.patterns,
        "learned_fixes": _learner_instance.learned_fixes,
        "error_history_count": len(_learner_instance.error_history),
    }
    return data


def invoke(payload: dict) -> dict:
    errors = payload.get("errors", "")
    options = payload.get("options", {})

    return error_pattern_learner(errors, options)


def register_skill() -> dict:
    return {
        "name": "error_pattern_learner",
        "description": "Learns from recurring errors by collecting, clustering, and predicting fixes",
        "version": "1.0.0",
        "functions": {
            "error_pattern_learner": {
                "description": "Main function to analyze errors and learn patterns",
                "parameters": {
                    "errors": "Error log (string or list)",
                    "options": "Optional settings (mode, persist, fixes)",
                },
            },
            "invoke": {
                "description": "Skill invocation entry point",
                "parameters": {"payload": "Dict with errors and options"},
            },
            "register_skill": {
                "description": "Returns skill metadata for registration"
            },
        },
        "capabilities": [
            "collect_errors",
            "identify_patterns",
            "cluster_errors",
            "learn_fixes",
            "predict_fixes",
        ],
    }
