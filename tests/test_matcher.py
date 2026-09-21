import unittest
from recall.core.matcher import check_match, normalize_string


class TestMatcher(unittest.TestCase):
    def test_exact_match(self):
        expected = ["plt.figure(figsize=(9, 5))", "sns.set_style('whitegrid')"]
        actual = ["plt.figure(figsize=(9, 5))", "sns.set_style('whitegrid')"]
        result = check_match(expected, actual)
        self.assertTrue(result.is_match)
        self.assertAlmostEqual(result.similarity, 1.0)

    def test_case_insensitive_match(self):
        expected = ["The Quick Brown Fox"]
        actual = ["the quick brown fox"]
        res_strict = check_match(expected, actual, case_sensitive=True)
        res_loose = check_match(expected, actual, case_sensitive=False)
        self.assertFalse(res_strict.is_match)
        self.assertTrue(res_loose.is_match)

    def test_ignore_whitespace(self):
        expected = ["counts[word]   =  1"]
        actual = ["counts[word] = 1"]
        res_strict = check_match(expected, actual, ignore_whitespace=False)
        res_loose = check_match(expected, actual, ignore_whitespace=True)
        self.assertFalse(res_strict.is_match)
        self.assertTrue(res_loose.is_match)

    def test_mismatch_detection(self):
        expected = ["line 1", "line 2", "line 3"]
        actual = ["line 1", "wrong line", "line 3"]
        result = check_match(expected, actual)
        self.assertFalse(result.is_match)
        self.assertIn("Mismatch at item 2", result.error_summary)

    def test_missing_line_detection(self):
        expected = ["line 1", "line 2"]
        actual = ["line 1"]
        result = check_match(expected, actual)
        self.assertFalse(result.is_match)
        self.assertIn("Missing 1 line", result.error_summary)


if __name__ == "__main__":
    unittest.main()
