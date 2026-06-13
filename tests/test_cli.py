from __future__ import annotations

import io
import unittest
from contextlib import redirect_stdout

from firmddle.cli import main


class CliTests(unittest.TestCase):
    def test_doctor_runs_without_strict_failure(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            rc = main(["doctor"])

        self.assertEqual(rc, 0)
        self.assertIn("firmddle doctor", output.getvalue())


if __name__ == "__main__":
    unittest.main()
