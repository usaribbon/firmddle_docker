from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .io import analysis_dir, read_jsonl, write_json, write_jsonl


DEFAULT_KEYWORDS = {
    "credential": [
        "admin",
        "root",
        "password",
        "passwd",
        "shadow",
        "authorized_keys",
        "secret",
        "token",
    ],
    "debug_or_magic": [
        "debug",
        "factory",
        "testmode",
        "backdoor",
        "superuser",
        "magic",
        "developer",
    ],
    "command_execution": [
        "/bin/sh",
        "telnetd",
        "dropbear",
        "system",
        "popen",
        "execve",
        "execl",
        "wget",
        "curl",
        "tftp",
        "nc",
    ],
    "firmware_config": [
        "nvram_get",
        "nvram_set",
        "uci",
        "ubus",
        "httpd",
        "cgi",
        "login",
        "auth",
    ],
}

SEVERITY = {
    "command_execution": 4,
    "credential": 3,
    "debug_or_magic": 2,
    "firmware_config": 2,
}


@dataclass
class Clue:
    category: str
    keyword: str
    evidence_file: str
    line_no: int
    line: str
    score: int

    def to_dict(self) -> dict:
        return {
            "category": self.category,
            "keyword": self.keyword,
            "evidence_file": self.evidence_file,
            "line_no": self.line_no,
            "line": self.line[:500],
            "score": self.score,
        }


def compile_keyword(keyword: str, category: str = "") -> re.Pattern[str]:
    escaped = re.escape(keyword)
    flags = 0 if category == "command_execution" else re.IGNORECASE
    if re.fullmatch(r"[A-Za-z0-9_]+", keyword):
        return re.compile(rf"\b{escaped}\b", flags)
    return re.compile(escaped, flags)


def evidence_files(adir: Path) -> list[Path]:
    targets: list[Path] = []
    for subdir in ("strings", "imports", "asm"):
        root = adir / subdir
        if root.exists():
            targets.extend(path for path in root.rglob("*") if path.is_file())
    inventory = adir / "inventory.jsonl"
    if inventory.exists():
        targets.append(inventory)
    return sorted(targets)


def scan_file(path: Path, adir: Path, keywords: dict[str, list[str]]) -> list[Clue]:
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return []
    rel = str(path.relative_to(adir))
    clues: list[Clue] = []
    lowered_keywords = {
        category: [(kw, compile_keyword(kw, category)) for kw in words]
        for category, words in keywords.items()
    }
    for line_no, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        for category, pairs in lowered_keywords.items():
            for keyword, pattern in pairs:
                if pattern.search(line):
                    clues.append(
                        Clue(
                            category=category,
                            keyword=keyword,
                            evidence_file=rel,
                            line_no=line_no,
                            line=line.strip(),
                            score=SEVERITY.get(category, 1),
                        )
                    )
    return clues


def hunt_backdoor_clues(run_dir: Path) -> dict:
    run_dir = run_dir.resolve()
    adir = analysis_dir(run_dir)
    files = evidence_files(adir)
    clues: list[Clue] = []
    for path in files:
        clues.extend(scan_file(path, adir, DEFAULT_KEYWORDS))

    clue_rows = [clue.to_dict() for clue in sorted(clues, key=lambda c: (-c.score, c.evidence_file, c.line_no))]
    write_jsonl(adir / "clues.jsonl", clue_rows)
    summary = {
        "run_dir": str(run_dir),
        "evidence_files": len(files),
        "clues": len(clue_rows),
        "categories": {
            category: sum(1 for row in clue_rows if row["category"] == category)
            for category in DEFAULT_KEYWORDS
        },
    }
    write_json(adir / "hunt_summary.json", summary)
    return summary


def load_top_clues(run_dir: Path, limit: int = 100) -> list[dict]:
    adir = analysis_dir(run_dir)
    rows = read_jsonl(adir / "clues.jsonl")
    return sorted(rows, key=lambda row: (-int(row.get("score", 0)), row.get("evidence_file", ""), row.get("line_no", 0)))[:limit]
