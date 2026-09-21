"""
Rich-powered terminal interface for Recall.
Handles banners, panels, screen clearing, formatting, and interactive prompts.
"""

import os
import sys
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text

from recall.core.session import SessionStats
from recall.ui.diff_view import render_line_diff, render_word_diff

console = Console()


def clear_screen() -> None:
    """Clear terminal screen in a cross-platform manner."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def show_banner() -> None:
    """Displays the stylized application banner."""
    banner_text = Text()
    banner_text.append("🧠 RECALL\n", style="bold cyan")
    banner_text.append("Terminal Active-Recall & Code Memorization Tool", style="dim italic")
    console.print(Panel(banner_text, border_style="cyan", expand=False, padding=(1, 4)))


def show_session_header(level: int, total_levels: int, mode_name: str) -> None:
    """Displays progress indicator for the current level."""
    pct = int((level / total_levels) * 100)
    bar_filled = "━" * (level * 20 // total_levels)
    bar_empty = "┈" * (20 - len(bar_filled))
    progress_bar = f"[{bar_filled}{bar_empty}]"

    header = Text()
    header.append(f"Level {level} / {total_levels} ", style="bold bright_white")
    header.append(f"{progress_bar} {pct}% ", style="cyan")
    header.append(f"• Mode: {mode_name.upper()}", style="dim")

    console.print(Panel(header, border_style="blue", padding=(0, 2)))


def show_target_content(chunks: List[str], unit: str = "line", language: Optional[str] = None) -> None:
    """Renders the text to be memorized inside a styled panel."""
    content = "\n".join(chunks) if unit == "line" else " ".join(chunks)

    if language and language not in ("text", "none"):
        try:
            renderable = Syntax(content, language, theme="monokai", line_numbers=(unit == "line"))
        except Exception:
            renderable = content
    else:
        renderable = content

    console.print(
        Panel(
            renderable,
            title="[bold yellow]👁️ Memorize This Part[/]",
            subtitle="[dim]Press Enter when you are ready to hide it[/]",
            border_style="yellow",
            padding=(1, 2),
        )
    )


def wait_for_enter(prompt_text: str = "Memorize this and press Enter to hide...") -> None:
    """Waits for user confirmation before clearing the screen."""
    console.print(f"[bold dim]{prompt_text}[/]", end=" ")
    try:
        input()
    except (KeyboardInterrupt, EOFError):
        console.print("\n[yellow]Session interrupted.[/]")
        sys.exit(0)


def prompt_recall_lines(unit: str = "line") -> List[str]:
    """
    Prompts the user to input their recalled text.
    For lines: reads until 'END' or blank double-enter.
    For words: reads a single line.
    """
    if unit == "word":
        console.print("[bold cyan]Type the recalled sentence so far:[/]")
        try:
            line = input("> ")
            return line.strip().split()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Session interrupted.[/]")
            sys.exit(0)
    else:
        console.print(
            "[bold cyan]Type the recalled lines so far[/] [dim](Type 'END' on a new line or ':q' to quit):[/]"
        )
        lines = []
        while True:
            try:
                line = input()
            except (KeyboardInterrupt, EOFError):
                console.print("\n[yellow]Session interrupted.[/]")
                sys.exit(0)

            if line.strip() == "END":
                break
            if line.strip().lower() == ":q":
                return [":q"]
            lines.append(line)
        return lines


def show_mismatch(expected: List[str], actual: List[str], unit: str = "line") -> None:
    """Renders mismatch diff comparison."""
    console.print("\n[bold red]❌ Not quite right yet![/]")
    if unit == "line":
        render_line_diff(expected, actual, console)
    else:
        render_word_diff(expected, actual, console)


def show_stats_summary(stats: SessionStats) -> None:
    """Renders the post-session stats scorecard."""
    table = Table(
        title="[bold green]🎉 Session Completed - Performance Scorecard[/]",
        show_header=True,
        header_style="bold green",
    )
    table.add_column("Metric", style="cyan")
    table.add_column("Result", style="bold white")

    table.add_row("Total Levels Mastered", str(stats.total_levels))
    table.add_row("Total Recall Attempts", str(stats.total_attempts))
    table.add_row("Recall Accuracy", f"{stats.accuracy_percentage}%")
    table.add_row("Hints Used", str(stats.hints_used))
    table.add_row("Time Taken", f"{stats.elapsed_seconds:.1f} seconds")

    console.print()
    console.print(table)

    if stats.accuracy_percentage >= 90:
        badge = "[bold gold1]🌟 Excellent memory retention! Keep it up![/]"
    elif stats.accuracy_percentage >= 70:
        badge = "[bold green]👍 Great work! A few more practice runs will make it second nature.[/]"
    else:
        badge = "[bold blue]💪 Good practice session. Repetition is key to mastery![/]"

    console.print(f"\n{badge}\n")
