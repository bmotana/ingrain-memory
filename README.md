# 🧠 Recall CLI

> A modern, terminal-based active recall and memorization tool for code snippets, poetry, prose, and speeches.

`recall` turns rote memorization into an interactive, step-by-step game. It builds muscle memory and mental retention by progressively revealing text unit-by-unit (words or lines), prompting you to reproduce it, and giving you instant visual feedback with colorized diffs.

---

## ✨ Features

- **🎮 Three Dedicated Recall Modes**:
  - **Code Mode**: Syntax highlighting, line numbers, indentation tolerance, and side-by-side diffs.
  - **Typing Mode**: Word-by-word or line-by-line progressive recall with strict or forgiving matching.
  - **Oral / Flashcard Mode**: Hands-free practice for reciting out loud or mental review with self-assessment.
- **🔍 Smart Visual Diffs**: When you make a mistake, `recall` doesn't just say *"Wrong"*; it renders an inline table highlighting character differences, missing lines, and extra tokens.
- **💡 Active-Recall Hints**: Stuck on a level? Type `:h` or `hint` to reveal the first letters of words with the rest masked out.
- **📚 Built-in Deck Library**: Comes preloaded with Python idioms, Matplotlib/Seaborn visualization setups, poetry (*Invictus*), French phrases, and Git workflows.
- **💾 Custom Decks**: Easily save your own snippets and study decks using `recall add <name>`.
- **📊 Performance Scorecard**: Detailed end-of-session breakdown with total attempts, accuracy percentage, hints used, and completion time.
- **⚡ Clean CLI Experience**: Built with [Rich](https://github.com/Textualize/rich), featuring cross-platform screen clearing, progress bars, and zero screen clutter.

---

## 🚀 Installation & Setup

### Requirements
- Python 3.10 or newer

### Install Locally (Editable)
```bash
# Clone or navigate to the directory
cd "memorization tool"

# Install in editable mode
pip install -e .
```

After installation, the `recall` command will be globally available in your terminal!

---

## 💻 Quick Start & Usage

### 1. Interactive Menu
Simply run `recall` (or `python main.py`) with no arguments to open the interactive launcher:

```bash
recall
```

```
🧠 RECALL
Terminal Active-Recall & Code Memorization Tool

Select an action:
  1. Quick Sentence Recall (word-by-word typing)
  2. Code Memorizer (line-by-line with syntax highlighting)
  3. Oral / Speech Practice (recite aloud, self-graded)
  4. Practice from Snippet Library
  5. Load from a File
  6. View Snippet Library
  7. Exit
```

---

### 2. CLI Commands & Options

#### Start an active recall session
```bash
# Memorize a single sentence (word by word)
recall start -t "The quick brown fox jumps over the lazy dog"

# Memorize code from a file
recall start -f samples/data_viz.py -m code

# Practice a built-in sample deck
recall start -s invictus -m oral

# Practice with whitespace leniency (great for tabs vs. spaces)
recall start -f script.py --ignore-whitespace

# Case-insensitive recall
recall start -t "To be or not to be" --ignore-case
```

#### In-Game Shortcuts
During any active recall level:
- Type `:h` or `hint` to view an active-recall hint.
- Type `:q` or `quit` to end the session early.
- Type `END` on a new line when submitting multi-line code.

#### Browse and inspect snippet decks
```bash
# List all preloaded and custom decks
recall samples

# Preview snippet content with syntax highlighting
recall show data_viz
```

#### Save a custom snippet to your personal library
```bash
recall add my_sql_query -d "Window function template" -l sql
```

---

## 🧪 Running Tests

The test suite uses Python's standard `unittest` framework with no external test runners required:

```bash
python -m unittest discover -s tests
```

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).
