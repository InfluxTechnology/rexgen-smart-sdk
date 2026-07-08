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

## Minimum Practical Recommendations

The Yocto documentation gives a minimum baseline, but for practical Rexgen Smart work the host machine should also have:

- enough free disk space for full image builds
- enough RAM for repeatable builds
- stable network connectivity for repository sync

The final SDK release should publish a project-specific recommendation for:

- minimum free disk space
- recommended disk space
- minimum RAM
- recommended RAM

## Locale

The host should have `en_US.UTF-8` generated and available, as shown above.

If locale problems are seen during build setup, this should be one of the first items checked.

## Validation Status

This document reflects the official Yocto `Scarthgap` package baseline, cross-checked against the Yocto Project 5.0.6 system requirements.
