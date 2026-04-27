#!/usr/bin/env python3
"""
Surgical Constraint

Enforces Karpathy's 'Surgical Changes' principle:
- Touch only what's necessary
- Don't refactor things that aren't broken
- Changes should trace directly to the request
- Clean up only your own mess
"""

import logging
import difflib
import re
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class CodeChange:
    """Represents a single code modification."""
    filepath: str
    line_num: int
    old_content: str
    new_content: str
    change_type: str  # add, modify, delete
    related_to_request: bool = False


@dataclass
class SurgicalValidation:
    passed: bool
    changes: List[CodeChange] = field(default_factory=list)
    related_changes: int = 0
    unrelated_changes: int = 0
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    magnitude_score: float = 0.0


class SurgicalConstraint:
    """Enforces minimal, focused changes that address only the request."""

    def __init__(self, max_change_ratio: float = 0.1, max_lines_changed: int = 50):
        """
        Args:
            max_change_ratio: Maximum ratio of changed lines to total lines
            max_lines_changed: Maximum absolute lines that can be changed
        """
        self.max_change_ratio = max_change_ratio
        self.max_lines_changed = max_lines_changed

    def validate(
        self,
        original_code: str,
        modified_code: str,
        request_description: str,
        filepath: str = "<unknown>",
    ) -> SurgicalValidation:
        """
        Validate that code changes are surgical and focused.

        Args:
            original_code: Code before modification
            modified_code: Code after modification
            request_description: What the change was supposed to address
            filepath: Path to the file being validated

        Returns:
            SurgicalValidation with analysis results
        """
        diff = self._compute_diff(original_code, modified_code)
        changes = self._parse_diff(diff, filepath)
        request_keywords = self._extract_keywords(request_description)

        related = self._filter_related_changes(changes, request_keywords)
        unrelated = [c for c in changes if c not in related]

        magnitude = self._compute_magnitude(original_code, changes)
        issues = self._identify_issues(changes, unrelated, magnitude)
        suggestions = self._generate_suggestions(unrelated, magnitude)

        is_surgical = len(unrelated) == 0 and magnitude <= self.max_change_ratio

        return SurgicalValidation(
            passed=is_surgical,
            changes=changes,
            related_changes=len(related),
            unrelated_changes=len(unrelated),
            issues=issues,
            suggestions=suggestions,
            magnitude_score=magnitude,
        )

    def _compute_diff(self, original: str, modified: str) -> List[str]:
        """Compute line-by-line diff between original and modified code."""
        original_lines = original.splitlines(keepends=True)
        modified_lines = modified.splitlines(keepends=True)

        differ = difflib.unified_diff(
            original_lines,
            modified_lines,
            lineterm="",
        )

        return list(differ)

    def _parse_diff(self, diff: List[str], filepath: str) -> List[CodeChange]:
        """Parse unified diff into structured code changes."""
        changes = []
        current_line = 0

        for line in diff:
            # Skip diff metadata headers
            if line.startswith("---") or line.startswith("+++") or line.startswith("@@"):
                continue

            if line.startswith("-") and not line.startswith("---"):
                # Deleted line
                changes.append(
                    CodeChange(
                        filepath=filepath,
                        line_num=current_line + 1,
                        old_content=line[1:].strip(),
                        new_content="",
                        change_type="delete",
                    )
                )
                current_line += 1
            elif line.startswith("+") and not line.startswith("+++"):
                # Added line
                changes.append(
                    CodeChange(
                        filepath=filepath,
                        line_num=current_line + 1,
                        old_content="",
                        new_content=line[1:].strip(),
                        change_type="add",
                    )
                )
            # Context line (unchanged)
            elif line.strip():
                current_line += 1

        return changes

    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract meaningful keywords from request description."""
        # Remove common words and punctuation
        words = re.findall(r'\b[a-z]+\b', text.lower())
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
            "this", "that", "these", "those", "will", "should", "could", "may",
            "can", "must", "shall", "would", "might", "has", "have", "had",
        }

        return set(w for w in words if w not in stop_words and len(w) > 2)

    def _filter_related_changes(
        self, changes: List[CodeChange], request_keywords: Set[str]
    ) -> List[CodeChange]:
        """Identify changes related to the request based on keyword matching."""
        related = []

        for change in changes:
            # Combine old and new content for keyword search
            content = f"{change.old_content} {change.new_content}".lower()

            # Check if any request keyword appears in the change
            for keyword in request_keywords:
                if keyword in content:
                    change.related_to_request = True
                    related.append(change)
                    break

        return related

    def _compute_magnitude(self, original: str, changes: List[CodeChange]) -> float:
        """Compute ratio of changed lines to total lines."""
        total_lines = len(original.splitlines())

        if total_lines == 0:
            return 0.0

        changed_lines = len(changes)
        return changed_lines / total_lines

    def _identify_issues(
        self,
        changes: List[CodeChange],
        unrelated: List[CodeChange],
        magnitude: float,
    ) -> List[str]:
        """Identify issues with the changes."""
        issues = []

        if unrelated:
            issues.append(
                f"{len(unrelated)} unrelated changes detected - not surgical"
            )

        if magnitude > self.max_change_ratio:
            issues.append(
                f"Change magnitude ({magnitude:.1%}) exceeds threshold "
                f"({self.max_change_ratio:.1%})"
            )

        if len(changes) > self.max_lines_changed:
            issues.append(
                f"Too many lines changed ({len(changes)}) - exceeds "
                f"maximum ({self.max_lines_changed})"
            )

        return issues

    def _generate_suggestions(
        self, unrelated: List[CodeChange], magnitude: float
    ) -> List[str]:
        """Generate suggestions for making changes more surgical."""
        suggestions = []

        if unrelated:
            suggestions.append(
                "Review and remove unrelated changes - "
                "only modify code directly related to the request"
            )

        if magnitude > self.max_change_ratio * 0.8:
            suggestions.append(
                "Consider breaking this into smaller, incremental changes"
            )

        if magnitude > self.max_change_ratio * 1.5:
            suggestions.append(
                "This appears to be over-engineering - "
                "implement minimal solution first"
            )

        return suggestions

    def to_prolog_rules(self) -> str:
        """
        Generate Prolog rules for surgical change validation.
        """
        return """
