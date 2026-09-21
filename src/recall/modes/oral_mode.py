"""
Oral / flashcard recall mode (inspired by v2_not_for_typing prototype).
Designed for speaking aloud or mental rehearsal with self-grading.
"""

import time
from rich.panel import Panel
from recall.modes.base import BaseMode
from recall.core.session import RecallSession
from recall.ui.console import (
    console,
    clear_screen,
    show_session_header,
    show_target_content,
    wait_for_enter,
    show_stats_summary,
)


class OralMode(BaseMode):
    """
    Hands-free / oral recall mode.
    Instead of typing each line/word, the user recites aloud and self-grades.
    """

    def run(self, session: RecallSession) -> bool:
        while not session.is_completed:
            clear_screen()
            show_session_header(session.current_level, session.total_levels, f"Oral Recall ({session.unit})")
            show_target_content(
                session.current_revealed_chunks,
                unit=session.unit,
                language=self.language,
            )

            wait_for_enter("Study this part and press Enter when ready to recite...")

            while True:
                clear_screen()
                show_session_header(
                    session.current_level,
                    session.total_levels,
                    f"Recite Aloud (Level {session.current_level})",
                )

                console.print(
                    Panel(
                        "🗣️ [bold cyan]Recite the revealed passage aloud now![/]\n"
                        "[dim]When finished reciting, press Enter to verify against the answer.[/]",
                        border_style="cyan",
                        padding=(1, 2),
                    )
                )

                wait_for_enter("Press Enter to reveal answer...")

                # Reveal answer for comparison
                clear_screen()
                show_session_header(session.current_level, session.total_levels, "Self-Verification")
                show_target_content(
                    session.current_revealed_chunks,
                    unit=session.unit,
                    language=self.language,
                )

                console.print("\n[bold]Did you recite it correctly?[/]")
                console.print("  [bold green][Y][/] Yes, got it right  |  [bold yellow][R][/] Retry level  |  [bold red][Q][/] Quit")
                console.print("Choice [Y/r/q]: ", end="")

                try:
                    choice = input().strip().lower()
                except (KeyboardInterrupt, EOFError):
                    console.print("\n[yellow]Session interrupted.[/]")
                    return False

                if choice in ("q", ":q", "quit"):
                    console.print("\n[yellow]Quitting session...[/]")
                    return False
                elif choice in ("y", "yes", ""):
                    session.record_attempt(True)
                    console.print("\n[bold green]✅ Great job! Moving to next level...[/]")
                    time.sleep(0.8)
                    session.advance()
                    break
                else:
                    session.record_attempt(False)
                    console.print("\n[yellow]Let's try this level again.[/]")
                    time.sleep(1.0)

        clear_screen()
        show_stats_summary(session.get_stats())
        return True
