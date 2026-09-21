"""
Text chunking utilities for recall sessions.
Supports splitting by words, lines, or logical blocks.
"""

from typing import List, Literal

ChunkUnit = Literal["word", "line"]


def chunk_text(text: str, unit: ChunkUnit = "word", strip_empty: bool = True) -> List[str]:
    """
    Splits input text into discrete memorization units (words or lines).

    Args:
        text: The source string to chunk.
        unit: 'word' for word-by-word recall, or 'line' for line-by-line recall.
        strip_empty: Whether to discard empty lines/tokens.

    Returns:
        List of non-empty string chunks.
    """
    if not text:
        return []

    # Standardize line breaks
    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")

    if unit == "line":
        raw_lines = normalized_text.split("\n")
        chunks = []
        for line in raw_lines:
            # We preserve leading spaces (crucial for code indentation),
            # but strip trailing spaces
            cleaned = line.rstrip()
            if strip_empty and not cleaned.strip():
                continue
            chunks.append(cleaned)
        return chunks

    elif unit == "word":
        # Split by whitespace, ignoring consecutive spaces/newlines
        raw_words = normalized_text.split()
        if strip_empty:
            return [w.strip() for w in raw_words if w.strip()]
        return raw_words

    else:
        raise ValueError(f"Unknown chunk unit: {unit}. Must be 'word' or 'line'.")


def detect_unit(text: str) -> ChunkUnit:
    """
    Heuristically detect the best chunking unit based on the text structure.
    Multi-line text defaults to 'line', single-line text defaults to 'word'.
    """
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    non_empty_lines = [line for line in normalized.split("\n") if line.strip()]
    if len(non_empty_lines) > 1:
        return "line"
    return "word"
