# firmddle_docker

Firmware evidence extraction and backdoor-clue hunting toolkit.

Status: `0.1.0-alpha` research preview.

This repository is being refactored from a GUI-first Ghidra Docker image into a
CLI-first workflow that can be used from Docker or a local Python environment.
The current CLI does not require a database. It creates a file-based analysis
workspace containing an inventory, strings/import/disassembly artifacts, clue
JSONL, and a Markdown report.

## What It Does

`firmddle` is a preparation layer for firmware reverse engineering and
vulnerability hunting. It helps you turn firmware images or extracted firmware
directories into evidence that another analyst, script, or LLM agent can inspect.

The first refactored version focuses on three practical tasks:

- Build an inventory of files inside a firmware image or extracted rootfs.
- Generate local evidence from ELF files using `strings`, `readelf`, and
  `objdump`.
- Search for backdoor-oriented clues such as credentials, debug strings,
  command execution sinks, and firmware configuration APIs.

Ghidra is still useful for deeper semantic analysis. The old GUI environment is
kept as a legacy option, but the default path is now a smaller CLI workflow.

## Quick Start With Docker

Build the CLI image:

```bash
docker compose build firmddle
```

Run the bundled demo:

```bash
docker compose run --rm firmddle demo --out /workspace/runs/demo
```

Analyze your own firmware:

```bash
mkdir -p workspace/input workspace/runs
cp /path/to/firmware.bin workspace/input/

docker compose run --rm firmddle prepare /workspace/input/firmware.bin --out /workspace/runs/firmware
docker compose run --rm firmddle asm /workspace/runs/firmware
docker compose run --rm firmddle hunt /workspace/runs/firmware --target backdoor
docker compose run --rm firmddle report /workspace/runs/firmware
```

Open the report at:

```text
workspace/runs/firmware/_analysis/findings.md
```

## Quick Start Without Docker

Native installs require Python 3.10 or newer.

Install the Python package in editable mode:

```bash
python3 -m pip install -e .
```

Check available external tools:

```bash
firmddle doctor
```

Run the demo:

```bash
firmddle demo --out workspace/runs/demo
```

For best native results, install these command-line tools on the host:

```text
file strings readelf objdump binwalk
```

On Debian/Ubuntu, `binutils-multiarch` is recommended because firmware ELF files
often target ARM, MIPS, or other non-host architectures.

The Docker image intentionally pins `binwalk` to `v2.1.1` and includes
`sasquatch`. This matches the legacy firmware-mod-kit behavior more closely for
older DD-WRT-style SquashFS images than Ubuntu's default Binwalk package.

## CLI Commands

```bash
firmddle doctor
firmddle prepare <firmware-or-directory> --out <run-dir>
firmddle asm <run-dir>
firmddle hunt <run-dir> --target backdoor
firmddle report <run-dir>
firmddle demo
```

The generated run directory looks like this:

```text
workspace/runs/example/
|-- input/
|-- extracted/
`-- _analysis/
    |-- inventory.jsonl
    |-- prepare_summary.json
    |-- strings/
    |-- imports/
    |-- asm/
    |-- clues.jsonl
    |-- hunt_summary.json
    `-- findings.md
```

## Legacy Ghidra GUI

The previous Ghidra GUI Docker workflow is still available, but it is no longer
the default path. It requires the Eclipse tarball described in the old setup
guide.

```bash
docker compose --profile legacy-gui build ghidra-gui
docker compose --profile legacy-gui up -d ghidra-gui
```

Then open:

```text
http://127.0.0.1:8080/
```

See [docs/legacy_gui.md](docs/legacy_gui.md) for the legacy workflow and current
caveats.

## Development

Run the unit tests:

```bash
python3 -m unittest discover -s tests
```

Run a smoke test:

```bash
python3 -m firmddle.cli demo --out workspace/runs/demo --max-files 1
```

See [docs/refactor_plan.md](docs/refactor_plan.md) for the refactoring plan and
test plan.

Before cutting a release, run:

```bash
python3 -m unittest discover -s tests
docker compose build firmddle
docker compose run --rm firmddle doctor
docker compose run --rm firmddle demo --out /workspace/runs/release-demo --max-files 1
docker compose run --rm firmddle prepare /repo/raw_firmwares/raw/binary2/binary2.bin --out /workspace/runs/release-binary2
```

The `binary2.bin` smoke test should extract successfully and find 131 ELF files.

## Known Limitations

The current release is a triage/evidence-preparation layer, not a complete
vulnerability proof system. See
[docs/known_limitations.md](docs/known_limitations.md) for extraction,
accuracy, scale, native-run, and third-party build caveats.

## License

The firmddle source code is licensed under Apache License 2.0. Docker images and
legacy workflows may install or interoperate with third-party tools such as
Binwalk, sasquatch/SquashFS tools, Ghidra, and angr. Those tools retain their
upstream licenses. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Ethics

Use this toolkit only on firmware you own, are authorized to test, or are
analyzing for legitimate research and defensive purposes. The clue scanner is a
triage aid, not a vulnerability proof. Findings should be manually validated
against code, configuration, call sites, and runtime behavior before disclosure.
