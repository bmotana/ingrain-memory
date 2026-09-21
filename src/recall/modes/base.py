"""
Abstract base class for all memorization modes.
"""

from abc import ABC, abstractmethod
from typing import Optional
from recall.core.session import RecallSession


class BaseMode(ABC):
    """Base interface for recall interaction modes."""

    def __init__(
        self,
        case_sensitive: bool = True,
        ignore_whitespace: bool = False,
        language: Optional[str] = None,
    ):
        self.case_sensitive = case_sensitive
        self.ignore_whitespace = ignore_whitespace
        self.language = language

    @abstractmethod
    def run(self, session: RecallSession) -> bool:
        """
        Execute the recall game loop.
        Returns True if session completed successfully, False if aborted by user.
        """
        pass
