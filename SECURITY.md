# Security Policy

## Purpose

This document defines the baseline security posture expected for the Rexgen Smart SDK release flow.

## Principles

The SDK should avoid:

- known shared default credentials in release images
- passwordless user access in release paths
- personal credential examples in public documentation
- undocumented security-sensitive shortcuts

## Development vs Release

Where development convenience is required, it should be:

- clearly marked as development-only
- documented separately from release behavior
- excluded from production-like deployment guidance

## Current Credential Posture (`influx-image-base`)

**Known dev-only risk, current as of the `influx-6.6.23` baseline.** The `influx-image-base` recipe (`meta-influx/recipes-influx/images/influx-image-base.bb`) currently ships all of the following, active in every build unless the recipe is overridden:

- `ssh-server-openssh` is enabled by default (`IMAGE_FEATURES`).
- A `tester` user is created with an **empty password** (`useradd -p ''`) and a login shell (`/bin/sh`) — passwordless shell access if SSH/console is reachable.
- `root`'s password is hardcoded to a fixed value (`pass`), with the SHA-512 hash committed directly in the (public) recipe file.

This means: anyone who can reach the device over SSH or a console today can log in as `tester` with no password at all, or as `root` with a password that is trivially known (it's public on GitHub in cleartext form, not just as a hash).

**Do not deploy an image built from this recipe, unchanged, to any customer-facing, internet-reachable, or otherwise untrusted-network device.** Before any non-lab deployment:

- remove or disable the `tester` user and its empty-password entry
- set a unique, non-published `root` password (or disable root login entirely and use key-based SSH for a named user)
- disable `ssh-server-openssh` in `IMAGE_FEATURES` for release images, or restrict it to key-only auth

## Reporting

Security issues discovered in the SDK flow, release artifacts or platform integration should be reported through the appropriate internal or approved partner communication path.

**Reporting contact: not yet defined.** This needs a real, monitored address/process from the project owner before this document can be treated as complete — placeholder text should not ship in a public release.

## Release Expectation

No published SDK release should rely on public documentation that exposes personal access patterns, reusable shared credentials or unsafe production defaults. The credential posture described above is a known exception to that rule today and must be resolved (or explicitly accepted and time-boxed) before a production-oriented SDK release.
