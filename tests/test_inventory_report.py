from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from firmddle.inventory import build_inventory
from firmddle.io import analysis_dir, read_jsonl, write_jsonl
from firmddle.report import generate_report


class InventoryReportTests(unittest.TestCase):
    def test_prepare_indexes_directory_without_extraction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "firmware-root"
            source.mkdir()
            (source / "passwd").write_text("root:x:0:0:root:/root:/bin/sh\n", encoding="utf-8")
            run_dir = root / "run"

            summary = build_inventory(source, run_dir, extract=False)
            rows = read_jsonl(analysis_dir(run_dir) / "inventory.jsonl")

        self.assertEqual(summary["files"], 1)
        self.assertEqual(rows[0]["name"], "passwd")
        self.assertEqual(rows[0]["kind"], "config")

    def test_prepare_preserves_directory_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "firmware-root"
            source.mkdir()
            (source / "target").write_text("ok\n", encoding="utf-8")
            (source / "link").symlink_to("target")
            run_dir = root / "run"

            summary = build_inventory(source, run_dir, extract=False)

        self.assertEqual(summary["files"], 2)

    def test_report_generates_markdown_from_existing_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            adir = analysis_dir(run_dir)
            write_jsonl(
                adir / "inventory.jsonl",
                [
                    {
                        "kind": "elf",
                        "is_elf": True,
                        "name": "busybox",
                        "rel_path": "input/busybox",
                    }
                ],
            )
            write_jsonl(
                adir / "clues.jsonl",
                [
                    {
                        "category": "command_execution",
                        "keyword": "/bin/sh",
                        "evidence_file": "strings/busybox.strings.txt",
                        "line_no": 10,
                        "line": "/bin/sh",
                        "score": 4,
                    }
                ],
            )

            report = generate_report(run_dir)
            text = report.read_text(encoding="utf-8")

        self.assertIn("# firmddle Findings", text)
        self.assertIn("command_execution", text)
        self.assertIn("/bin/sh", text)


if __name__ == "__main__":
    unittest.main()
