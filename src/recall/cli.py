"""
CLI entry point for Recall.
Handles argument parsing, commands, and interactive menu navigation.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# Ensure standard streams handle UTF-8 cleanly on Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

from recall import __version__
from recall.core.chunker import chunk_text, detect_unit
from recall.core.session import RecallSession
from recall.core.library import LibraryManager, DeckSnippet
from recall.modes import TypingMode, CodeMode, OralMode
from recall.ui.console import console, show_banner, clear_screen


def display_samples_table(library: LibraryManager) -> None:
    """Prints a styled table of all available sample decks."""
    table = Table(title="[bold bright_magenta]📚 Recall Snippet Library[/]", expand=True, border_style="bright_blue", header_style="bold bright_cyan")
    table.add_column("Name", style="bold bright_green", width=18)
    table.add_column("Category", style="bright_magenta", width=12)
    table.add_column("Language", style="bright_blue", width=10)
    table.add_column("Default Unit", style="bright_yellow", width=12)
    table.add_column("Description", style="bright_white")

    for snippet in library.get_all_samples():
        table.add_row(
            snippet.name,
            snippet.category,
            snippet.language or "text",
            snippet.default_unit,
            snippet.description,
        )

    console.print()
    console.print(table)
    console.print("\n[dim]Run [cyan]recall start -s <name>[/] or [cyan]recall show <name>[/] to inspect.[/]\n")


def execute_session(
    text: str,
    mode_name: str = "typing",
    unit: Optional[str] = None,
    language: Optional[str] = None,
    case_sensitive: bool = True,
    ignore_whitespace: bool = False,
) -> None:
    """Prepares and launches the active recall session."""
    if not text.strip():
        console.print("[bold red]Error:[/] No text provided to memorize.")
        return

    # Auto-detect unit if not explicitly specified
    chunk_unit = unit if unit else detect_unit(text)
    chunks = chunk_text(text, unit=chunk_unit)

    if not chunks:
        console.print("[bold red]Error:[/] Could not extract any chunks from the provided text.")
        return

    session = RecallSession(chunks=chunks, unit=chunk_unit)

    mode_map = {
        "typing": TypingMode(
            case_sensitive=case_sensitive,
            ignore_whitespace=ignore_whitespace,
            language=language,
        ),
        "code": CodeMode(
            case_sensitive=case_sensitive,
            ignore_whitespace=ignore_whitespace,
            language=language or "python",
        ),
        "oral": OralMode(
            case_sensitive=case_sensitive,
            ignore_whitespace=ignore_whitespace,
            language=language,
        ),
    }

    mode_runner = mode_map.get(mode_name.lower(), mode_map["typing"])
    mode_runner.run(session)


def interactive_paste() -> str:
    """Collects multi-line text from standard input until 'END' or EOF."""
    console.print(
        Panel(
            "Paste or type your text below.\n"
            "When finished, type [bold yellow]'END'[/] on a new line and press Enter.",
            title="[bold cyan]Multi-line Text Input[/]",
            border_style="cyan",
        )
    )
    lines = []
    while True:
        try:
            line = input()
        except (KeyboardInterrupt, EOFError):
            break
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def interactive_menu(library: LibraryManager) -> None:
    """Renders an interactive launcher menu if no arguments are provided."""
    while True:
        clear_screen()
        show_banner()
        console.print(Panel(
            "[bold bright_yellow]1.[/] [bold bright_cyan]Quick Sentence Recall[/] [dim](word-by-word typing)[/]\n"
            "[bold bright_yellow]2.[/] [bold bright_green]Code Memorizer[/] [dim](line-by-line with syntax highlighting)[/]\n"
            "[bold bright_yellow]3.[/] [bold bright_magenta]Oral / Speech Practice[/] [dim](recite aloud, self-graded)[/]\n"
            "[bold bright_yellow]4.[/] [bright_blue]Practice from Snippet Library[/]\n"
            "[bold bright_yellow]5.[/] [bright_cyan]Load from a File[/]\n"
            "[bold bright_yellow]6.[/] [bright_green]View Snippet Library[/]\n"
            "[bold bright_yellow]7.[/] [bright_red]Exit[/]",
            title="[bold bright_magenta]Select an action[/]", border_style="bright_cyan", padding=(1, 2),
        ))

        try:
            choice = input("Enter choice [1-7]: ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[yellow]Goodbye![/]")
            sys.exit(0)

        if choice == "1":
            console.print("\n[cyan]Enter the sentence you want to memorize:[/]")
            sentence = input("> ").strip()
            if sentence:
                execute_session(sentence, mode_name="typing", unit="word")
            break

        elif choice == "2":
            clear_screen()
            console.print("[bold cyan]Code Memorizer[/]\n")
            console.print("1. Paste code interactively")
            console.print("2. Choose sample (e.g. data_viz, python_idioms)")
            sub_choice = input("Choice [1/2]: ").strip()
            if sub_choice == "2":
                display_samples_table(library)
                name = input("Enter snippet name: ").strip()
                snip = library.find_snippet(name)
                if snip:
                    execute_session(snip.content, mode_name="code", unit=snip.default_unit, language=snip.language)
                else:
                    console.print(f"[red]Snippet '{name}' not found.[/]")
                    input("Press Enter to continue...")
            else:
                code_text = interactive_paste()
                if code_text.strip():
                    execute_session(code_text, mode_name="code", unit="line", language="python")
            break

        elif choice == "3":
            clear_screen()
            console.print("[bold cyan]Oral / Speech Practice[/]\n")
            text = interactive_paste()
            if text.strip():
                unit = detect_unit(text)
                execute_session(text, mode_name="oral", unit=unit)
            break

        elif choice == "4":
            clear_screen()
            display_samples_table(library)
            name = input("Enter sample name to practice: ").strip()
            snip = library.find_snippet(name)
            if snip:
                mode = "code" if snip.category == "code" else "typing"
                execute_session(
                    snip.content,
                    mode_name=mode,
                    unit=snip.default_unit,
                    language=snip.language,
                )
            else:
                console.print(f"[red]Snippet '{name}' not found.[/]")
                input("Press Enter to continue...")

        elif choice == "5":
            path_str = input("Enter file path: ").strip().strip('"')
            p = Path(path_str)
            if p.exists() and p.is_file():
                try:
                    content = p.read_text(encoding="utf-8")
                    lang = "python" if p.suffix == ".py" else ("javascript" if p.suffix in (".js", ".ts") else "text")
                    mode = "code" if lang != "text" else "typing"
                    execute_session(content, mode_name=mode, unit="line", language=lang)
                except Exception as e:
                    console.print(f"[red]Error reading file:[/] {e}")
                    input("Press Enter to continue...")
            else:
                console.print(f"[red]File '{path_str}' does not exist.[/]")
                input("Press Enter to continue...")

        elif choice == "6":
            clear_screen()
            display_samples_table(library)
            input("Press Enter to return to menu...")

        elif choice in ("7", "q", "quit", "exit"):
            console.print("\n[yellow]Goodbye![/]")
            sys.exit(0)


def build_parser() -> argparse.ArgumentParser:
    """Builds the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="recall",
        description="Recall - A modern terminal active-recall and memorization tool.",
    )
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Start command
    start_p = subparsers.add_parser("start", help="Start an active-recall session")
    start_p.add_argument("-t", "--text", type=str, help="Text to memorize directly")
    start_p.add_argument("-f", "--file", type=Path, help="File containing text or code to memorize")
    start_p.add_argument("-s", "--sample", type=str, help="Name of a built-in or user sample deck")
    start_p.add_argument(
        "-m", "--mode",
        choices=["typing", "code", "oral"],
        default=None,
        help="Interaction mode (default: auto-detected)",
    )
    start_p.add_argument(
        "-u", "--unit",
        choices=["word", "line"],
        default=None,
        help="Chunking unit: 'word' or 'line' (default: auto-detected)",
    )
    start_p.add_argument("-l", "--lang", type=str, default=None, help="Syntax language for code mode (e.g. python, bash)")
    start_p.add_argument("--ignore-whitespace", action="store_true", help="Ignore extra spaces/tabs in comparisons")
    start_p.add_argument("--ignore-case", action="store_true", help="Case-insensitive recall matching")

    # Samples command
    subparsers.add_parser("samples", help="List all available practice samples and decks")

    # Show command
    show_p = subparsers.add_parser("show", help="Show snippet content from library")
    show_p.add_argument("name", type=str, help="Snippet name to inspect")

    # Add command
    add_p = subparsers.add_parser("add", help="Add a custom snippet to your personal library")
    add_p.add_argument("name", type=str, help="Unique name for the snippet")
    add_p.add_argument("-d", "--description", type=str, default="", help="Description of the snippet")
    add_p.add_argument("-u", "--unit", choices=["word", "line"], default="line", help="Default chunking unit")
    add_p.add_argument("-l", "--lang", type=str, default="text", help="Language syntax for snippet")

    return parser


