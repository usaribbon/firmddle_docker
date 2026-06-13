# Legacy Ghidra GUI Workflow

This document keeps the original GUI-oriented workflow for users who still need
the old desktop environment. The recommended default workflow is now the
`firmddle` CLI described in the top-level README.

## Setup

Install Docker and download the Eclipse tarball:

```text
eclipse-committers-2022-06-R-linux-gtk-x86_64.tar.gz
```

Place it under:

```text
raw_firmwares/eclipse/
```

Build and start the GUI service:

```bash
docker compose --profile legacy-gui build ghidra-gui
docker compose --profile legacy-gui up -d ghidra-gui
```

Open the browser UI:

```text
http://127.0.0.1:8080/
```

The repository directory `raw_firmwares/` is mounted into the container as:

```text
/mnt/raw_firmwares/
```

## Original Flow

Place firmware images under:

```text
raw_firmwares/raw/
```

Inside the container, run the firmware-mod-kit extraction script:

```bash
/root/firmware-mod-kit/extract_elf.sh
```

Extracted files are written to:

```text
raw_firmwares/extracted/
```

The old Ghidra import flow used:

```bash
/root/firmware-mod-kit/import_elf_ghidra.sh
```

Ghidra projects were saved under:

```text
raw_firmwares/ghidraprj/
```

## Current Caveats

The old Dockerfile still expects the Eclipse archive to exist locally, so a
plain `docker compose build` is not enough for the legacy GUI image. In the
previously inspected container, Ghidra itself was available, but older Java
scripts did not compile cleanly against Ghidra 11.2.1 APIs. Treat the legacy GUI
path as a compatibility environment, not the new default interface.
