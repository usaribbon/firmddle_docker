# Known Limitations

firmddle is a triage and evidence-preparation tool. It helps analysts collect
firmware evidence, but it does not prove that a vulnerability or backdoor is
exploitable.

## Analysis Accuracy

The current `hunt` command is heuristic. It can miss vulnerabilities whose
evidence is spread across several functions, generated dynamically, encrypted,
or hidden behind unusual control flow. It can also produce false positives when
a suspicious string or API is present but not reachable in an exploitable path.

## Extraction Coverage

Firmware extraction depends on Binwalk, sasquatch, and the archive/file-system
tools available in the runtime environment. The Docker image pins Binwalk
`v2.1.1` and builds sasquatch for legacy compatibility, but unusual compression
formats, encrypted partitions, vendor containers, or damaged images may still
require manual unpacking.

## Native Runs

The native Python package does not bundle Binwalk, sasquatch, `objdump`,
`readelf`, or `strings`. Native runs are useful for development, but release
comparisons should use the Docker image when reproducibility matters.

## Scope Of The First CLI Release

The first refactored release does not yet provide a database, a full-text index,
Ghidra function graph export, MCP integration, or an LLM-driven firmware-wide
agent. The generated files are intentionally simple so that future agents can
consume them without requiring a service.

## Scale

Large firmware images can produce many extracted files and large disassembly
outputs. The current workflow writes plain files under a run directory and does
not yet include retention policies, deduplication, or incremental indexing.

## Third-Party Build Inputs

The Docker build downloads some third-party sources at build time. Important
versions are pinned where practical, but availability of upstream archives and
distribution packages can still affect rebuilds.
