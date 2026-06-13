from __future__ import annotations

from collections import Counter
from pathlib import Path

from .hunt import load_top_clues
from .io import analysis_dir, read_jsonl


def generate_report(run_dir: Path, *, limit: int = 50) -> Path:
    run_dir = run_dir.resolve()
    adir = analysis_dir(run_dir)
    inventory = read_jsonl(adir / "inventory.jsonl")
    clues = load_top_clues(run_dir, limit=limit)
    category_counts = Counter(row.get("category", "unknown") for row in read_jsonl(adir / "clues.jsonl"))
    kinds = Counter(row.get("kind", "unknown") for row in inventory)

    lines = [
        "# firmddle Findings",
        "",
        f"Run directory: `{run_dir}`",
        "",
        "## Corpus Summary",
        "",
        f"- Files indexed: {len(inventory)}",
        f"- ELF files: {sum(1 for row in inventory if row.get('is_elf'))}",
        f"- Clues found: {sum(category_counts.values())}",
        "",
        "## File Kinds",
        "",
    ]
    for kind, count in kinds.most_common():
        lines.append(f"- {kind}: {count}")
    lines.extend(["", "## Backdoor Clue Categories", ""])
    for category, count in category_counts.most_common():
        lines.append(f"- {category}: {count}")
    lines.extend(["", "## Top Evidence", ""])

    if not clues:
        lines.append("No clues were found. Run `firmddle asm` and `firmddle hunt` first.")
    else:
        for idx, clue in enumerate(clues, start=1):
            lines.extend(
                [
                    f"### {idx}. {clue.get('category')} / `{clue.get('keyword')}`",
                    "",
                    f"- Evidence: `{clue.get('evidence_file')}:{clue.get('line_no')}`",
                    f"- Score: {clue.get('score')}",
                    "",
                    "```text",
                    str(clue.get("line", ""))[:1000],
                    "```",
                    "",
                ]
            )

    report_path = adir / "findings.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path
