# Rexgen Smart SDK Positioning Draft

## Official Definition

`Rexgen Smart SDK` is the official development package for building Linux-side software on Rexgen Smart devices.

It provides the build environment, documentation, platform integration flow and example starting points needed to build, deploy and validate software running on the i.MX8 Linux host in a Rexgen Smart system.

The SDK is intended for internal developers, integration engineers and approved partners who need to build Linux images, run supported examples and develop Linux-side applications that interact with Rexgen Smart platform services and Rexgen Core.

## Short Version

`Rexgen Smart SDK` is the official software development package for Rexgen Smart.

It enables developers to build Rexgen Smart Linux images, flash supported hardware and create Linux-side applications on top of the supported platform stack.

## Supported

- building supported Rexgen Smart Linux images
- using the documented Yocto-based build flow
- flashing supported Rexgen Smart hardware
- developing Linux-side applications for the i.MX8 host
- interacting with Rexgen Core through documented and supported platform interfaces
- running and adapting official SDK examples
- using the SDK on the supported branch, release and hardware scope defined in release notes

## Not Supported

- Rexgen Standalone firmware development
- arbitrary customer forks outside the documented SDK flow
- undocumented internal interfaces treated as stable APIs
- unsupported hardware revisions or unofficial board variants
- production security policy customizations outside the documented release process
- custom Linux platform changes not covered by the supported SDK release

## Official Terminology

| Term | Meaning |
|---|---|
| `Rexgen Core` | The MCU-based Rexgen subsystem used as the core functional unit in Rexgen products. |
| `Rexgen Standalone` | A Rexgen device based on Rexgen Core without the i.MX8 Linux host platform. |
| `RexgenLibrary` | The software library and related tooling used for Rexgen Core and Rexgen Standalone integration workflows. |
| `Rexgen Smart` | A Rexgen system that combines Rexgen Core with an i.MX8 Linux host connected through USB. |
| `Rexgen Smart SDK` | The official Linux-side development package for building, deploying and validating software on Rexgen Smart. |
| `Rexgen PRO` | The official Rexgen Smart product application or application layer delivered by the company. |
| `Rexgen OEM` | Customer-specific or partner-specific applications and integrations built on or for Rexgen Smart. |

## Notes For README Usage

The first paragraph of the README can use this shorter wording:

`Rexgen Smart SDK is the official development package for building Linux-side software on Rexgen Smart devices. It provides the documented build flow, platform integration path and example starting points needed to build images, flash devices and develop applications on the i.MX8 Linux host.`

The README should also include a short scope block:

- Supported: Linux-side development for supported Rexgen Smart hardware and releases
- Not supported: Rexgen Standalone firmware development and undocumented internal interfaces
