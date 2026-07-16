# Troubleshooting

Common issues encountered while syncing, building, flashing, and booting Rexgen Smart with this SDK, with their known cause and fix.

## Source Sync

**`repo init` fails or pulls the wrong content.**
Cause: wrong branch (`-b`) or manifest file (`-m`) argument. Fix: use `-b main -m manifest/base.xml` against `https://github.com/InfluxTechnology/rexgen-smart-sdk` exactly as shown in [getting-started.md](getting-started.md#source-setup).

**`repo sync` stalls or fails partway through.**
Cause: usually a network interruption mid-fetch of one of the layers in `manifest/`. Fix: re-run `repo sync` — it resumes per-project rather than starting over. If one specific project keeps failing, check that project's remote is reachable (`git ls-remote <url>`).

## Build Environment

**`source influx-setup-release.sh` or `bitbake` fails with missing-tool errors.**
Cause: missing host packages. Fix: install the exact package list in [host-setup.md](host-setup.md#required-packages-for-ubuntu-and-debian); don't substitute an older/alternate list.

**Build fails on Ubuntu `24.04` with toolchain or Python version errors that don't reproduce on `22.04`.**
Cause: 24.04 is not on Yocto Scarthgap's officially tested distro list (see [host-setup.md](host-setup.md#supported-host-baseline)) — its newer glibc/Python can trip host-tool assumptions in some recipes. Fix: build on Ubuntu `22.04 LTS`, or use the Yocto buildtools tarball fallback described in host-setup.md.

## Build Failures

**`bitbake` fails with `No space left on device` partway through.**
Cause: disk exhaustion — this is the single most common Yocto build failure. `influx-image-base` needs well above the 90 GB Yocto floor once `sstate-cache` and `downloads/` accumulate across rebuilds; see [host-setup.md](host-setup.md#disk-space-and-ram). Fix: free space or move `TMPDIR`/`DL_DIR`/`SSTATE_DIR` to a larger volume, then re-run `bitbake influx-image-base`.

**A previously-working recipe fails after switching branches/manifests in the same build directory.**
Cause: stale `sstate-cache`/`tmp` from a different configuration. Fix: `bitbake -c cleansstate <recipe>` for the specific recipe, or start a fresh `build-dir` for a different manifest/branch rather than reusing one across streams.

## Flashing

**UUU doesn't detect the board (`uuu` reports no device / times out).**
Cause: board not in OTG boot/recovery mode, a charge-only USB cable, or (on Linux) missing udev permissions for the device. Fix: confirm the board is in OTG mode per your board's boot-mode strap/switch, use a data-capable USB cable, and run `uuu` with `sudo` (or add a udev rule for the device) on Linux.

**UUU starts but aborts partway through a step.**
Cause: usually a wrong/corrupted image artifact, or the board dropped out of OTG mode mid-flash. Fix: re-run `./deploy-image.sh` to regenerate `uuu-deploy.tgz` from a known-good build, and re-flash without disconnecting the cable — see [flashing.md](flashing.md#recovery-notes).

## Boot Problems

**Device doesn't boot after a flash that UUU reported as successful.**
Cause: most often an image built for a different machine than `imx8mm-smart`, or a truncated `.sdimg`/`.wic` from an interrupted build. Fix: confirm `MACHINE=imx8mm-smart` was used for the build (see [getting-started.md](getting-started.md#build-environment-initialization)), then rebuild and reflash.

## Reporting A New Issue

If you hit an issue not listed here, open a GitHub issue in this repository with: the exact command that failed, the full error output, your host OS/version, and the SDK/BSP version pair from [Version Baseline](../README.md#version-baseline). Confirmed fixes get folded back into this file.
