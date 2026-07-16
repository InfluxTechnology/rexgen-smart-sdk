# Security Policy

## Supported Versions

| SDK / platform stream | Supported |
|---|---|
| `influx-6.6.23` (current, `imx8mm-smart`) | Yes |
| Older or unreleased streams | No |

Security fixes are provided only for the currently supported stream listed above. See [Version Baseline](README.md#version-baseline) for how the SDK stream and NXP BSP baseline relate to each other.

## Reporting A Vulnerability

Report suspected vulnerabilities in this SDK, its documented build/flash flow, or the platform images it produces to:

**security@influxtechnology.com**

Include, where applicable:

- affected component (e.g. `influx-image-base`, `meta-influx`, a specific layer/recipe, or this SDK's documentation/tooling)
- SDK/platform version (`influx-6.6.23` stream and, if relevant, the NXP BSP baseline)
- steps to reproduce, and the impact you believe it has
- whether the issue is already public

We ask that you report privately and give InfluxTechnology a reasonable window to investigate and ship a fix before any public disclosure. Do not open a public GitHub issue for a suspected vulnerability.

This is a company mailbox, not a guaranteed-response SLA; for anything time-critical on a production deployment, also use your normal InfluxTechnology support/partner contact in parallel.

## Current Credential Posture (`influx-image-base`)

The `influx-image-base` recipe (`meta-influx/recipes-influx/images/influx-image-base.bb`) ships the following by default, in every build, unless the recipe is overridden downstream:

- `ssh-server-openssh` enabled (`IMAGE_FEATURES`)
- a `tester` user with an **empty password** (`useradd -p ''`) and a login shell (`/bin/sh`)
- `root` password hardcoded to a fixed value (`pass`), with the password hash committed in the (public) recipe source

This is a **lab/bench development default**, not a release-security posture. As shipped, anyone able to reach a device's SSH port or console can log in as `tester` with no password, or as `root` with a password that is public knowledge (it is visible in cleartext in this project's git history, not just as a hash).

**Do not deploy an unmodified build of this image to any customer-facing, internet-reachable, or otherwise untrusted-network device.**

## Hardening Checklist Before Non-Lab Deployment

Before flashing a device for anything beyond bench development, apply all of the following:

1. Remove the `tester` user and its empty-password entry, or replace `EXTRA_USERS_PARAMS` in a `.bbappend` with accounts that use unique, non-published passwords or SSH keys only.
2. Set a unique `root` password per device/fleet (not the shared default), or disable root login entirely (`PermitRootLogin no` in the SSH server config) in favor of a named, key-authenticated user.
3. Restrict `ssh-server-openssh` to key-based authentication (`PasswordAuthentication no`) for release images, or disable it entirely if remote shell access is not required.
4. Regenerate any credentials before the device leaves a trusted network — never rely on the baseline SDK image's credentials past initial bring-up.
5. Track this checklist per fleet/deployment; a device that skipped step 1–3 should not be treated as production-ready regardless of its build date.

## Scope

This policy covers:

- this SDK repository (documentation, manifest, and any tooling published here)
- the `influx-image-base` image and the layers pinned in [`manifest/`](manifest/README.md)
- the documented build, flashing, and application-SDK flows

It does not cover Rexgen Standalone firmware, RexgenLibrary, or any customer-specific (Rexgen OEM) fork or modification made outside this repository's documented flow — report issues in those separately through the appropriate InfluxTechnology channel.

## Development Vs Release

Development conveniences (such as the credential posture above) exist to make bring-up and debugging fast. They are documented here precisely so they are never mistaken for a release-security posture. Any new development-only shortcut added to the platform should be called out in this section the same way, with an explicit hardening step before it ships.
