"""
Session manager that tracks progress, levels, attempts, hints, and elapsed time.
"""

from dataclasses import dataclass, field
import time
from typing import List, Dict, Optional, Literal
from recall.core.chunker import ChunkUnit


@dataclass
class SessionStats:
    total_levels: int
    total_attempts: int
    successful_attempts: int
    hints_used: int
    elapsed_seconds: float
    accuracy_percentage: float


class RecallSession:
    """
    Tracks the progression through an active recall challenge.
    Each level adds one chunk to the target to remember.
    """

    def __init__(self, chunks: List[str], unit: ChunkUnit = "word"):
        if not chunks:
            raise ValueError("RecallSession requires at least one chunk to memorize.")
        self.chunks = chunks
        self.unit = unit
        self.current_level = 1
        self.total_levels = len(chunks)
        self.attempts: Dict[int, int] = {i: 0 for i in range(1, self.total_levels + 1)}
        self.hints_used: Dict[int, int] = {i: 0 for i in range(1, self.total_levels + 1)}
        self.start_time = time.time()
        self.end_time: Optional[float] = None
        self._completed = False

    @property
    def is_completed(self) -> bool:
        return self._completed

    @property
    def current_revealed_chunks(self) -> List[str]:
        """All chunks revealed up to and including the current level."""
        return self.chunks[:self.current_level]

    @property
    def latest_chunk(self) -> str:
        """The newest chunk introduced at this level."""
        return self.chunks[self.current_level - 1]

    def record_attempt(self, success: bool) -> None:
        """Record an attempt for the current level."""
        self.attempts[self.current_level] += 1

    def record_hint(self) -> None:
        """Record hint usage for current level."""
        self.hints_used[self.current_level] += 1

    def advance(self) -> bool:
        """
        Advance to the next level.
        Returns True if advanced, or False if all levels are completed.
        """
        if self.current_level >= self.total_levels:
            self._completed = True
            self.end_time = time.time()
            return False
        self.current_level += 1
        return True

    def get_hint(self) -> str:
        """
        Generate an active-recall hint for the newest chunk at this level.
        Masks the middle of words or reveals the first characters.
        """
        self.record_hint()
        target = self.latest_chunk
        if self.unit == "word":
            # For a single word: reveal first letter and length
            if len(target) <= 2:
                return target[0] + "_" * (len(target) - 1)
            return target[0] + "_" * (len(target) - 2) + target[-1]
        else:
            # For a line: mask words except their first letters
            words = target.split()
            hint_words = []
            for w in words:
                if len(w) <= 2:
                    hint_words.append(w)
                else:
                    hint_words.append(w[0] + "_" * (len(w) - 1))
            return " ".join(hint_words)

    def get_stats(self) -> SessionStats:
        """Calculate summary performance statistics for the session."""
        now = self.end_time if self.end_time else time.time()
        elapsed = max(0.1, now - self.start_time)
        total_attempts = sum(self.attempts.values())
        hints = sum(self.hints_used.values())
        successful = self.total_levels if self._completed else (self.current_level - 1)

        accuracy = 0.0
        if total_attempts > 0:
            accuracy = round((successful / total_attempts) * 100, 1)

        return SessionStats(
            total_levels=self.total_levels,
            total_attempts=total_attempts,
            successful_attempts=successful,
            hints_used=hints,
            elapsed_seconds=round(elapsed, 1),
            accuracy_percentage=accuracy,
        )
