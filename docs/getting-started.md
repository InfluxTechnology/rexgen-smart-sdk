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

`influx-yocto-base` and every layer it references (`meta-influx`, `meta-mender`, `meta-mender-community`, `meta-murata-wireless`, plus upstream `poky` / `meta-openembedded` / `meta-imx` / etc.) are **public repositories**. No GitHub account or token is required to sync the SDK baseline.

Install `repo` and initialize the manifest:

```bash
mkdir -p ~/bin
curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
chmod a+x ~/bin/repo
export PATH=~/bin:$PATH

git config --global user.email "you@example.com"
git config --global user.name "Your Name"

mkdir build && cd build
repo init -u https://github.com/InfluxTechnology/influx-yocto-base -b influx-6.6.23 -m base.xml
repo sync
```

`base.xml` includes the Mender OTA update layers and the release toolchain setup script. Other manifest profiles (`common.xml`, `default.xml`, `mender.xml`, `single.xml`) select different layer/feature combinations — use `base.xml` for the SDK baseline unless you have a reason to pick another one.

You only need a GitHub token/`.netrc` entry if you are syncing from your **own private fork**. In that case, never commit a real token or personal account to shared documentation — use a placeholder like below and keep the real credentials local to your machine:

```text
machine github.com
login your-github-username
password your-personal-access-token
```

## Build Environment Initialization

The `influx-yocto-base` machine/distro baseline for Rexgen Smart is:

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

The first example should be small, deterministic and easy to validate.

The ideal first example is:

- easy to build
- easy to run
- clearly connected to the platform value of Rexgen Smart

## Hardware Interfaces

The baseline image ships the userspace tooling to reach the platform interfaces out of the box:

- **CAN**: SocketCAN via `can-utils`/`iproute2` (`ip link set can0 up type can bitrate 500000`, `candump can0`, `cansend can0 123#DEADBEEF`).
- **GPIO**: `libgpiod`/`libgpiod-tools` (`gpiodetect`, `gpioget`, `gpioset`).
- **GNSS**: onboard GNSS data logging is a documented Rexgen device feature.
- **Rexgen Core / IMU**: reached through the Rexgen Core integration path (`rexgen-core`, `rexgend`, `wlan-manager`) over the USB link — see [hardware-architecture.md](hardware-architecture.md). Live CAN, socket control ports (5051/5053/5054) and datalog upload to cloud storage are part of this path.
- **Flashing and recovery**: see [flashing.md](flashing.md).

## Release Readiness Note

This document should only be called complete once a developer can follow it from a clean environment without requiring additional oral instructions.
