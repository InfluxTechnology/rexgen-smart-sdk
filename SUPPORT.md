# Support Policy

## Scope

This document defines the support boundary for the Rexgen Smart SDK: what's supported, what's best-effort, and what falls outside the support promise entirely.

## Supported

The SDK supports:

- the documented build, flashing, and application-SDK flow in this repository
- hardware: `imx8mm-smart` (Rexgen Smart, i.MX8MM) — the only machine currently defined in `manifest/`
- branch/stream: `influx-6.6.23` (kernel `6.6.23`, NXP BSP `rel_imx_6.6.36_2.1.0`) — see [Version Baseline](README.md#version-baseline)
- documented Linux-side development workflows against the interfaces listed in [Hardware Interfaces](README.md#hardware-interfaces)

Official runnable SDK examples are planned but not yet published — see the [Current Scope](README.md#current-scope) table in the main README.

## Best-Effort Areas

The following may be assisted on a best-effort basis depending on internal priorities and release maturity:

- integration guidance for approved partners
- adaptation of examples for close variants of supported use cases
- troubleshooting around validated SDK flows

## Not Supported

The SDK does not promise support for:

- undocumented internal interfaces
- unsupported hardware revisions
- arbitrary custom forks
- custom platform changes outside the documented flow
- Rexgen Standalone firmware development

## Requirements For Supported Use

To stay within supported scope:

- use the documented branch or release (`influx-6.6.23`)
- follow the documented setup, build, and flashing instructions
- use supported hardware revisions (`imx8mm-smart`)
- don't rely on undocumented internal behavior

## Getting Help

- **Bugs and questions about this SDK** (documentation, manifest, build/flash flow): open a GitHub issue in this repository.
- **Security issues**: do not open a public issue — see [SECURITY.md](SECURITY.md) for the reporting contact.
- **Partner and commercial support**: use your existing InfluxTechnology account/partner contact.
