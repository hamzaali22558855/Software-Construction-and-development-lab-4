import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import main as app
from validation import validate_mark
from calculations import calculate_total, calculate_average, calculate_grade


def run_app(inputs):
    out = io.StringIO()
    with patch("builtins.input", side_effect=inputs), redirect_stdout(out):
        app.main()
    return out.getvalue()


class TestValidation(unittest.TestCase):
    def test_valid(self):
        for m in (0, 50, 100, 75.5):
            self.assertTrue(validate_mark(m))

    def test_invalid(self):
        for m in (-5, -0.1, 100.1, 105):
            self.assertFalse(validate_mark(m))


class TestCalculations(unittest.TestCase):
    def test_total_average(self):
        self.assertEqual(calculate_total([75, 82, 68]), 225)
        self.assertEqual(calculate_average([75, 82, 68]), 75)

    def test_grade_boundaries(self):
        cases = {80: "A", 79.99: "B", 70: "B", 69.99: "C", 60: "C",
                 59.99: "D", 50: "D", 49.99: "F", 0: "F", 100: "A"}
        for avg, grade in cases.items():
            self.assertEqual(calculate_grade(avg), grade, avg)


class TestApplication(unittest.TestCase):
    def test_normal(self):
        out = run_app(["Ali", "75", "82", "68"])
        for line in ("Name: Ali", "Total: 225.0", "Average: 75.0", "Grade: B"):
            self.assertIn(line, out)

    def test_boundaries(self):
        for mark, grade in ((50, "D"), (60, "C"), (70, "B"), (80, "A")):
            out = run_app(["X", str(mark), str(mark), str(mark)])
            self.assertIn(f"Grade: {grade}", out)

    def test_invalid_marks_reprompt(self):
        out = run_app(["Bad", "-5", "105", "90", "80", "70"])
        self.assertEqual(out.count("Invalid marks. Enter 0-100."), 2)
        self.assertIn("Total: 240.0", out)

    def test_second_student(self):
        out = run_app(["Sara", "40", "45", "30"])
        self.assertIn("Grade: F", out)
        self.assertIn("Total: 115.0", out)


if __name__ == "__main__":
    unittest.main()
