# Doctor CLI Contract

## Commands
- `emacs-a11y doctor`
- `emacs-a11y doctor --json`

## Behavior
- MUST run in strict read-only mode.
- MUST NOT:
  - modify files
  - create directories
  - install dependencies
  - download binaries
  - alter PATH
  - request admin privileges

## Output modes

### Text mode
- Linear, screen-reader-friendly output.
- Ordered sections:
  - Summary
  - Critical
  - Warnings
  - Info
  - Next steps

### JSON mode
- JSON object following `doctor-report.schema.json`.
- Semantic parity with text mode for the same execution context.

## Exit codes
- `0`: ready (no warnings, no critical)
- `1`: warnings present, no critical
- `2`: at least one critical
- `3`: internal diagnostic execution error

## Distribution parity
- Canonical channel: Python package (pipx-compatible).
- Optional standalone executables MUST preserve command behavior, output semantics and exit code mapping.

## Script boundary
- `.ps1` / `.sh` wrappers MAY call the command but MUST NOT implement diagnostic business rules.
