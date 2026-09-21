"""
Snippet library management.
Discovers bundled sample decks and manages custom user decks.
"""

from dataclasses import dataclass
import json
import os
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class DeckSnippet:
    name: str
    category: str
    description: str
    content: str
    default_unit: str = "line"
    language: Optional[str] = None


BUILTIN_SAMPLES: List[DeckSnippet] = [
    DeckSnippet(
        name="data_viz",
        category="code",
        description="Seaborn & Matplotlib regression plot setup (from V3 prototype)",
        content="""plt.figure(figsize=(9, 5))
sns.set_style("whitegrid")
sns.regplot(x="Age", y="Salary", data=df)
plt.xlim(27, 42)
plt.ylim(60000, 95000)
plt.legend(["ALL"])
plt.show()""",
        default_unit="line",
        language="python",
    ),
    DeckSnippet(
        name="python_idioms",
        category="code",
        description="Dictionary defaults & nested list comprehension",
        content="""counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
flattened = [item for sublist in matrix for item in sublist]""",
        default_unit="line",
        language="python",
    ),
    DeckSnippet(
        name="invictus",
        category="poetry",
        description="Invictus (Stanza 1) by William Ernest Henley",
        content="""Out of the night that covers me,
Black as the pit from pole to pole,
I thank whatever gods may be
For my unconquerable soul.""",
        default_unit="line",
        language="text",
    ),
    DeckSnippet(
        name="french_phrase",
        category="quotes",
        description="Classic French lyric (Ne me quitte pas)",
        content="Ne me quitte pas, il faut oublier, tout peut s'oublier qui s'enfuit déjà.",
        default_unit="word",
        language="text",
    ),
    DeckSnippet(
        name="git_workflow",
        category="commands",
        description="Standard Git feature branch workflow",
        content="""git checkout -b feature/active-recall
git add .
git commit -m "feat: implement active recall engine"
git push -u origin feature/active-recall""",
        default_unit="line",
        language="bash",
    ),
]


class LibraryManager:
    """Manages bundled and user-saved snippets."""

    def __init__(self, custom_dir: Optional[Path] = None):
        if custom_dir:
            self.user_dir = custom_dir
        else:
            self.user_dir = Path.home() / ".recall"
        self.user_file = self.user_dir / "user_decks.json"

    def get_all_samples(self) -> List[DeckSnippet]:
        """Returns bundled samples merged with any user-saved decks."""
        decks = list(BUILTIN_SAMPLES)
        user_decks = self._load_user_decks()
        decks.extend(user_decks)
        return decks

    def find_snippet(self, name: str) -> Optional[DeckSnippet]:
        """Finds a snippet by name (case-insensitive)."""
        target = name.strip().lower()
        for deck in self.get_all_samples():
            if deck.name.lower() == target:
                return deck
        return None

    def save_user_deck(self, name: str, content: str, description: str = "", unit: str = "line", language: str = "text") -> None:
        """Saves or updates a custom user deck."""
        self.user_dir.mkdir(parents=True, exist_ok=True)
        raw_data = self._read_raw_user_file()
        raw_data[name] = {
            "name": name,
            "category": "custom",
            "description": description or f"User deck: {name}",
            "content": content,
            "default_unit": unit,
            "language": language,
        }
        with open(self.user_file, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, indent=2)

    def _read_raw_user_file(self) -> Dict[str, dict]:
        if not self.user_file.exists():
            return {}
        try:
            with open(self.user_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _load_user_decks(self) -> List[DeckSnippet]:
        raw = self._read_raw_user_file()
        decks = []
        for d in raw.values():
            decks.append(
                DeckSnippet(
                    name=d.get("name", "custom"),
                    category=d.get("category", "custom"),
                    description=d.get("description", ""),
                    content=d.get("content", ""),
                    default_unit=d.get("default_unit", "line"),
                    language=d.get("language", "text"),
                )
            )
        return decks
