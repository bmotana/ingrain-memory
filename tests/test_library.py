import unittest
import tempfile
import shutil
from pathlib import Path
from recall.core.library import LibraryManager


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.library = LibraryManager(custom_dir=Path(self.temp_dir))

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_builtin_samples_present(self):
        samples = self.library.get_all_samples()
        names = [s.name for s in samples]
        self.assertIn("data_viz", names)
        self.assertIn("invictus", names)

    def test_find_snippet(self):
        snip = self.library.find_snippet("DATA_VIZ")
        self.assertIsNotNone(snip)
        self.assertEqual(snip.category, "code")

    def test_save_and_retrieve_user_deck(self):
        self.library.save_user_deck(
            name="my_custom_code",
            content="print('hello world')",
            description="A test snippet",
            unit="line",
            language="python",
        )
        snip = self.library.find_snippet("my_custom_code")
        self.assertIsNotNone(snip)
        self.assertEqual(snip.content, "print('hello world')")
        self.assertEqual(snip.description, "A test snippet")


if __name__ == "__main__":
    unittest.main()
