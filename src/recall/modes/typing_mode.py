"""
Interactive typing recall mode (word-by-word or line-by-line).
"""

import time
from recall.modes.base import BaseMode
from recall.core.session import RecallSession
from recall.core.matcher import check_match
from recall.ui.console import (
    console,
    clear_screen,
    show_session_header,
    show_target_content,
    wait_for_enter,
    prompt_recall_lines,
    show_mismatch,
    show_stats_summary,
)


class TypingMode(BaseMode):
    """
    Standard active-recall typing mode.
    Reveals progressively more words or lines and requires exact reproduction.
    """

    def run(self, session: RecallSession) -> bool:
        while not session.is_completed:
            clear_screen()
            show_session_header(session.current_level, session.total_levels, f"Typing ({session.unit})")
            show_target_content(
                session.current_revealed_chunks,
                unit=session.unit,
                language=self.language,
            )

            wait_for_enter("Memorize this part and press Enter to hide it...")

            hint_to_show = None

            # Attempt loop for current level
            while True:
                clear_screen()
                show_session_header(session.current_level, session.total_levels, f"Recalling Level {session.current_level}")

                if hint_to_show:
                    console.print(f"[bold yellow]💡 Hint:[/] {hint_to_show}\n")

                user_input = prompt_recall_lines(unit=session.unit)

                # Check for special commands
                if len(user_input) == 1 and user_input[0].strip().lower() in (":q", "quit", "q"):
                    console.print("\n[yellow]Quitting session...[/]")
                    return False

                if len(user_input) == 1 and user_input[0].strip().lower() in (":h", "hint"):
                    hint_to_show = session.get_hint()
                    continue

                # Check match against target
                expected = session.current_revealed_chunks
                result = check_match(
                    expected=expected,
                    actual=user_input,
                    case_sensitive=self.case_sensitive,
                    ignore_whitespace=self.ignore_whitespace,
                )

                if result.is_match:
                    session.record_attempt(True)
                    console.print("\n[bold green]✅ Correct! Moving to the next level...[/]")
                    time.sleep(0.9)
                    session.advance()
                    break
                else:
                    session.record_attempt(False)
                    show_mismatch(expected, user_input, unit=session.unit)
                    console.print("\n[dim]Press Enter to try again, or type ':h' for a hint, ':q' to quit:[/]", end=" ")
                    action = input().strip().lower()
                    if action in (":q", "q", "quit"):
                        console.print("\n[yellow]Quitting session...[/]")
                        return False
                    elif action in (":h", "hint"):
                        hint_to_show = session.get_hint()
                    else:
                        hint_to_show = None

        # Completed all levels
        clear_screen()
        show_stats_summary(session.get_stats())
        return True
