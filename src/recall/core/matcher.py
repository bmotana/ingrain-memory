"""
Matching and comparison engine for recall guesses.
Provides flexible comparison (case sensitivity, whitespace tolerance) and diff generation.
"""

from dataclasses import dataclass, field
import difflib
import re
from typing import List, Tuple, Optional


@dataclass
class MatchResult:
    """Represents the outcome of a comparison between target and user guess."""
    is_match: bool
    similarity: float  # 0.0 to 1.0
    expected_lines: List[str]
    actual_lines: List[str]
    diff_tokens: List[Tuple[str, str]] = field(default_factory=list)  # ('equal'|'insert'|'delete'|'replace', text)
    error_summary: str = ""


def normalize_string(
    text: str,
    case_sensitive: bool = True,
    ignore_whitespace: bool = False,
    ignore_punctuation: bool = False,
) -> str:
    """Normalizes a single string according to matching rules."""
    res = text
    if not case_sensitive:
        res = res.lower()
    if ignore_whitespace:
        # Standardize spaces and tabs
        res = re.sub(r"\s+", " ", res).strip()
    if ignore_punctuation:
        res = re.sub(r"[^\w\s]", "", res)
    return res


def normalize_lines(
    lines: List[str],
    case_sensitive: bool = True,
    ignore_whitespace: bool = False,
    ignore_punctuation: bool = False,
) -> List[str]:
    """Normalizes a list of lines/tokens."""
    normalized = []
    for line in lines:
        cleaned = normalize_string(
            line,
            case_sensitive=case_sensitive,
            ignore_whitespace=ignore_whitespace,
            ignore_punctuation=ignore_punctuation,
        )
        normalized.append(cleaned)
    return normalized


def check_match(
    expected: List[str],
    actual: List[str],
    case_sensitive: bool = True,
    ignore_whitespace: bool = False,
    ignore_punctuation: bool = False,
) -> MatchResult:
    """
    Compares the expected target list of chunks/lines against the user's actual input.

    Args:
        expected: List of expected chunks or lines.
        actual: List of received chunks or lines.
        case_sensitive: Whether character case matters.
        ignore_whitespace: Whether to collapse multiple spaces/tabs.
        ignore_punctuation: Whether to ignore punctuation marks.

    Returns:
        MatchResult with match status, similarity ratio, and diff details.
    """
    norm_exp = normalize_lines(expected, case_sensitive, ignore_whitespace, ignore_punctuation)
    norm_act = normalize_lines(actual, case_sensitive, ignore_whitespace, ignore_punctuation)

    # Filter out empty lines from both if ignore_whitespace
    if ignore_whitespace:
        norm_exp = [x for x in norm_exp if x]
        norm_act = [x for x in norm_act if x]

    is_match = (norm_exp == norm_act)

    # Compute similarity using difflib
    exp_joined = "\n".join(norm_exp)
    act_joined = "\n".join(norm_act)
    matcher = difflib.SequenceMatcher(None, exp_joined, act_joined)
    similarity = matcher.ratio()

    diff_tokens: List[Tuple[str, str]] = []
    error_summary = ""

    if not is_match:
        if len(norm_act) < len(norm_exp):
            missing_count = len(norm_exp) - len(norm_act)
            error_summary = f"Missing {missing_count} line{'s' if missing_count > 1 else ''} or token{'s' if missing_count > 1 else ''}."
        elif len(norm_act) > len(norm_exp):
            extra_count = len(norm_act) - len(norm_exp)
            error_summary = f"Input has {extra_count} extra line{'s' if extra_count > 1 else ''} or token{'s' if extra_count > 1 else ''}."
        else:
            # Same line count, but content differs
            for idx, (exp_l, act_l) in enumerate(zip(norm_exp, norm_act), start=1):
                if exp_l != act_l:
                    error_summary = f"Mismatch at item {idx}."
                    break

    return MatchResult(
        is_match=is_match,
        similarity=similarity,
        expected_lines=expected,
        actual_lines=actual,
        diff_tokens=diff_tokens,
        error_summary=error_summary,
    )
