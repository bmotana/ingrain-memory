"""
Code-specialized active-recall mode.
Highlights syntax, line numbers, code diffs, and offers indentation tolerance.
"""

import time
from typing import Optional
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


class CodeMode(BaseMode):
    """
    Active recall mode tuned specifically for code syntax and multi-line snippets.
    """

    def __init__(
        self,
        case_sensitive: bool = True,
        ignore_whitespace: bool = False,
        language: Optional[str] = "python",
    ):
        super().__init__(
            case_sensitive=case_sensitive,
            ignore_whitespace=ignore_whitespace,
            language=language or "python",
        )

    def run(self, session: RecallSession) -> bool:
        while not session.is_completed:
            clear_screen()
            show_session_header(
                session.current_level,
                session.total_levels,
                f"Code Recall ({self.language})",
            )
            show_target_content(
                session.current_revealed_chunks,
                unit="line",
                language=self.language,
            )

            wait_for_enter("Memorize the code and press Enter to hide...")

            hint_to_show = None

            while True:
                clear_screen()
                show_session_header(
                    session.current_level,
                    session.total_levels,
                    f"Recalling Code (Up to Line {session.current_level})",
                )

                if hint_to_show:
                    console.print(f"[bold yellow]💡 Code Hint:[/] {hint_to_show}\n")

                user_input = prompt_recall_lines(unit="line")

                # Quit check
                if len(user_input) == 1 and user_input[0].strip().lower() in (":q", "quit", "q"):
                    console.print("\n[yellow]Quitting code session...[/]")
                    return False

                if len(user_input) == 1 and user_input[0].strip().lower() in (":h", "hint"):
                    hint_to_show = session.get_hint()
                    continue

                expected = session.current_revealed_chunks
                result = check_match(
                    expected=expected,
                    actual=user_input,
                    case_sensitive=self.case_sensitive,
                    ignore_whitespace=self.ignore_whitespace,
                )

                if result.is_match:
                    session.record_attempt(True)
                    console.print("\n[bold green]✅ Code matches perfectly! Advancing to next line...[/]")
                    time.sleep(0.9)
                    session.advance()
                    break
                else:
                    session.record_attempt(False)
                    show_mismatch(expected, user_input, unit="line")
                    console.print("\n[dim]Press Enter to try again, ':h' for hint, ':q' to quit:[/]", end=" ")
                    action = input().strip().lower()
                    if action in (":q", "q", "quit"):
                        console.print("\n[yellow]Quitting session...[/]")
                        return False
                    elif action in (":h", "hint"):
                        hint_to_show = session.get_hint()
                    else:
                        hint_to_show = None

        clear_screen()
        show_stats_summary(session.get_stats())
        return True
