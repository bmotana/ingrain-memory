"""
Visual diff highlighting for recall mismatches.
Highlights differences between expected target text and user guesses.
"""

from typing import List
from rich.console import Console
from rich.table import Table
from rich.text import Text
import difflib


def render_line_diff(expected: List[str], actual: List[str], console: Console) -> None:
    """
    Renders a side-by-side comparison table highlighting line mismatches.
    """
    table = Table(
        title="[bold yellow]Comparison: Expected vs. Your Input[/]",
        show_header=True,
        header_style="bold magenta",
        expand=True,
    )
    table.add_column("#", justify="right", style="dim", width=4)
    table.add_column("Target (Expected)", style="green")
    table.add_column("Your Recall", style="white")
    table.add_column("Status", justify="center", width=10)

    max_len = max(len(expected), len(actual))

    for i in range(max_len):
        line_num = str(i + 1)
        exp = expected[i] if i < len(expected) else "[dim italic]<none>[/]"
        act = actual[i] if i < len(actual) else "[dim italic]<missing>[/]"

        if i < len(expected) and i < len(actual):
            if expected[i].strip() == actual[i].strip():
                status = "[bold green]MATCH[/]"
                act_styled = f"[green]{actual[i]}[/]"
            else:
                status = "[bold red]DIFF[/]"
                # Highlight character differences
                act_styled = highlight_char_diff(expected[i], actual[i])
        elif i >= len(actual):
            status = "[bold yellow]MISSING[/]"
            act_styled = "[dim red]<line omitted>[/]"
        else:
            status = "[bold red]EXTRA[/]"
            act_styled = f"[bold red]{actual[i]}[/]"

        table.add_row(line_num, exp, act_styled, status)

    console.print(table)


def highlight_char_diff(target: str, guess: str) -> str:
    """Highlight character-level additions and mismatches using Rich markup."""
    s = difflib.SequenceMatcher(None, target, guess)
    result = []
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        sub_guess = guess[j1:j2]
        if tag == "equal":
            result.append(f"[green]{sub_guess}[/]")
        elif tag in ("replace", "insert"):
            result.append(f"[bold red on #3a1111]{sub_guess}[/]")
    return "".join(result) if result else f"[red]{guess}[/]"


def render_word_diff(expected_words: List[str], actual_words: List[str], console: Console) -> None:
    """Renders inline diff for word-by-word recall."""
    t_exp = " ".join(expected_words)
    t_act = " ".join(actual_words)

    s = difflib.SequenceMatcher(None, expected_words, actual_words)
    styled_guess = Text()

    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag == "equal":
            styled_guess.append(" ".join(actual_words[j1:j2]) + " ", style="bold green")
        elif tag == "replace":
            styled_guess.append(" ".join(actual_words[j1:j2]) + " ", style="bold red underline")
        elif tag == "insert":
            styled_guess.append(" ".join(actual_words[j1:j2]) + " ", style="bold red")

    console.print("\n[bold]Expected:[/]")
    console.print(f"  [green]{t_exp}[/]")
    console.print("[bold]Your Input:[/]")
    console.print("  ", styled_guess)
