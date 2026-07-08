# Support Policy

## Scope

This document defines the support boundary for the Rexgen Smart SDK baseline.

The goal is to make it clear what is intended to be supported, what is best-effort and what falls outside the SDK support promise.

## Supported

The SDK is intended to support:

- the documented build flow
- hardware: `imx8mm-smart` (Rexgen Smart, i.MX8MM) — the only machine currently defined in `manifest/`
- branch/stream: `influx-6.6.23` (kernel `6.6.23`, NXP BSP `rel_imx_6.6.36_2.1.0`) — see [Version Baseline](README.md#version-baseline)
- official SDK examples (once published — see [RELEASE_NOTES.md](RELEASE_NOTES.md) known limitations)
- documented Linux-side development workflows

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

To stay within supported scope, users should:

- use the documented branch or release
- follow the documented setup and flashing instructions
- use supported hardware revisions
- avoid relying on undocumented internal behavior

## Documentation Status

This support policy should be refined as the first formal SDK release is prepared and as the supported hardware and release matrix is finalized.
