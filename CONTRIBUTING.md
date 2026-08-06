# Contributing

This repository is the documentation, manifest, and examples entry point for the Rexgen Smart SDK. It is maintained by InfluxTechnology; external contributions are welcome within the scope below.

## Scope

Good contributions here:

- fixes to documentation (broken links, stale facts, unclear instructions)
- new or improved examples under [examples/](examples/README.md) (bug fixes, additional languages, new interfaces)
- fixes to the CI/lint setup under [.github/workflows/](.github/workflows/)

Out of scope for this repository (see [SUPPORT.md](SUPPORT.md)):

- changes to the platform/BSP itself (`influx-yocto-base`, `meta-influx`) — those live in their own repositories
- Rexgen Standalone firmware
- undocumented internal interfaces

## Before You Start

For anything beyond a small fix (a new example, a documentation restructure), open an issue first to confirm the direction before investing time in a PR.

## Filing An Issue

Use the issue templates (bug report / documentation issue) where they fit. At minimum, include:

- what you expected vs. what happened
- exact commands run, and their full output
- your host OS/version, and the SDK/BSP version pair from [Version Baseline](README.md#version-baseline)

Security vulnerabilities go to **security@influxtechnology.com** (see [SECURITY.md](SECURITY.md)) — not a public issue.

## Submitting A Change

1. Fork the repository and branch from `main`.
2. Keep the change focused — one fix or one example per PR.
3. If you touch `examples/`, make sure it still passes the CI lint checks (ShellCheck, Python/Node.js syntax, manifest XML validation — see [.github/workflows/lint-examples.yml](.github/workflows/lint-examples.yml)); you can run the same checks locally:
   ```sh
   shellcheck examples/**/*.sh
   find examples -name '*.py' -exec python3 -m py_compile {} \;
   find examples -name '*.js' -exec node --check {} \;
   ```
4. Open a PR against `main` describing what changed and why.

## Style

Match the existing tone: declarative statements of current fact, not aspirational "should be" language. If something is genuinely unfinished, say so explicitly (see the "Known Limitations" sections in [RELEASE_NOTES.md](RELEASE_NOTES.md)) rather than describing a plan as if it were done.
