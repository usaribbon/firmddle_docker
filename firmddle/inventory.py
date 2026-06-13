from __future__ import annotations

import hashlib
import mimetypes
import os
import pwd
import shutil
from pathlib import Path

from .io import analysis_dir, ensure_dir, write_json, write_jsonl
from .tools import command_text, find_tool, run_cmd, TOOL_CANDIDATES


SCRIPT_EXTS = {".sh", ".bash", ".cgi", ".php", ".lua", ".py", ".pl", ".js"}
CONFIG_HINTS = {
    "passwd",
    "shadow",
    "group",
    "inittab",
    "rc.local",
    "authorized_keys",
    "crontab",
}


def sha256_file(path: Path, limit: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        remaining = limit
        while remaining > 0:
            chunk = f.read(min(65536, remaining))
            if not chunk:
                break
            h.update(chunk)
            remaining -= len(chunk)
    return h.hexdigest()


def file_description(path: Path) -> str:
    file_tool = find_tool(TOOL_CANDIDATES["file"])
    if not file_tool:
        guessed = mimetypes.guess_type(str(path))[0] or ""
        return guessed
    result = run_cmd([file_tool, "-b", str(path)], timeout=15)
    return command_text(result, max_chars=1000).strip()


def classify_file(path: Path, desc: str) -> str:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if "elf" in desc.lower():
        return "elf"
    if suffix in SCRIPT_EXTS:
        return "script"
    if name in CONFIG_HINTS or "/etc/" in str(path).lower():
        return "config"
    if suffix in {".pem", ".crt", ".cer", ".key", ".pub"}:
        return "key_or_cert"
    if suffix in {".html", ".htm", ".js", ".css"} or "/www/" in str(path).lower():
        return "web"
    if os.access(path, os.X_OK):
        return "executable_or_script"
    return "file"


def iter_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    skip_parts = {"_analysis", ".git"}
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_parts for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def copy_or_link_input(source: Path, run_dir: Path) -> Path:
    input_dir = ensure_dir(run_dir / "input")
    destination = input_dir / source.name
    if destination.exists():
        return destination
    if source.is_dir():
        shutil.copytree(source, destination, symlinks=True)
    else:
        shutil.copy2(source, destination)
    return destination


def run_binwalk(input_path: Path, run_dir: Path) -> tuple[bool, str]:
    binwalk = find_tool(TOOL_CANDIDATES["binwalk"])
    if not binwalk or input_path.is_dir():
        return False, "binwalk unavailable or input is a directory; skipped extraction"
    extracted = ensure_dir(run_dir / "extracted")
    command = [binwalk, "-eM", str(input_path), "-C", str(extracted)]
    result = run_cmd(command, timeout=1800)
    text = command_text(result)
    if result.returncode == 0 or "--run-as" not in text:
        return result.returncode == 0, text

    user = pwd.getpwuid(os.geteuid()).pw_name
    retry = [binwalk, "-eM", f"--run-as={user}", str(input_path), "-C", str(extracted)]
    retry_result = run_cmd(retry, timeout=1800)
    retry_text = command_text(retry_result)
    combined = text.rstrip() + "\n\n--- retry with --run-as ---\n" + retry_text
    return retry_result.returncode == 0, combined


def build_inventory(source: Path, run_dir: Path, *, extract: bool = True) -> dict:
    source = source.resolve()
    run_dir = run_dir.resolve()
    ensure_dir(run_dir)
    adir = analysis_dir(run_dir)

    local_input = copy_or_link_input(source, run_dir)
    extraction_ok = False
    extraction_log = "extraction disabled"
    if extract:
        extraction_ok, extraction_log = run_binwalk(local_input, run_dir)

    scan_roots = [run_dir / "input", run_dir / "extracted"]
    rows = []
    for root in scan_roots:
        if not root.exists():
            continue
        for path in iter_files(root):
            desc = file_description(path)
            rel = path.relative_to(run_dir)
            kind = classify_file(path, desc)
            rows.append(
                {
                    "path": str(path),
                    "rel_path": str(rel),
                    "name": path.name,
                    "size": path.stat().st_size,
                    "sha256_1m": sha256_file(path),
                    "file_type": desc,
                    "kind": kind,
                    "is_elf": kind == "elf",
                }
            )

    inventory_path = adir / "inventory.jsonl"
    write_jsonl(inventory_path, rows)
    summary = {
        "source": str(source),
        "run_dir": str(run_dir),
        "inventory": str(inventory_path),
        "files": len(rows),
        "elf_files": sum(1 for row in rows if row["is_elf"]),
        "extraction_ok": extraction_ok,
        "extraction_log": extraction_log[:4000],
    }
    write_json(adir / "prepare_summary.json", summary)
    return summary
