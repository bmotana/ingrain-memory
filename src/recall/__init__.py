"""
Recall - A modern terminal active-recall and memorization tool.
"""

__version__ = "0.1.0"
__author__ = "Bafana"

from recall.core.session import RecallSession
from recall.core.chunker import chunk_text
from recall.core.matcher import check_match

__all__ = ["RecallSession", "chunk_text", "check_match", "__version__"]