% === Surgical Changes Constraint Rules ===
% Validate that modifications are minimal and focused

% Check if a change is related to the request
related_to_request(Change, RequestKeywords) :-
    change_content(Change, Content),
    keyword_match(Content, RequestKeywords).

% Keyword matching in content
keyword_match(Content, [Keyword | Rest]) :-
    sub_atom(Content, _, _, _, Keyword), !.
keyword_match(Content, [_ | Rest]) :-
    keyword_match(Content, Rest).

% Compute change magnitude (ratio of changed to total lines)
change_magnitude(OriginalLines, ChangeCount, Magnitude) :-
    OriginalLines > 0,
    Magnitude is ChangeCount / OriginalLines.

% Check if change magnitude is acceptable
acceptable_magnitude(Magnitude) :-
    max_change_ratio(Max),
    Magnitude =< Max.

max_change_ratio(0.10).  % Default: max 10% of code changed

% Validate that all changes are surgical
validate_surgical_changes(Original, Modified, Request, Validation) :-
    compute_diff(Original, Modified, Diff),
    parse_diff(Diff, Changes),
    extract_keywords(Request, Keywords),
    partition_related(Changes, Keywords, Related, Unrelated),
    length(Changes, TotalChanged),
    length(OriginalLines, TotalOriginal),
    change_magnitude(TotalOriginal, TotalChanged, Magnitude),
    (   Unrelated = [],
        acceptable_magnitude(Magnitude)
    ->  Validation = passed
    ;   Validation = failed
    ),
    % Log details
    format('Changes: ~w total~n', [TotalChanged]),
    format('Related to request: ~w~n', [Related]),
    format('Unrelated (non-surgical): ~w~n', [Unrelated]),
    format('Magnitude: ~2f~n', [Magnitude]).

