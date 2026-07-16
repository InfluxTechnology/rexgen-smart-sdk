# Rexgen Smart SDK Overview

## Purpose

`Rexgen Smart SDK` is the official development package for building Linux-side software on Rexgen Smart devices.

The SDK is built around the existing Yocto-based platform flow and is intended to provide a clear, documented and repeatable way to:

- build supported Rexgen Smart Linux images
- flash supported hardware
- validate platform bring-up
- run official examples
- develop Linux-side applications on the i.MX8 host

## Who This SDK Is For

The SDK is intended for:

- internal application developers
- integration engineers
- validation engineers
- approved OEM and partner teams

It is intended for users who need to work on software running on the Linux host side of Rexgen Smart.

## What The SDK Includes

- documented Yocto-based build flow, including its own `repo` manifest (no separate visit to `influx-yocto-base` needed)
- supported image build path (`influx-image-base`) and application SDK (`populate_sdk`)
- flashing guidance (NXP UUU over USB)
- architecture documentation
- release notes and support scope

Official SDK examples are planned but not yet published — see [Current Scope](../README.md#current-scope) in the main README. Additional tooling, examples, and release artifacts will be added without changing this basic developer entry flow.

## What The SDK Does Not Try To Be

This SDK is not intended to be:

- a generic Linux distribution for arbitrary hardware
- a firmware SDK for Rexgen Standalone
- a support promise for undocumented internal interfaces
- a replacement for all lower-level BSP engineering work

## Scope

Supported scope:

- Linux-side development on Rexgen Smart
- documented and validated build and flashing flow
- supported hardware revisions listed in release documentation
- official branch and release combinations defined by the SDK release

Out-of-scope:

- unsupported board variants
- undocumented custom forks
- unsupported platform modifications
- Rexgen Standalone firmware workflows

## Relationship To The Existing Yocto Base

The SDK uses the current Yocto-based project (`influx-yocto-base`) as its platform foundation, mirrored into this repository's own [`manifest/`](../manifest/README.md):

- the build system is Yocto-based
- platform integration is centered around the current BSP stack (`meta-imx`, `meta-freescale`, `meta-influx`)
- documentation and developer usability are layered on top without a platform repository redesign

## Success Criterion

A developer can follow the documented flow in [getting-started.md](getting-started.md), build a supported image, flash a supported Rexgen Smart device, boot it successfully, and reach the platform's hardware interfaces (CAN, GPIO, GNSS, Rexgen Core) — without relying on internal tribal knowledge. The one part of this not yet true end-to-end is "start from an official example," since no `examples/` directory has been published yet.
