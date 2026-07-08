# Manifest Files

These are the `repo` manifest files for the `influx-6.6.23` platform stream (mirrored from `InfluxTechnology/influx-yocto-base`), so `rexgen-smart-sdk` can act as a single entry point for both documentation and source sync.

| File | Purpose |
|---|---|
| `common.xml` | Shared layer set (poky, meta-openembedded, meta-imx, meta-freescale, meta-murata-wireless, etc.). Included by all the other manifests. |
| `base.xml` | Base functionality profile, usable for SDK work. Includes Mender OTA layers. **Use this one for the SDK baseline.** |
| `default.xml` | Minimal default profile on top of `common.xml`. |
| `mender.xml` | Mender-focused profile variant. |
| `single.xml` | Single-partition profile variant. |

## Usage

```bash
mkdir build && cd build
repo init -u https://github.com/InfluxTechnology/rexgen-smart-sdk -b main -m manifest/base.xml
repo sync
```

Each `<project>` entry in these manifests pins an exact revision of a layer (e.g. `meta-imx` at `rel_imx_6.6.36_2.1.0`). Updating the platform baseline means updating these files — keep them in sync with `InfluxTechnology/influx-yocto-base` when that project moves to a new stream.

## Version Baseline Pinned By These Manifests

- SDK release stream: `influx-6.6.23`
- Linux kernel: `6.6.23`
- U-Boot: `2024.04`
- Yocto distro: `fsl-imx-wayland` / `scarthgap`
- NXP BSP (`meta-imx`): `rel_imx_6.6.36_2.1.0`
