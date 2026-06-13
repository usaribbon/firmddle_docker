# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0-alpha] - 2026-06-13

### Added

- Added the `firmddle` Python CLI with `doctor`, `prepare`, `asm`, `hunt`,
  `report`, and `demo` commands.
- Added a Docker-first CLI workflow that writes analysis artifacts under a
  file-based run directory.
- Added firmware inventory, extraction summaries, ELF strings, imports,
  disassembly artifacts, clue JSONL, and Markdown reporting.
- Added a backdoor-oriented clue scanner for credentials, debug interfaces,
  command execution sinks, and firmware configuration APIs.
- Added tests for CLI behavior, extraction summaries, report generation, and
  clue matching.
- Added release documentation for licensing, security reporting, known
  limitations, and legacy GUI usage.

### Changed

- Moved the previous GUI-oriented Ghidra workflow behind the `legacy-gui` Docker
  Compose profile.
- Pinned the CLI Docker image to Binwalk `v2.1.1` and included sasquatch to
  preserve compatibility with older DD-WRT-style SquashFS images.

### Known Limitations

- The current clue scanner is heuristic and requires manual validation.
- The first release does not yet include a full Ghidra, MCP, or LLM agent loop.
- Native host runs depend on the user's installed reverse-engineering tools.
