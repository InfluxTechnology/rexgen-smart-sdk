# Rexgen Smart SDK — Usage Notice

## Purpose

This notice sets out the terms under which InfluxTechnology makes the Rexgen Smart SDK available. It governs use of this repository, its documentation, the `influx-image-base` build it produces, and any application SDK / cross-toolchain generated from it, on supported Rexgen Smart hardware and supported release baselines (see [Version Baseline](README.md#version-baseline)).

## Permitted Use

Approved users — internal developers, integration engineers, and approved OEM/partner teams — may use the SDK to:

- build supported Rexgen Smart Linux images
- evaluate and validate the platform
- develop Linux-side software for supported Rexgen Smart systems
- integrate supported applications and examples

## Restricted Use

This notice does not grant rights to:

- redistribute the SDK or built images outside the documented flow
- use the SDK outside agreed commercial or partner terms
- reverse-engineer components that are covered by separate third-party licensing terms
- use the SDK against unsupported hardware revisions or undocumented internal interfaces as if they were stable, supported APIs

## No Implied Production Approval

Availability of a development flow, example, image, or tool in this SDK does not by itself mean it is approved for production deployment in every customer scenario. In particular, the default credential posture of `influx-image-base` is a lab/development configuration — see [SECURITY.md](SECURITY.md) before any non-lab deployment.

Production usage, provisioning, and security posture follow InfluxTechnology's documented release process and any applicable commercial agreement.

## Third-Party Components

The SDK depends on third-party open-source components and platform layers pinned in [`manifest/`](manifest/README.md) (Yocto/OpenEmbedded, NXP's `meta-imx`, Mender, and others), each governed by its own upstream license. Using the SDK does not change those upstream license terms; consult each layer's own license for its specific conditions.

## Versioning

Published SDK snapshots are tagged in this repository and released with accompanying release notes — see [License And Versioning](README.md#license-and-versioning) and [RELEASE_NOTES.md](RELEASE_NOTES.md).

## Precedence

This notice is the governing usage document for the SDK unless and until InfluxTechnology publishes a separate, formally executed license agreement covering your use — in which case that agreement takes precedence. InfluxTechnology may update this notice between releases; the version distributed with a given SDK release governs that release.
