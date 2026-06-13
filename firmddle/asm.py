from __future__ import annotations

import hashlib
from pathlib import Path

from .io import analysis_dir, ensure_dir, read_jsonl, safe_slug, write_json
from .tools import command_text, find_tool, run_cmd, TOOL_CANDIDATES


def _artifact_name(rel_path: str) -> str:
    digest = hashlib.sha1(rel_path.encode("utf-8")).hexdigest()[:10]
    return f"{safe_slug(rel_path)}.{digest}"


def _disassembler() -> tuple[str | None, list[str]]:
    llvm = find_tool(TOOL_CANDIDATES["llvm-objdump"])
    if llvm:
        return llvm, [llvm, "-d"]
    objdump = find_tool(TOOL_CANDIDATES["objdump"])
    if objdump:
        return objdump, [objdump, "-d"]
    return None, []


def generate_artifacts(run_dir: Path, *, max_files: int | None = None) -> dict:
    run_dir = run_dir.resolve()
    adir = analysis_dir(run_dir)
    inventory = read_jsonl(adir / "inventory.jsonl")
    elf_rows = [row for row in inventory if row.get("is_elf")]
    if max_files is not None:
        elf_rows = elf_rows[:max_files]

    strings_tool = find_tool(TOOL_CANDIDATES["strings"])
    readelf_tool = find_tool(TOOL_CANDIDATES["readelf"])
    disasm_tool, disasm_base = _disassembler()

    strings_dir = ensure_dir(adir / "strings")
    imports_dir = ensure_dir(adir / "imports")
    asm_dir = ensure_dir(adir / "asm")
    logs_dir = ensure_dir(adir / "logs")

    processed = 0
    disasm_ok = 0
    for row in elf_rows:
        path = Path(row["path"])
        if not path.exists():
            continue
        name = _artifact_name(row["rel_path"])
        if strings_tool:
            result = run_cmd([strings_tool, "-a", str(path)], timeout=120)
            (strings_dir / f"{name}.strings.txt").write_text(command_text(result, 2_000_000), encoding="utf-8")
        if readelf_tool:
            result = run_cmd([readelf_tool, "-h", "-sW", "-d", "-rW", str(path)], timeout=120)
            (imports_dir / f"{name}.readelf.txt").write_text(command_text(result, 2_000_000), encoding="utf-8")
        if disasm_tool:
            result = run_cmd(disasm_base + [str(path)], timeout=180)
            text = command_text(result, 4_000_000)
            (asm_dir / f"{name}.asm.txt").write_text(text, encoding="utf-8")
            if result.returncode == 0:
                disasm_ok += 1
            else:
                (logs_dir / f"{name}.disasm.err.txt").write_text(text, encoding="utf-8")
        processed += 1

    summary = {
        "run_dir": str(run_dir),
        "elf_files": len(elf_rows),
        "processed": processed,
        "strings_tool": strings_tool,
        "readelf_tool": readelf_tool,
        "disassembler": disasm_tool,
        "disassembly_success": disasm_ok,
    }
    write_json(adir / "asm_summary.json", summary)
    return summary
