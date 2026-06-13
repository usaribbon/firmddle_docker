from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .asm import generate_artifacts
from .hunt import hunt_backdoor_clues
from .inventory import build_inventory
from .report import generate_report
from .tools import collect_tool_status


def find_demo_sample() -> Path | None:
    rel = Path("raw_firmwares") / "raw_easy" / "binary1"
    candidates = [
        Path(__file__).resolve().parents[1] / rel,
        Path.cwd() / rel,
        Path("/opt/firmddle") / rel,
        Path("/repo") / rel,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def cmd_doctor(args: argparse.Namespace) -> int:
    statuses = collect_tool_status()
    print("firmddle doctor")
    missing_required = False
    for status in statuses:
        marker = "OK" if status.available else ("MISSING" if status.required else "optional-missing")
        path = status.path or "-"
        req = "required" if status.required else "optional"
        print(f"{marker:16} {status.name:14} {req:8} {path}")
        if status.required and not status.available:
            missing_required = True
    if missing_required and args.strict:
        return 1
    return 0


def cmd_prepare(args: argparse.Namespace) -> int:
    summary = build_inventory(Path(args.input), Path(args.out), extract=not args.no_extract)
    print(f"prepared: {summary['run_dir']}")
    print(f"files={summary['files']} elf_files={summary['elf_files']} extraction_ok={summary['extraction_ok']}")
    return 0


def cmd_asm(args: argparse.Namespace) -> int:
    summary = generate_artifacts(Path(args.run_dir), max_files=args.max_files)
    print(f"asm artifacts: {summary['run_dir']}")
    print(
        "processed={processed} elf_files={elf_files} disassembly_success={disassembly_success}".format(
            **summary
        )
    )
    if not summary.get("disassembler"):
        print("warning: no disassembler found; strings/readelf artifacts may still exist", file=sys.stderr)
    return 0


def cmd_hunt(args: argparse.Namespace) -> int:
    if args.target != "backdoor":
        print(f"unsupported target: {args.target}", file=sys.stderr)
        return 2
    summary = hunt_backdoor_clues(Path(args.run_dir))
    print(f"hunt: {summary['run_dir']}")
    print(f"evidence_files={summary['evidence_files']} clues={summary['clues']}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    path = generate_report(Path(args.run_dir), limit=args.limit)
    print(f"report: {path}")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    sample = find_demo_sample()
    if sample is None:
        print("demo sample not found: raw_firmwares/raw_easy/binary1", file=sys.stderr)
        return 1
    run_dir = Path(args.out)
    build_inventory(sample, run_dir, extract=False)
    generate_artifacts(run_dir, max_files=args.max_files)
    hunt_backdoor_clues(run_dir)
    report = generate_report(run_dir, limit=25)
    print(f"demo complete: {report}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="firmddle", description="Firmware evidence extraction and clue hunting CLI.")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="check external tool availability")
    doctor.add_argument("--strict", action="store_true", help="exit non-zero when a required tool is missing")
    doctor.set_defaults(func=cmd_doctor)

    prepare = sub.add_parser("prepare", help="extract firmware and build inventory")
    prepare.add_argument("input", help="firmware image or already extracted directory")
    prepare.add_argument("--out", required=True, help="run output directory")
    prepare.add_argument("--no-extract", action="store_true", help="skip binwalk extraction")
    prepare.set_defaults(func=cmd_prepare)

    asm = sub.add_parser("asm", help="generate strings/readelf/disassembly artifacts for ELF files")
    asm.add_argument("run_dir", help="run directory created by prepare")
    asm.add_argument("--max-files", type=int, default=None, help="limit ELF files for smoke tests")
    asm.set_defaults(func=cmd_asm)

    hunt = sub.add_parser("hunt", help="scan analysis artifacts for vulnerability clues")
    hunt.add_argument("run_dir", help="run directory created by prepare")
    hunt.add_argument("--target", default="backdoor", help="hunt target; currently only backdoor")
    hunt.set_defaults(func=cmd_hunt)

    report = sub.add_parser("report", help="create findings markdown")
    report.add_argument("run_dir", help="run directory created by prepare")
    report.add_argument("--limit", type=int, default=50, help="number of clues to include")
    report.set_defaults(func=cmd_report)

    demo = sub.add_parser("demo", help="run a small demo using the bundled sample ELF")
    demo.add_argument("--out", default="workspace/runs/demo", help="demo run output directory")
    demo.add_argument("--max-files", type=int, default=1, help="limit ELF files")
    demo.set_defaults(func=cmd_demo)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
