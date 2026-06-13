# Third-Party Notices

This repository contains firmddle source code and Docker/build instructions for
external reverse-engineering tools. The firmddle source code is licensed under
Apache-2.0. Third-party tools keep their upstream licenses.

This file is a best-effort notice list for the release tree. If you redistribute
a built Docker image, also review the package licenses inside that image.

## Docker CLI Image

- Binwalk is installed from `ReFirmLabs/binwalk` at tag `v2.1.1`. Binwalk is
  distributed by its upstream project under the MIT License.
- sasquatch is built from `devttys0/sasquatch` at commit
  `bd864a1b037bf57ca7d64a292a60ba0d6459611f`. sasquatch patches and builds
  SquashFS tooling, so its upstream notices and the SquashFS tool licenses
  apply.
- SquashFS tools 4.3 are downloaded during the Docker build. SquashFS tools are
  distributed by their upstream project under GPL-family terms.
- Ubuntu/Debian packages installed by the Dockerfile, such as `binutils`,
  `file`, `gcc`, `python3`, `p7zip`, and `squashfs-tools`, retain their package
  licenses from the distribution.

## Legacy Ghidra GUI Workflow

- Ghidra is licensed under Apache License 2.0.

Copyright 2021 National Security Agency

Licensed under the Apache License, Version 2.0. You may obtain a copy at
<http://www.apache.org/licenses/LICENSE-2.0>.

The legacy GUI workflow is kept for compatibility and is not the default CLI
path.

## Legacy angr Scripts

Some historical scripts in `raw_firmwares/angr/` refer to angr. angr is licensed
under the BSD 2-clause "Simplified" License.

Copyright (c) 2015-2022, The Angr Team
All rights reserved.

For the full license text, see the upstream angr project:
<https://github.com/angr/angr/blob/master/LICENSE>.
