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

## Reporting

Security issues discovered in the SDK flow, release artifacts or platform integration should be reported through the appropriate internal or approved partner communication path.

The final public or partner-facing release should define the exact reporting contact and expected handling path.

## Current Documentation Gap

Before the first formal SDK release, the following should be validated and documented:

- release image credential posture
- development image credential posture
- provisioning expectations
- any relevant update or recovery security assumptions

## Release Expectation

No published SDK release should rely on public documentation that exposes personal access patterns, reusable shared credentials or unsafe production defaults.