% Partition changes into related and unrelated
partition_related([], _, [], []).
partition_related([Change | Rest], Keywords, [Change | Related], Unrelated) :-
    related_to_request(Change, Keywords), !,
    partition_related(Rest, Keywords, Related, Unrelated).
partition_related([Change | Rest], Keywords, Related, [Change | Unrelated]) :-
    partition_related(Rest, Keywords, Related, Unrelated).

% Warn about non-surgical changes
warn_non_surgical(Validation) :-
    Validation = failed,
    format('WARNING: Changes are not surgical!~n').
warn_non_surgical(passed).
        """
    
    def to_hy_heuristics(self) -> str:
        """
        Generate Hy/Lisp heuristics for surgical changes.
        """
        return r"""
;; === Surgical Change Heuristics ===
;; Ensure changes are minimal, focused, and traceable

(defn compute-diff [original modified]
  "Compute line-by-line diff between code versions"
  (let [orig-lines (clojure.string/split-lines original)
        mod-lines (clojure.string/split-lines modified)
        matcher (difflib/UnifiedDiffer.)]
    (.compare matcher orig-lines mod-lines)
    (vec (map #(apply str %) (.getGroupedOpcodes matcher 2)))))

(defn parse-changes [diff]
  "Parse diff into structured change objects"
  (for [[tag i1 i2 j1 j2 lines] diff
        :when (not= tag \equal)]
    {:tag tag
     :original-lines (vec (range i1 i2))
     :modified-lines (vec (range j1 j2))
     :content lines}))

(defn extract-keywords [text]
  "Extract meaningful keywords from request"
  (let [words (clojure.string/split (clojure.string/lower-case text) #"\s+")
        stop-words #{"the" "a" "an" "and" "or" "but" "in" "on" "at" "to" "for"}
        significant (filter #(> (count %) 2) words)]
    (set (remove stop-words significant))))

(defn changes-related? [change keywords]
  "Check if a change is related to the request keywords"
  (let [content (apply str (:content change))
        content-lower (clojure.string/lower-case content)]
    (some #(clojure.string/includes? content-lower %)
          keywords)))

(defn partition-changes [changes keywords]
  "Split changes into related and unrelated"
  (let [related (filter #(changes-related? % keywords) changes)
        unrelated (remove #(changes-related? % keywords) changes)]
    [related unrelated]))

(defn compute-magnitude [original changes]
  "Calculate ratio of changed lines to total lines"
  (let [total-lines (count (clojure.string/split-lines original))
        changed-lines (count changes)]
    (if (zero? total-lines)
      0.0
      (/ changed-lines total-lines))))

(defn validate-surgical [original modified request & {:keys [max-ratio] 
                                                      :or {max-ratio 0.1}}]
  "Validate that code changes are surgical"
  (let [diff (compute-diff original modified)
        changes (parse-changes diff)
        keywords (extract-keywords request)
        [related unrelated] (partition-changes changes keywords)
        magnitude (compute-magnitude original changes)]
    {:passed (and (empty? unrelated) (<= magnitude max-ratio))
     :changes changes
     :related related
     :unrelated unrelated
     :magnitude magnitude
     :max-ratio max-ratio
     :issues (cond-> []
               (seq unrelated) (conj "Unrelated changes detected")
               (> magnitude max-ratio) (conj "Change magnitude too large"))}))

(defn suggest-surgical-improvements [validation]
  "Suggest ways to make changes more surgical"
  (let [{:keys [unrelated magnitude max-ratio]} validation]
    (cond-> []
      (seq unrelated)
      (conj (str "Remove " (count unrelated) " unrelated changes"))
      (> magnitude (* max-ratio 0.8))
      (conj "Consider incremental changes")
      :always
      (conj "Verify each change traces to the request"))))
        """
