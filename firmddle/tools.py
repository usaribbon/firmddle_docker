from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


BINWALK_CANDIDATES = (
    "binwalk",
    "/root/firmware-mod-kit/src/binwalk-2.1.1/src/scripts/binwalk",
)

GHIDRA_CANDIDATES = (
    "analyzeHeadless",
    "/root/firmusa/ghidra_11.2.1_PUBLIC/support/analyzeHeadless",
    "/root/firmusa/ghidra_10.1.5_PUBLIC/support/analyzeHeadless",
)

TOOL_CANDIDATES = {
    "binwalk": BINWALK_CANDIDATES,
    "file": ("file",),
    "strings": ("strings",),
    "readelf": ("readelf",),
    "objdump": ("objdump",),
    "llvm-objdump": ("llvm-objdump",),
    "ghidra": GHIDRA_CANDIDATES,
    "java": ("java",),
    "sasquatch": ("sasquatch",),
}


@dataclass(frozen=True)
class ToolStatus:
    name: str
    path: str | None
    required: bool

    @property
    def available(self) -> bool:
        return self.path is not None


def find_tool(candidates: tuple[str, ...]) -> str | None:
    for candidate in candidates:
        if os.sep in candidate:
            path = Path(candidate)
            try:
                if path.exists() and os.access(path, os.X_OK):
                    return str(path)
            except OSError:
                continue
            continue
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    return None


def collect_tool_status() -> list[ToolStatus]:
    required = {"file", "strings", "readelf"}
    return [
        ToolStatus(name, find_tool(candidates), name in required)
        for name, candidates in TOOL_CANDIDATES.items()
    ]


def require_tool(name: str) -> str:
    path = find_tool(TOOL_CANDIDATES[name])
    if not path:
        raise RuntimeError(f"required tool not found: {name}")
    return path


def run_cmd(
    args: list[str],
    *,
    cwd: Path | None = None,
    timeout: int | None = None,
    check: bool = False,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=check,
    )


def command_text(result: subprocess.CompletedProcess[str], max_chars: int = 20000) -> str:
    text = ""
    if result.stdout:
        text += result.stdout
    if result.stderr:
        if text and not text.endswith("\n"):
            text += "\n"
        text += result.stderr
    return text[:max_chars]
