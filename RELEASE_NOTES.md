# Release Notes

## Current Status

This file is the release notes baseline for the first Rexgen Smart SDK release prepared with minimal structural changes on top of the current Yocto-based platform flow.

## Release Template

Each SDK release should record at minimum:

- SDK version
- release date
- supported branch
- supported hardware revisions
- Linux kernel baseline
- U-Boot baseline
- image artifacts included
- known limitations
- major fixes or changes

## v1.0 (Underlying Platform Baseline)

This describes the `influx-6.6.23` platform baseline the SDK currently wraps (source: `influx-yocto-base` release notes). SDK-specific packaging on top of this baseline is still to be tagged — see "SDK Packaging" below.

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

### Known Limitations

- No dedicated SDK version tag yet — this baseline is tracked via the manifest files under [`manifest/`](manifest/README.md) (mirrored from `influx-yocto-base`'s `influx-6.6.23` branch), not as a separate SDK release artifact
- Public API/wrapper boundary for Rexgen Core interfaces is still being documented (see [README.md](README.md#hardware-interfaces))
- `populate_sdk` (application SDK / cross-toolchain) output has not yet been published as a standalone downloadable artifact — build it locally per [docs/getting-started.md](docs/getting-started.md#building-the-application-sdk)
- **`influx-image-base` ships insecure default credentials (passwordless `tester` user, hardcoded `root` password, SSH enabled by default) — see [SECURITY.md](SECURITY.md#current-credential-posture-influx-image-base) before deploying any built image outside a lab environment**

## SDK Packaging

`TBD` — first SDK-specific tag/release (`vX.Y.Z`) covering this repository's documentation and any SDK-only tooling on top of the `influx-6.6.23` baseline above.

### Notes

This file should be updated for every published SDK candidate and release, and whenever the underlying `influx-yocto-base` branch/BSP baseline changes.
