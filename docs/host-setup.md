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

A full from-scratch `influx-image-base` build has not been benchmarked and published for a reference host yet. Until a first-party measurement exists, the table below gives **estimated ranges** for common host specs, positioned against published third-party Yocto build-time benchmarks for comparable (not identical) images — these are not measurements of `influx-image-base` itself, and should be replaced with a real number as soon as one is available.

| Host spec | Estimated range | Based on |
|---|---|---|
| Core i7 (7th gen), 32 GB RAM, 1 TB SSD | ~1.5–2.5 hours | [sveinse/yocto-benchmark](https://github.com/sveinse/yocto-benchmark): i7-7820HQ, 8 cores, 32 GB, NVMe → 34 min on a much smaller test image; [djboni/yocto-benchmark](https://github.com/djboni/yocto-benchmark): 8–12 core / 32 GB / SSD hosts → 1h25–2h02 building `core-image-minimal` + SDK |
| Core i7 (9th gen), 64 GB RAM, 1 TB SSD | ~1.5–2 hours | djboni: 8-core / 64 GB / NVMe class → 1h46 (`core-image-minimal` + SDK); extra RAM beyond ~16–32 GB is rarely the bottleneck |
| 2× Xeon E5-2620 v2, 128 GB RAM, 1 TB SSD | ~2–3.5 hours | djboni: 12-core / 32 GB / SSD (newer, higher-clock chip) → 1h25; same-generation reference (2× Xeon E5-2670 v2, more cores/higher clock) → 19 min on the smaller sveinse test image — an older, lower-clock dual-Xeon like the E5-2620 v2 should land well above these. 128 GB RAM is well past the point where RAM is the bottleneck (see note above), so it doesn't shift this range — core count/clock still dominate here |

`influx-image-base` is heavier than the `core-image-minimal`/small test images these benchmarks used (it adds Qt6, Wayland, Bluetooth, wireless firmware/drivers, and Mender), so real times likely sit at the upper end of these ranges or above. If you time a real build, replace this table with the actual measurement (host spec + wall-clock time) — real data beats estimates.

## Locale

The host should have `en_US.UTF-8` generated and available, as shown above.

If locale problems are seen during build setup, this should be one of the first items checked.

## Validation Status

This document reflects the official Yocto `Scarthgap` package baseline, cross-checked against the Yocto Project 5.0.6 system requirements.
