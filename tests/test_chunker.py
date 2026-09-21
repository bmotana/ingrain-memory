import unittest
from recall.core.chunker import chunk_text, detect_unit


class TestChunker(unittest.TestCase):
    def test_chunk_words(self):
        text = "The quick brown fox jumps"
        chunks = chunk_text(text, unit="word")
        self.assertEqual(chunks, ["The", "quick", "brown", "fox", "jumps"])

    def test_chunk_lines_preserves_indent(self):
        code = "def foo():\n    return 42\n\nprint(foo())"
        chunks = chunk_text(code, unit="line", strip_empty=True)
        self.assertEqual(chunks, ["def foo():", "    return 42", "print(foo())"])

    def test_chunk_empty_input(self):
        self.assertEqual(chunk_text("", unit="word"), [])
        self.assertEqual(chunk_text("", unit="line"), [])

    def test_detect_unit(self):
        single_line = "Just one short sentence to memorize."
        multi_line = "line 1\nline 2\nline 3"
        self.assertEqual(detect_unit(single_line), "word")
        self.assertEqual(detect_unit(multi_line), "line")


if __name__ == "__main__":
    unittest.main()
