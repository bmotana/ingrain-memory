import unittest
from recall.core.session import RecallSession


class TestSession(unittest.TestCase):
    def test_session_initialization(self):
        chunks = ["word1", "word2", "word3"]
        session = RecallSession(chunks, unit="word")
        self.assertEqual(session.current_level, 1)
        self.assertEqual(session.total_levels, 3)
        self.assertEqual(session.current_revealed_chunks, ["word1"])
        self.assertFalse(session.is_completed)

    def test_session_progression(self):
        chunks = ["line1", "line2"]
        session = RecallSession(chunks, unit="line")
        session.record_attempt(True)
        advanced = session.advance()
        self.assertTrue(advanced)
        self.assertEqual(session.current_level, 2)
        self.assertEqual(session.current_revealed_chunks, ["line1", "line2"])

        session.record_attempt(True)
        completed = not session.advance()
        self.assertTrue(completed)
        self.assertTrue(session.is_completed)

    def test_hint_generation(self):
        chunks = ["elephant"]
        session = RecallSession(chunks, unit="word")
        hint = session.get_hint()
        self.assertTrue(hint.startswith("e"))
        self.assertTrue(hint.endswith("t"))
        self.assertIn("_", hint)

    def test_stats_calculation(self):
        chunks = ["a", "b"]
        session = RecallSession(chunks, unit="word")
        session.record_attempt(False)
        session.record_attempt(True)
        session.advance()
        session.record_attempt(True)
        session.advance()

        stats = session.get_stats()
        self.assertEqual(stats.total_levels, 2)
        self.assertEqual(stats.total_attempts, 3)
        self.assertEqual(stats.successful_attempts, 2)
        self.assertGreater(stats.accuracy_percentage, 60.0)


if __name__ == "__main__":
    unittest.main()
