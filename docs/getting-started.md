# Getting Started

## Purpose

This document defines the baseline first-run flow for the Rexgen Smart SDK.

It is intentionally focused on a practical developer path:

1. prepare the host machine
2. obtain the source tree
3. initialize the Yocto build environment
4. build a supported image
5. flash the target device
6. verify boot and basic platform health
7. run an official SDK example

## Expected Host Environment

The supported host operating system and package prerequisites are documented in [host-setup.md](host-setup.md).

Baseline:

- supported host: Ubuntu `22.04 LTS` (recommended) or `20.04 LTS`
- Ubuntu `24.04` is not officially supported by Yocto Scarthgap and is not validated for this project — use 22.04 LTS
- required packages follow the Yocto `Scarthgap` host package list

## Source Setup

This SDK repository (`rexgen-smart-sdk`) carries its own copy of the `repo` manifest files under [`manifest/`](../manifest/README.md), so it is the single entry point for both documentation and source sync — you don't need to visit `influx-yocto-base` directly. Every layer referenced by the manifest (`meta-influx`, `meta-mender`, `meta-mender-community`, `meta-murata-wireless`, plus upstream `poky` / `meta-openembedded` / `meta-imx` / etc.) is a **public repository**. No GitHub account or token is required to sync the SDK baseline.

Install `repo` and initialize the manifest:

```bash
mkdir -p ~/bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
export PATH=~/bin:$PATH

git config --global user.email "you@example.com"
git config --global user.name "Your Name"

mkdir build && cd build
repo init -u https://github.com/InfluxTechnology/rexgen-smart-sdk -b main -m manifest/base.xml
repo sync
```

`manifest/base.xml` includes the Mender OTA update layers and the release toolchain setup script. Other manifest profiles (`manifest/common.xml`, `manifest/default.xml`, `manifest/mender.xml`, `manifest/single.xml`) select different layer/feature combinations — use `base.xml` for the SDK baseline unless you have a reason to pick another one. See [manifest/README.md](../manifest/README.md) for what each profile includes.

You only need a GitHub token/`.netrc` entry if you are syncing from your **own private fork**. In that case, never commit a real token or personal account to shared documentation — use a placeholder like below and keep the real credentials local to your machine:

```text
machine github.com
login your-github-username
password your-personal-access-token
```

## Build Environment Initialization

The machine/distro baseline for Rexgen Smart (pinned in `manifest/`) is:

```bash
MACHINE=imx8mm-smart
DISTRO=fsl-imx-wayland
```

Initialize the build directory (this creates `conf/local.conf` and `conf/bblayers.conf` already set to that machine/distro):

```bash
source influx-setup-release.sh -b build-dir
```

If you come back to an already-initialized build directory in a new shell (or after a reboot), don't rerun the setup script — just re-source the environment:

```bash
source setup-environment build-dir
```

## Building The Image

The baseline image recipe is `influx-image-base`:

```bash
bitbake influx-image-base
```

Build output lands in:

```text
build-dir/tmp/deploy/images/imx8mm-smart/
```

Build logs for a failing task are under `build-dir/tmp/work/.../temp/log.do_<task>`; `bitbake -c cleansstate <recipe>` followed by a rebuild is the usual first troubleshooting step for a corrupted task.

Version relationship to keep in mind when reporting a build:

- SDK stream: `influx-6.6.23`
- NXP BSP baseline: `rel_imx_6.6.36_2.1.0`

These are related but not interchangeable version labels — see [Version Baseline](../README.md#version-baseline) in the main README.

## Building The Application SDK

To build a Linux-side application without rebuilding the whole platform, generate a standalone cross-development SDK from an initialized build directory:

```bash
bitbake influx-image-base -c populate_sdk
```

This produces a self-extracting installer under:

```text
build-dir/tmp/deploy/sdk/
```

Install it on the host and source the generated environment:

```bash
./build-dir/tmp/deploy/sdk/*-toolchain-*.sh
source /opt/<sdk-name>/environment-setup-*
```

Once sourced, `$CC`, `$CXX`, `$PKG_CONFIG_PATH` and the target sysroot point at the same toolchain and headers used to build the device image, so you can cross-compile applications directly:

```bash
$CC myapp.c -o myapp
```

## Flashing And Boot Validation

After the image is built, flash it following [flashing.md](flashing.md) (deploy script + NXP UUU over USB).

Minimum post-flash validation checklist:

- device boots successfully
- console access works as documented
- expected services start (`systemctl status`, check `rexgend`/`wlan-manager`)
- Rexgen Core integration path is visible (device responds on the socket control ports)
- the device is ready for example execution

## Running An Example

Device-verified examples are available in [../examples/](../examples/README.md):

- [CAN round-trip](../examples/can.md) — Rexgen pipe and SocketCAN, send and receive
- [Sensor channels](../examples/sensor-channels.md) — Accelerometer, Gyroscope, Analog (ADC), Digital input
- [GNSS](../examples/gnss.md) — parsed fixes and raw NMEA UART

Each example is a manual, shell-level walkthrough (real commands and real captured output) rather than a compiled application — they're the fastest way to confirm a booted device's interfaces are working before writing your own application against them.

## Hardware Interfaces

The baseline image ships the userspace tooling to reach the platform interfaces out of the box; see [Running An Example](#running-an-example) above for verified, working walkthroughs of each:

- **CAN**: Rexgen named pipe (`/var/run/rexgen/can0/tx`+`rx`) or standard SocketCAN (`can-utils`/`iproute2`: `candump can0`, `cansend can0 123#DEADBEEF`).
- **Accelerometer / Gyroscope**: Rexgen named pipes (`/var/run/rexgen/acc/rx`, `/var/run/rexgen/gyro/rx`), enabled via RexDesk.
- **Analog / Digital channels**: Rexgen named pipes (`/var/run/rexgen/adc/rx`, `/var/run/rexgen/dig/rx`).
- **GNSS**: `/opt/influx/gnssdata_start.sh` to init, then `/var/run/rexgen/gnss/rx` (parsed) or `/dev/ttymxc1` (raw NMEA).
- **Rexgen Core**: reached through the same pipe interface and the socket control ports (5051/5053/5054) over the USB link — see [hardware-architecture.md](hardware-architecture.md).
- **Flashing and recovery**: see [flashing.md](flashing.md).
