from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from firmddle import inventory


class BinwalkRetryTests(unittest.TestCase):
    def test_run_binwalk_retries_when_run_as_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "firmware.bin"
            input_path.write_bytes(b"test")
            run_dir = Path(tmp) / "run"

            first = mock.Mock(returncode=1, stdout="", stderr="use '--run-as=root'")
            second = mock.Mock(returncode=0, stdout="ok", stderr="")

            with mock.patch.object(inventory, "find_tool", return_value="/usr/bin/binwalk"):
                with mock.patch.object(inventory, "run_cmd", side_effect=[first, second]) as run_cmd:
                    ok, text = inventory.run_binwalk(input_path, run_dir)

            self.assertTrue(ok)
            self.assertIn("--- retry with --run-as ---", text)
            self.assertEqual(run_cmd.call_count, 2)
            self.assertIn("--run-as=", run_cmd.call_args_list[1].args[0][2])


if __name__ == "__main__":
    unittest.main()