def main() -> None:
    """Main CLI entrypoint."""
    library = LibraryManager()
    parser = build_parser()

    # If no arguments provided, launch interactive menu
    if len(sys.argv) == 1:
        interactive_menu(library)
        return

    args = parser.parse_args()

    if args.command == "samples":
        display_samples_table(library)
        return

    elif args.command == "show":
        snip = library.find_snippet(args.name)
        if not snip:
            console.print(f"[bold red]Error:[/] Snippet '{args.name}' not found.")
            sys.exit(1)
        console.print(
            Panel(
                snip.content,
                title=f"[bold green]{snip.name}[/] ({snip.category})",
                subtitle=snip.description,
                border_style="bright_green",
            )
        )
        return

    elif args.command == "add":
        console.print(f"[bold cyan]Adding new snippet '{args.name}'[/]")
        text = interactive_paste()
        if not text.strip():
            console.print("[yellow]Empty content. Aborted.[/]")
            return
        library.save_user_deck(
            name=args.name,
            content=text,
            description=args.description,
            unit=args.unit,
            language=args.lang,
        )
        console.print(f"[bold green]✓[/] Snippet '{args.name}' saved to your local library!")
        return

    elif args.command == "start":
        text_to_memorize = ""
        mode = args.mode
        unit = args.unit
        lang = args.lang

        if args.sample:
            snip = library.find_snippet(args.sample)
            if not snip:
                console.print(f"[bold red]Error:[/] Sample '{args.sample}' not found.")
                sys.exit(1)
            text_to_memorize = snip.content
            if not unit:
                unit = snip.default_unit
            if not lang:
                lang = snip.language
            if not mode:
                mode = "code" if snip.category == "code" else "typing"

        elif args.file:
            if not args.file.exists():
                console.print(f"[bold red]Error:[/] File '{args.file}' does not exist.")
                sys.exit(1)
            text_to_memorize = args.file.read_text(encoding="utf-8")
            if not lang:
                if args.file.suffix == ".py":
                    lang = "python"
                elif args.file.suffix in (".js", ".ts"):
                    lang = "javascript"
                elif args.file.suffix == ".sh":
                    lang = "bash"
                else:
                    lang = "text"
            if not mode:
                mode = "code" if lang != "text" else "typing"

        elif args.text:
            text_to_memorize = args.text
        else:
            text_to_memorize = interactive_paste()

        if not mode:
            mode = "typing"

        execute_session(
            text=text_to_memorize,
            mode_name=mode,
            unit=unit,
            language=lang,
            case_sensitive=not args.ignore_case,
            ignore_whitespace=args.ignore_whitespace,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
