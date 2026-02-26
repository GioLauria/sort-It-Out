# Changelog

All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog" and the project follows
semantic versioning.

## [Unreleased]

- TODO: add unreleased changes

## [0.3.2] - 2026-02-26

- 3b71f16 ci(changelog): add validation workflow and check script (Giovanni Lauria)

## [0.3.1] - 2026-02-26


- Docs: moved per-algorithm documentation to `docs/algorithms/` and
  removed legacy `docs/alghorythms/` folder.
- Minor documentation updates and metadata improvements.

## [0.3.0] - 2026-02-26

- Release: packaged as `0.3.0.post1` (packaging metadata); bugfixes,
  docs and minor packaging improvements.

## [0.2.4] - 2026-02-25

- Release: patch with documentation fixes and packaging adjustments.
- Refactor: centralized algorithm registry in `src/sort_it_out/algorithms.py`.
- API/CLI: algorithm names use canonical capitalized names (e.g. `Merge`,
  `Quick`); CLI accepts case-insensitive lookup for backward compatibility.
- Docs: README and docs updated to use canonical algorithm names and
  document new GUI features.

## [0.2.3] - 2026-02-25

- Release: pushed tag `v0.2.3` with documentation updates and packaging
  tweaks.

## [0.2.2] - 2026-02-25

- Release: small fixes and documentation normalization; preparatory
  housekeeping for subsequent patch releases.

## [0.2.1] - 2026-02-25

- ci: test release automation (push tag `v0.2.1` to trigger workflow)

## [0.2.0] - 2026-02-25

- GUI: added File menu (Import, Exit), Clear button, scrollbars, and live
  items count that supports newline- or comma-separated input.
- GUI: algorithm selector now shows only algorithms that support the
  current input data types (integer-only, float-in-[0,1), homogeneous

## [0.1.3] - 2026-02-25

- CI: pushed tag `v0.1.3` (triggered release workflow).
- Misc: small fixes and housekeeping commits on `master`.

## [0.1.2] - 2026-02-25

- CI: granted `contents: write` and `packages: write` permissions to the
  release workflow so the action can create releases and upload artifacts
  without 403 errors.

## [0.1.1] - 2026-02-25

- CI: adjusted release workflow to attach `dist/**/*` and added artifact
  listing step to improve reliability of uploaded release assets.

## [0.1.0] - 2026-02-25

- Initial public release.
- Features:
  - Many handwritten sorting algorithm implementations (bubble, quick,
    merge, selection, insertion, heap, shell, counting, radix, bucket,
    comb, cocktail, gnome).
  - CLI tool `sortItOut` with stdin support and timing helpers.
  - Simple Tkinter GUI opened by default when invoked with no args.
  - Programmatic entrypoint: `sort_it_out.run(argv)`.
  - Tests (pytest), pre-commit hooks (Black, isort, flake8), and
    per-algorithm documentation under `docs/algorithms/`.
  - `launcher.py` entrypoint and PyInstaller instructions to build
    single-file executables.

### Notes

- Versioning: package now uses `setuptools_scm` to generate
  `src/sort_it_out/_version.py` at build/install time. At runtime the
  package prefers the generated version and falls back to the latest git
  tag or `0.0.0` if none is available.
