# Host Setup

## Purpose

This document describes the expected host build environment for the Rexgen Smart SDK baseline.

The SDK is built on a Yocto `Scarthgap`-based flow, so the host requirements should follow the corresponding Yocto Project guidance unless the project documents stricter local requirements.

## Supported Host Baseline

The SDK follows the Yocto Project `5.0.6` (`Scarthgap`) system requirements. Officially supported hosts are:

- Ubuntu `22.04 LTS` (recommended)
- Ubuntu `20.04 LTS`

`Ubuntu 24.04` is **not** on the Yocto Project's officially tested distro list for Scarthgap and is not validated against the Rexgen Smart build flow. Building on 24.04 may work but is unsupported; use 22.04 LTS if you want a first-attempt clean build.

## Required Packages For Ubuntu And Debian

For a headless build host, install the official Yocto `Scarthgap` package baseline (this replaces the older package list from earlier, pre-Scarthgap Yocto guides — the `influx-yocto-base` README still references that older list, use the one below instead):

```bash
sudo apt install gawk wget git diffstat unzip texinfo gcc build-essential chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping python3-git python3-jinja2 python3-subunit zstd liblz4-tool file locales libacl1
sudo locale-gen en_US.UTF-8
```

## Optional Host Tool Fallback

If the host environment does not meet the required versions for Git, tar, Python, make or gcc, the Yocto buildtools flow should be considered.

Typical options include:

- `scripts/install-buildtools`
- `buildtools-tarball`
- `buildtools-extended-tarball`

This is especially useful when the SDK needs a more controlled host tool baseline.

## Disk Space And RAM

Official Yocto Project `5.0.6` (`Scarthgap`) minimums, quoted from the system requirements documentation:

- disk space: **at least 90 GB free** (quoted for `core-image-sato` on `qemux86-64`; a comparable-complexity image)
- RAM: **at least 8 GB**, with 4 CPU cores (builds succeed but are slow at this minimum)

`influx-image-base` is a comparable-or-larger image than `core-image-sato` (it adds Qt6, Wayland, Bluetooth, wireless firmware/drivers and the Mender OTA stack on top of the base Yocto set), so treat 90 GB/8 GB as a hard floor, not a comfortable target. Practical recommendation for repeated/parallel builds:

| | Minimum (Yocto floor) | Recommended for this project |
|---|---|---|
| Free disk space | 90 GB | 200 GB+ (sstate-cache and `downloads/` grow fast across rebuilds) |
| RAM | 8 GB | 16 GB+ |
| CPU cores | 4 | as many as available — build parallelism scales directly with `BB_NUMBER_THREADS`/`PARALLEL_MAKE` |

Stable network connectivity is also required for the initial `repo sync` (it fetches every layer in `manifest/`) and for any `bitbake` fetch tasks that aren't already in `downloads/` or `sstate-cache`.

A full from-scratch `influx-image-base` build has not been benchmarked and published for a reference host yet — if you time one, add the wall-clock time and host spec here for future readers.

## Locale

The host should have `en_US.UTF-8` generated and available, as shown above.

If locale problems are seen during build setup, this should be one of the first items checked.

## Validation Status

This document reflects the official Yocto `Scarthgap` package baseline, cross-checked against the Yocto Project 5.0.6 system requirements.
