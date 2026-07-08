# Flashing Guide

## Purpose

This document describes the supported flashing flow for Rexgen Smart devices built with the SDK.

The goal is to provide a safe and repeatable way to deploy a built image to supported hardware.

## Scope

This guide is intended for:

- development image flashing
- validation image flashing
- supported release image deployment during SDK workflows

It is not intended to replace internal manufacturing or production provisioning procedures unless that process is documented explicitly.

## Required Inputs

Before flashing a device, you need:

- a built image (`bitbake influx-image-base` completed successfully)
- a Rexgen Smart (`imx8mm-smart`) board
- a USB cable to the board's OTG port
- NXP's UUU (Universal Update Utility) — bundled in the deploy archive for Linux and Windows, also available upstream at [github.com/NXPmicro/mfgtools](https://github.com/NXPmicro/mfgtools)

## Supported Flashing Flow

1. **Package the deploy artifacts.** After a successful build, run the deploy script from the build directory:

   ```bash
   ./deploy-image.sh
   ```

   This collects the build output from `build-dir/tmp/deploy/images/imx8mm-smart/` (`.sdimg`, `.wic`, `.dtb`, `.bin`) into `build-dir/uuu-deploy.tgz`, which bundles the UUU binaries for Linux and Windows.

2. **Extract the archive** and go into the `uuu-deploy` folder.

3. **Put the board into OTG boot/recovery mode** and connect the USB cable to the host.

4. **Run UUU:**

   ```bash
   # Linux
   sudo ./uuu deploy-image-sdimg.uuu
   ```

   ```powershell
   # Windows
   uuu.exe deploy-image-sdimg.uuu
   ```

   UUU writes the image over USB; do not disconnect the cable or power during this step.

5. **Confirm success** — UUU reports a final success status per step; a failed step aborts with an error instead of silently continuing.

6. **First boot** — disconnect from OTG mode, power-cycle normally, and proceed to the boot validation checklist below.

## Safety Requirements

- Flashing overwrites all existing data on the device's storage — back up anything you need first.
- Only flash an image built for `imx8mm-smart`; images built for other machines will not boot and may leave the board in an inconsistent state.
- Do not disconnect power or the USB cable while UUU is running.
- The baseline `influx-image-base` build currently ships debug credentials by default (passwordless `tester` user, hardcoded `root` password, SSH enabled) — see [SECURITY.md](../SECURITY.md#current-credential-posture-influx-image-base). Do not flash an unmodified build of this image to a production-like, customer-facing, or otherwise untrusted-network device.

## Post-Flash Validation

After flashing, confirm:

- the device boots successfully and reaches a login/console prompt
- console access works (serial console or SSH as documented for your setup)
- the image reports the expected version (`cat /etc/os-release` / build identifier)
- baseline services start (`rexgend`, `wlan-manager`, `mender-update`)
- the device is ready to run an official SDK example

## Recovery Notes

- **Failed flash**: UUU aborts with a non-zero exit status and an error naming the failing step; re-check that the board is in OTG boot mode and the cable/port are the ones UUU expects, then retry the same command.
- **Retry**: simply re-run the `uuu` command from step 4 above — it does not require re-extracting the archive.
- **Recovery mode entry**: re-enter OTG boot mode the same way as the initial flash (board-specific boot switch/strap; see your board's hardware documentation).
- **Escalate** to deeper platform/BSP debugging if the board does not enumerate over USB at all (check `lsusb`/`dmesg` on the host) or if UUU completes but the board does not boot afterwards.
