# Refactoring Plan and Test Plan

## Refactoring Plan

The goal is to make this project usable by people who want firmware evidence
quickly, without first learning the old GUI Docker layout. The refactor keeps the
existing Docker/Ghidra assets, but moves the default workflow to a small
file-based CLI.

1. Add a Python CLI package named `firmddle`.
2. Provide `doctor`, `prepare`, `asm`, `hunt`, `report`, and `demo` commands.
3. Store all outputs in a run directory under `workspace/runs/`.
4. Keep raw evidence in plain files and JSONL so external agents can inspect it
   without a database.
5. Add a CLI Docker image that works without the Eclipse tarball.
6. Move the previous GUI workflow behind a `legacy-gui` Docker Compose profile.
7. Rewrite the README around the CLI quickstart and preserve old setup notes in
   a legacy document.
8. Pin the CLI Docker extractor stack to `binwalk v2.1.1` plus `sasquatch` so
   DD-WRT-style SquashFS extraction matches the legacy firmware-mod-kit path.

The first milestone intentionally does not add DeepSeek, GPT-OSS, MCP, or Ghidra
automation. Those should become optional layers after the base evidence pipeline
is stable.

## Test Plan

The tests cover three levels.

1. Unit tests verify keyword scanning, inventory generation, report generation,
   and the `doctor` command.
2. Native smoke tests run the bundled sample ELF through `demo` and confirm that
   `_analysis/findings.md` is produced.
3. Docker smoke tests build the CLI image and run the same demo in `/workspace`.

Manual checks after the automated tests should confirm that generated data stays
under `workspace/runs/`, ignored firmware extraction outputs are not committed,
and the legacy GUI service remains opt-in.
