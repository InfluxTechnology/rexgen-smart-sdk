# Rexgen Smart Hardware Architecture

## Overview

`Rexgen Smart` combines a Rexgen Core subsystem with an i.MX8 Linux host platform.

The Rexgen Smart SDK is focused on the Linux host side of this architecture.

## Main Components

### Rexgen Core

`Rexgen Core` is the MCU-based Rexgen subsystem and represents the core embedded functionality used in Rexgen products.

It is also the functional basis for `Rexgen Standalone` devices.

### i.MX8 Linux Host

The i.MX8 host runs Linux and is the application-processing side of Rexgen Smart.

This is where Linux-side services, integration logic, examples and application software run when using the SDK.

### USB Connection Between Rexgen Core And Linux Host

Within Rexgen Smart, Rexgen Core and the i.MX8 Linux host are connected over USB.

This USB link is the key integration path that allows Linux-side software to communicate with Rexgen Core through supported software interfaces.

## Product Family Positioning

### Rexgen Standalone

`Rexgen Standalone` uses Rexgen Core without the i.MX8 Linux host platform.

It is outside the main scope of this SDK.

### Rexgen Smart

`Rexgen Smart` includes:

- Rexgen Core
- i.MX8 Linux host
- USB-based integration between the two

This is the main target of the SDK.

## SDK Focus Area

The SDK is intended to support:

- Linux image build
- Linux-side software development
- integration with Rexgen Core through supported interfaces
- application bring-up and validation on supported Rexgen Smart hardware

The SDK does not define or replace all low-level firmware workflows for Rexgen Core itself.

## Relationship To RexgenLibrary

`RexgenLibrary` is a separate product: the library and tooling used for Rexgen Core / Rexgen Standalone integration workflows. It is not part of this SDK and is not built or packaged by it.

On Rexgen Smart, the i.MX8 Linux host talks to Rexgen Core over the USB link through the platform's own userspace services (`rexgen-core`, `rexgend`) and the socket control ports listed in [Hardware Interfaces](../README.md#hardware-interfaces) — not through RexgenLibrary. If a given integration needs RexgenLibrary specifically (e.g. to reuse Standalone-side logic), that dependency should be called out explicitly wherever it applies; as of this baseline, no part of the documented Smart SDK flow requires it.

## Architecture Summary

The working mental model for this SDK is:

`Rexgen Smart = Rexgen Core + i.MX8 Linux host + USB integration path`

The SDK exists to make Linux-side development on top of that platform understandable and repeatable.
