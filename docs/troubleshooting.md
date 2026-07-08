# Troubleshooting

## Purpose

This document collects the most common issues encountered while using the Rexgen Smart SDK baseline flow.

It should be updated whenever a setup, build, flash or runtime issue is discovered and resolved.

## Source Sync Problems

Typical areas to check:

- repository access permissions
- incorrect branch or manifest selection
- incomplete sync
- network interruptions during source retrieval

## Build Environment Problems

Typical areas to check:

- missing host dependencies
- wrong shell or environment initialization
- unsupported host operating system version
- incorrect machine configuration

## Build Failures

Typical areas to check:

- wrong image target name
- missing layers or incomplete source sync
- local environment contamination
- insufficient disk space or memory

When documenting a real issue here, include:

- symptom
- likely cause
- confirmed fix
- whether the issue affects all users or only specific host setups

## Flashing Problems

Typical areas to check:

- wrong target image
- wrong hardware revision
- failed recovery mode entry
- host flashing tool issues
- cable or interface problems

## Boot Problems

Typical areas to check:

- corrupted image artifact
- mismatched image and hardware revision
- incomplete flashing
- platform services failing to start

## Example Execution Problems

Typical areas to check:

- missing runtime dependencies
- unsupported example assumptions
- missing access to supported platform interfaces
- incorrect environment on the target

## Documentation Discipline

Every time a real issue is fixed, this file should be updated with:

- the observable symptom
- the confirmed resolution
- any required preventive note for future users
