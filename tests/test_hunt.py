from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from firmddle.hunt import hunt_backdoor_clues, scan_file
from firmddle.io import analysis_dir, read_jsonl


class HuntTests(unittest.TestCase):
    def test_scan_file_keeps_all_keywords_in_each_category(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            adir = analysis_dir(Path(tmp))
            evidence = adir / "strings" / "sample.strings.txt"
            evidence.parent.mkdir(parents=True)
            evidence.write_text(
                "admin password\n"
                "debug factory\n"
                "system('/bin/sh')\n"
                "nvram_get login\n",
                encoding="utf-8",
            )

            clues = scan_file(
                evidence,
                adir,
                {
                    "credential": ["admin", "password"],
                    "debug_or_magic": ["debug", "factory"],
                    "command_execution": ["system", "/bin/sh", "nc"],
                    "firmware_config": ["nvram_get", "login"],
                },
            )

        found = {(clue.category, clue.keyword) for clue in clues}
        self.assertIn(("credential", "admin"), found)
        self.assertIn(("credential", "password"), found)
        self.assertIn(("debug_or_magic", "debug"), found)
        self.assertIn(("debug_or_magic", "factory"), found)
        self.assertIn(("command_execution", "system"), found)
        self.assertIn(("command_execution", "/bin/sh"), found)
        self.assertNotIn(("command_execution", "nc"), found)
        self.assertIn(("firmware_config", "nvram_get"), found)
        self.assertIn(("firmware_config", "login"), found)

    def test_scan_file_uses_word_boundaries_for_plain_tokens(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            adir = analysis_dir(Path(tmp))
            evidence = adir / "imports" / "sample.readelf.txt"
            evidence.parent.mkdir(parents=True)
            evidence.write_text(
                "FUNC    GLOBAL ext_rtc_time_system\n"
                "FUNC    GLOBAL system\n"
                "FUNC    GLOBAL CConfigRefresh\n",
                encoding="utf-8",
            )

            clues = scan_file(evidence, adir, {"command_execution": ["system", "nc"]})

        found_lines = {(clue.keyword, clue.line) for clue in clues}
        self.assertIn(("system", "FUNC    GLOBAL system"), found_lines)
        self.assertNotIn(("system", "FUNC    GLOBAL ext_rtc_time_system"), found_lines)
        self.assertEqual([clue.keyword for clue in clues].count("nc"), 0)

    def test_command_execution_keywords_are_case_sensitive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            adir = analysis_dir(Path(tmp))
            evidence = adir / "imports" / "sample.readelf.txt"
            evidence.parent.mkdir(parents=True)
            evidence.write_text(
                "OS/ABI: UNIX - System V\n"
                "FUNC    GLOBAL system\n",
                encoding="utf-8",
            )

            clues = scan_file(evidence, adir, {"command_execution": ["system"]})

        self.assertEqual(1, len(clues))
        self.assertEqual("FUNC    GLOBAL system", clues[0].line)

    def test_hunt_writes_jsonl_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            adir = analysis_dir(run_dir)
            evidence = adir / "imports" / "toy.readelf.txt"
            evidence.parent.mkdir(parents=True)
            evidence.write_text("system\npopen\nadmin\n", encoding="utf-8")

            summary = hunt_backdoor_clues(run_dir)
            rows = read_jsonl(adir / "clues.jsonl")

        self.assertGreaterEqual(summary["clues"], 3)
        self.assertGreaterEqual(len(rows), 3)


if __name__ == "__main__":
    unittest.main()
