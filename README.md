# Rexgen Smart SDK

[![Lint examples & manifest](https://github.com/InfluxTechnology/rexgen-smart-sdk/actions/workflows/lint-examples.yml/badge.svg)](https://github.com/InfluxTechnology/rexgen-smart-sdk/actions/workflows/lint-examples.yml)

`Rexgen Smart SDK` is the official development package for building Linux-side software on Rexgen Smart devices. It provides the documented build flow, platform integration path and example starting points needed to build images, flash devices and develop applications on the i.MX8 Linux host.

This repository is the single entry point for Rexgen Smart Linux development: source sync, build, flash, application SDK, and hardware-interface documentation on top of the existing Yocto-based platform flow.

## What Is Rexgen Smart SDK

`Rexgen Smart SDK` is intended for internal developers, integration engineers and approved partners who need to:

- build supported Rexgen Smart Linux images
- flash supported Rexgen Smart hardware
- run supported examples
- develop Linux-side applications for the i.MX8 host
- interact with Rexgen Core through documented and supported platform interfaces

## Version Baseline

This SDK is built on the `influx-6.6.23` release stream. Wherever a version needs to be quoted, use these four values together — they are not interchangeable:

| Component | Value |
|---|---|
| SDK release stream / repo branch | `influx-6.6.23` |
| Linux kernel | `6.6.23` |
| U-Boot | `2024.04` |
| Yocto distro | `fsl-imx-wayland` (`scarthgap`) |
| NXP BSP baseline (`meta-imx`) | `rel_imx_6.6.36_2.1.0` (`scarthgap-6.6.36-2.1.0`) |

Rule of thumb for the docs and for support requests:

- `influx-6.6.23` identifies the Rexgen-supported release stream (the branch/manifest you check out).
- `rel_imx_6.6.36_2.1.0` identifies the NXP i.MX BSP layer pinned underneath it (`meta-imx`).

Always state both when reporting an issue or describing a build.

## Supported

- supported Rexgen Smart Linux image builds
- documented Yocto-based build flow
- Linux-side software development on the i.MX8 host
- supported platform integration flows
- supported hardware, branch and release scope defined by release documentation (see [SUPPORT.md](SUPPORT.md))

See [examples/](examples/README.md) for device-verified CAN, IMU/ADC/Digital, and GNSS examples.

## Not Supported

- Rexgen Standalone firmware development
- undocumented internal interfaces treated as stable APIs
- unsupported hardware revisions or unofficial board variants
- arbitrary forks outside the documented SDK flow
- custom Linux platform changes outside the supported release scope

## Product Architecture

Rexgen product family:

- `Rexgen Standalone`
  Uses `Rexgen Core` without the i.MX8 Linux host.
- `Rexgen Smart`
  Combines `Rexgen Core` with an i.MX8 Linux host connected through USB.

This SDK is focused on `Rexgen Smart` and on Linux-side development running on the i.MX8 host.

## Terminology

| Term | Meaning |
|---|---|
| `Rexgen Core` | The MCU-based Rexgen subsystem used as the core functional unit in Rexgen products. |
| `Rexgen Standalone` | A Rexgen device based on Rexgen Core without the i.MX8 Linux host platform. |
| `RexgenLibrary` | The software library and related tooling used for Rexgen Core and Rexgen Standalone integration workflows. |
| `Rexgen Smart` | A Rexgen system that combines Rexgen Core with an i.MX8 Linux host connected through USB. |
| `Rexgen Smart SDK` | The official Linux-side development package for building, deploying and validating software on Rexgen Smart. |
| `Rexgen PRO` | The official Rexgen Smart product application or application layer delivered by the company. |
| `Rexgen OEM` | Customer-specific or partner-specific applications and integrations built on or for Rexgen Smart. |

## Current Scope

Status of each SDK area:

| Area | Status |
|---|---|
| Architecture documentation | Done — [docs/hardware-architecture.md](docs/hardware-architecture.md) |
| Getting started flow | Done — [docs/getting-started.md](docs/getting-started.md) |
| Manifest / source sync | Done — [manifest/](manifest/README.md) |
| Flashing guide | Done — [docs/flashing.md](docs/flashing.md) |
| Supported hardware list | Done — `imx8mm-smart` only, see [SUPPORT.md](SUPPORT.md) |
| Support and security policies | Done — real reporting contact (`security@influxtechnology.com`) in [SECURITY.md](SECURITY.md) |
| Release notes | Done — first SDK tag `v0.1.0` cut, see [RELEASE_NOTES.md](RELEASE_NOTES.md) |
| Formal EULA/license text | Interim short-form notice only, pending legal review — see [EULA.md](EULA.md) |
| Official SDK examples | Done for CAN, IMU/ADC/Digital channels, and GNSS — see [examples/](examples/README.md) |

## Getting Started

First-run flow (full commands in [docs/getting-started.md](docs/getting-started.md)):

1. Prepare the supported host environment — [docs/host-setup.md](docs/host-setup.md).
2. Initialize and sync the source tree (public, no credentials needed).
3. Set up the build environment (`MACHINE=imx8mm-smart`).
4. Build the `influx-image-base` image, or generate the application SDK with `populate_sdk`.
5. Flash the target hardware — [docs/flashing.md](docs/flashing.md).
6. Boot the device and validate the platform.
7. Build and run an official SDK example.

Quick links:

- [Host Setup](docs/host-setup.md)
- [Overview](docs/overview.md)
- [Hardware Architecture](docs/hardware-architecture.md)
- [Getting Started](docs/getting-started.md)
- [Flashing Guide](docs/flashing.md)
- [Troubleshooting](docs/troubleshooting.md)
- [WiFi And Cellular](docs/wifi-cellular.md)
- [Examples](examples/README.md)

## Build Configuration

The baseline machine and image target for Rexgen Smart:

- `MACHINE=imx8mm-smart`
- `DISTRO=fsl-imx-wayland`
- image target: `influx-image-base`

## Repository Access

This repository carries its own `repo` manifest files under [`manifest/`](manifest/README.md), so `repo init`/`repo sync` can be run directly against `rexgen-smart-sdk` — no separate visit to `influx-yocto-base` is required:

```bash
repo init -u https://github.com/InfluxTechnology/rexgen-smart-sdk -b main -m manifest/base.xml
repo sync
```

Every layer the manifest references (`meta-influx`, `meta-mender`, `meta-mender-community`, `meta-murata-wireless`, and the upstream `poky`/`meta-openembedded`/`meta-imx` projects) is a **public** repository. No GitHub token or account is required.

A GitHub account/token is only needed if you work against a private fork or a private downstream repository of your own — in that case, use your own personal access token, never a token committed to shared documentation.

## Application SDK

Beyond building a full image, the SDK also supports generating a standalone cross-development SDK so a customer/partner can build applications without rebuilding the whole platform:

```bash
# from an initialized build directory
bitbake influx-image-base -c populate_sdk
```

This produces a self-extracting installer under:

```text
<build-dir>/tmp/deploy/sdk/
```

To use it:

```bash
# run the installer (default install path is /opt/<sdk-name>)
./<build-dir>/tmp/deploy/sdk/*-toolchain-*.sh

# source the generated environment before building an application
source /opt/<sdk-name>/environment-setup-*
```

Once sourced, `$CC`/`$CXX` and the target sysroot are available for cross-compiling Linux-side applications against the same headers and libraries used on the device.

See [docs/getting-started.md](docs/getting-started.md) for the full flow.

## Hardware Interfaces

The practical developer value of Rexgen Smart is the platform interfaces exposed to Linux-side software. Device-verified, working examples exist for all of these — see [examples/](examples/README.md):

- **CAN** — two interchangeable views of the same bus, bridged by `rexgend`: the Rexgen named pipe (`/var/run/rexgen/canN/{rx,tx,err}`) and a standard Linux SocketCAN `vcan` interface (`can0`..`can3`, usable with `cansend`/`candump`). Toggled via `use_socketcan` in `/data/rexgen/config/rexgend.conf`. See [examples/named-pipes/](examples/named-pipes/README.md) and [examples/socketcan/](examples/socketcan/README.md).
- **Accelerometer / Gyroscope (IMU)** — Rexgen named pipes (`/var/run/rexgen/acc/rx`, `/var/run/rexgen/gyro/rx`), enabled via RexDesk channel configuration. See [examples/named-pipes/](examples/named-pipes/README.md).
- **Analog (ADC) / Digital input channels** — Rexgen named pipes (`/var/run/rexgen/adc/rx`, `/var/run/rexgen/dig/rx`); digital input is read-only, there is no GPIO-output path through `rexgend`. See [examples/named-pipes/](examples/named-pipes/README.md).
- **GNSS** — parsed fixes via `/var/run/rexgen/gnss/rx`, or raw NMEA 0183 straight off the module's UART (`/dev/ttymxc1`), after `/opt/influx/gnssdata_start.sh`. See [examples/named-pipes/](examples/named-pipes/README.md).
- **Rexgen Core** — reached through the same pipe interface and the socket control ports (5051/5053/5054) over the USB link described in [docs/hardware-architecture.md](docs/hardware-architecture.md).
- **WiFi (AP + client) and cellular (LTE)** — WiFi AP (`wlan1`, `hostapd`+`dnsmasq`) and client (`wlan0`, `wpa_supplicant`), a Quectel EC25 modem (`ppp0`), and automatic WiFi/cellular failover, primarily configured through the on-device ReXgen Netservices Dashboard. See [docs/wifi-cellular.md](docs/wifi-cellular.md).
- **Flashing/recovery** — over USB using NXP's UUU tool; see [docs/flashing.md](docs/flashing.md).

The `rexgend` data-path protocol (pipe and SocketCAN frame/text formats) is fully specified in [examples/named-pipes/README.md](examples/named-pipes/README.md) and [examples/socketcan/README.md](examples/socketcan/README.md). By decision, no packaged client library will be built on top of it — applications talk to the pipes/sockets directly, as shown in the example code.

## Repository Status

The documentation baseline (build flow, manifest sync, flashing, application SDK, hardware interfaces, examples) is complete and usable end-to-end. Remaining known gap before calling this a finished v1.0 SDK: formal legal review of the EULA — see the table in [Current Scope](#current-scope).

## Documentation

- `manifest/README.md`
- `examples/README.md`
- `docs/overview.md`
- `docs/host-setup.md`
- `docs/hardware-architecture.md`
- `docs/getting-started.md`
- `docs/flashing.md`
- `docs/mender-ota.md`
- `docs/wifi-cellular.md`
- `docs/troubleshooting.md`
- `RELEASE_NOTES.md`
- `SUPPORT.md`
- `SECURITY.md`
- `EULA.md`
- `CONTRIBUTING.md`

## Development Direction

The current approach is to evolve the existing Yocto-based project into a usable first SDK release with minimal structural changes. Done: developer onboarding, build/flash/application-SDK documentation, hardware-interface examples, release hygiene (manifest mirroring, versioning model). Remaining: safer release defaults (see [SECURITY.md](SECURITY.md) development-vs-release posture).

## License And Versioning

Usage terms for this SDK are defined in [EULA.md](EULA.md) pending final legal review; it is the authoritative short-form notice until a formal license document is published. The underlying Yocto layers (`poky`, `meta-openembedded`, `meta-imx`, etc.) remain governed by their own upstream licenses.

Versioning model:

- each published SDK snapshot is tagged in this repository (`vX.Y.Z`) and published as a GitHub Release
- the tag/release notes state the `influx-6.6.23` stream and `rel_imx_6.6.36_2.1.0` BSP baseline it was built against (see [Version Baseline](#version-baseline))
- changes between releases are recorded in [RELEASE_NOTES.md](RELEASE_NOTES.md)
