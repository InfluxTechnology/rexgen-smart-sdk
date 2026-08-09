# Mender OTA Updates

## Status

**Confirmed working.** This OTA flow — building a `.mender` artifact, deploying it through the Mender platform, and the device installing/booting into the update — has been tested on real, production Rexgen Smart devices by InfluxTechnology and works end-to-end. The build-side configuration below is confirmed from `meta-influx-mender`'s actual layer source; the server-side deployment flow matches Mender's official documentation (cited per section). A few documentation-only items remain — see [Still Needed](#still-needed) — but they're about capturing artifacts of a run (logs/timings) for this doc, not about whether the flow itself works.

## Build Configuration

Mender OTA support is added by the `meta-influx-mender` layer and its `mender.xml` manifest profile (see [manifest/README.md](../manifest/README.md)) — `manifest/base.xml`, the default used by this SDK, already includes it.

`influx-setup-mender.sh` (the release setup script used when Mender layers are present) does the following to a build directory, confirmed from `meta-influx-mender`'s source:

- adds `meta-mender-core` and `meta-influx-mender` to `bblayers.conf`
- appends `meta-influx-mender/templates/local.conf.append` to `conf/local.conf`, which:
  - switches the image output from `.wic`/`sdcard` to Mender's full-disk-image format (`inherit mender-full`)
  - sets the artifact name to `${ARTIFACT_TYPE}_${INFLUX_RELEASE}` (`ARTIFACT_TYPE="image"`)
  - configures the A/B partition layout for `imx8mm-smart`: boot (`/dev/mmcblk2p1`), rootfs A (`/dev/mmcblk2p2`), rootfs B (`/dev/mmcblk2p3`), persistent data (`/dev/mmcblk2p4`)
  - points at a Mender server URL and tenant token (hosted Mender by default)
- patches U-Boot for Mender's boot-count/upgrade-available mechanism (`u-boot-inf-fw-utils.patch`)

**Do not reuse the `MENDER_SERVER_URL`/`MENDER_TENANT_TOKEN` values baked into the layer's template file as-is** — those are tied to a specific Mender tenant. Use your own organization's Mender account/tenant token when setting up a build.

Building with this configuration produces a `.mender` artifact (named per `MENDER_ARTIFACT_NAME` above) alongside the normal image output, plus `mender-artifact-info` installed on the target for on-device inspection.

## Server-Side Deployment

This part follows Mender's standard hosted-service workflow — it is not InfluxTechnology-specific, so treat [Mender's own documentation](https://docs.mender.io/get-started/deploy-an-operating-system-update) as the source of truth if anything below goes stale.

1. **Upload the artifact.** In the Mender web UI, open the **Releases** tab and upload the `.mender` file produced by the build. This creates a new Release containing that Artifact. ([docs.mender.io/overview/artifact](https://docs.mender.io/overview/artifact))
2. **Create a deployment.** From the Release, choose "Create a deployment for this Release" (or the **Deployments** tab → **Create deployment**), then select the target — a static group (fixed device list) or dynamic group. ([docs.mender.io/overview/deployment](https://docs.mender.io/overview/deployment))
3. **Device picks it up.** The Mender client on the device polls the server periodically; once it finds a pending deployment for itself, it downloads, installs into the inactive rootfs partition (A/B), and reboots into it.
4. **Commit or automatic rollback.** After rebooting into the new partition, the client must call `ArtifactCommit` to make the update permanent. If the new partition fails to come up healthy (per the update module's checks), Mender's orchestrator triggers `ArtifactRollback` instead, and the device boots back into the previous, known-good partition — rollback remains possible even after commit started, if the device lost power mid-commit. ([docs.mender.io/orchestrate-updates/interface-protocol](https://docs.mender.io/orchestrate-updates/interface-protocol))
5. **Status.** Deployment status per device moves through `downloading` → `installing` → `rebooting` → `pending`, ending in `success`, `failure`, `already-installed`, or `aborted`, visible in the Deployments tab. ([docs.mender.io/overview/deployment](https://docs.mender.io/overview/deployment))

## Still Needed

The flow itself is confirmed working in production; what's left is turning that into the same kind of documented, reproducible walkthrough as the other [examples/](../examples/README.md) (real captured output, not just a description):

- a real deployment run's on-device log output (e.g. `journalctl -u mender-updated`, `mender show-artifact`) captured and added here, screenshots optional
- a captured example of the automatic-rollback path specifically (a deliberately failed update), since normal successful updates don't exercise it
- decide whether `mender-connect` / remote terminal (a separate Mender add-on) is in scope, or explicitly out of scope

Whoever ran the production deployments should paste the real output/timings directly into this file when convenient.
