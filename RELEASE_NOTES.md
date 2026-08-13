# Release Notes

## Format

Each entry below records: SDK version, release date, supported branch and hardware, Linux kernel and U-Boot baseline, included image artifacts, known limitations, and major changes since the previous entry.

## Versioning Note

This file tracks two independent version numbers — don't conflate them:

- **SDK release tags** (`vX.Y.Z`, e.g. `v0.1.0` below) — this repository's own git tags/GitHub Releases.
- **Platform baseline version** (`v1.0` in the section right below) — `influx-yocto-base`'s own release numbering, quoted here for reference only.

## v0.1.0 — SDK Documentation & Examples Baseline

**Date:** 2026-07-30
**Tag:** [`v0.1.0`](https://github.com/InfluxTechnology/rexgen-smart-sdk/releases/tag/v0.1.0)
**Supported branch/hardware:** `influx-6.6.23`, `imx8mm-smart` (see [Platform Baseline Reference](#platform-baseline-reference-influx-yocto-base-v10) below)

First tagged snapshot of this repository. Included:

- self-contained `repo` manifest under [`manifest/`](manifest/README.md) — no separate visit to `influx-yocto-base` needed to sync source
- build, flashing, and application-SDK (`populate_sdk`) documentation — [docs/](docs/)
- device-verified examples with runnable Bash/Python/Node.js code for CAN (named pipe + SocketCAN), GNSS, accelerometer, gyroscope, ADC, and digital channels — [examples/](examples/README.md)
- support, security, and usage-notice policies — [SUPPORT.md](SUPPORT.md), [SECURITY.md](SECURITY.md), [EULA.md](EULA.md)

**Why `v0.1.0` and not `v1.0.0`:** several items are known-incomplete and are tracked as blockers to a `v1.0.0` release rather than silently shipped as done — see [Upcoming](#upcoming) below.

### Known Limitations

- The `rexgend` data-path protocol (named pipes and SocketCAN, for CAN/GNSS/IMU/ADC/digital channels) is documented and exampled in [examples/](examples/README.md). **By decision, no packaged client library/wrapper will be built on top of it** — applications are expected to talk to the pipes/sockets directly, as shown in the example code.
- `populate_sdk` (application SDK / cross-toolchain) output has not yet been published as a standalone downloadable artifact — build it locally per [docs/getting-started.md](docs/getting-started.md#building-the-application-sdk).
- **`influx-image-base` ships insecure default credentials (passwordless `tester` user, hardcoded `root` password, SSH enabled by default) — see [SECURITY.md](SECURITY.md#current-credential-posture-influx-image-base) before deploying any built image outside a lab environment.**
- [EULA.md](EULA.md) is an interim usage notice, not yet reviewed by legal/business ownership.

Mender OTA is confirmed working end-to-end on production devices — see [docs/mender-ota.md](docs/mender-ota.md); only a captured log/output example is still pending there, not a functional gap.

## Upcoming

Tracked blockers before a `v1.0.0` release:

- secure-by-default image variant or `.bbappend` (removes the passwordless `tester` user, requires a per-build `root` password instead of the shared default)
- `populate_sdk` toolchain installer published as a downloadable release artifact
- legal sign-off on [EULA.md](EULA.md)
- expanded CI beyond example lint (see below) — at minimum a scheduled/manual image build validation

## Platform Baseline Reference: `influx-yocto-base` v1.0

This section describes the `influx-6.6.23` platform baseline the SDK wraps (source: `influx-yocto-base`'s own release notes, its `v1.0` — not this repository's version number).

### Version

`influx-6.6.23`

### Supported Branch

`influx-6.6.23` (manifest `base.xml`)

### Supported Hardware

`imx8mm-smart` (Rexgen Smart, i.MX8MM)

### Platform Baseline

- Yocto distro: `fsl-imx-wayland` / `scarthgap`
- Linux kernel: `6.6.23`
- U-Boot: `2024.04`
- NXP BSP (`meta-imx`): `rel_imx_6.6.36_2.1.0`
- Mender OTA update support

### Included Artifacts

- `influx-image-base` (`.sdimg`, `.wic`, `.dtb`, `.bin` under `tmp/deploy/images/imx8mm-smart/`)
- `uuu-deploy.tgz` (flashing archive, produced by `deploy-image.sh`)

### Key Installed Packages / Features

- Networking/comms: `can-utils`, `iproute2`, `hostapd`, `dnsmasq`, `ppp`, `wvdial`, `openssh-sftp-server`, `murata-binaries`, `cyw-supplicant`/`cyw-hostapd`, `kernel-module-nxp-wlan`
- GPIO/hardware access: `libgpiod`, `libgpiod-tools`, `i2c-tools`, `mmc-utils`, `pciutils`
- Rexgen integration: `rexgen-core`, `wlan-manager`, `mender-artifact-info`, `mender-auth`, `mender-update`
- Diagnostics/dev tools: `gdbserver`, `htop`, `mc`, `screen`, `minicom`, `python3`/`python3-pip`, `auditd`

### Rexgen Device Features

- Socket control interface for ReXdesk app (ports 5053, 5054)
- Automatic RXD datalog upload to cloud (AWS S3, Google Cloud HMAC, Google Cloud Service Account)
- GNSS data logging support
- API service for remote functions (port 5051)
- Live CAN via SocketCAN
- Multi-partition support
- Passthrough mode
- CCP/XCP seedkey handlers (`.so`, `.lua`, `.sh`, `.py`, native binary, pre-loaded at startup)

### Notes

This file is updated for every published SDK candidate and release, and whenever the underlying `influx-yocto-base` branch/BSP baseline changes.
