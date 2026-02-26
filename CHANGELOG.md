# Changelog

All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog" and the project follows
semantic versioning.

## [Unreleased]

- TODO: add unreleased changes

## [0.3.2] - 2026-02-26

- 3b71f16 ci(changelog): add validation workflow and check script (Giovanni Lauria)

## [0.3.1] - 2026-02-26

- daa9355 chore(release): v0.3.1 (Giovanni Lauria)
- f6003f5 ci(release): consider tag intervals when extracting release notes (Giovanni Lauria)

## [0.3.0] - 2026-02-26

- f5291d3 fix(gui): combined docs-finder and lint fixes (Giovanni Lauria)
- e7ecd7d ci(release): externalize release notes generator into .github/scripts/generate-release-notes.js and call from workflow (Giovanni Lauria)

## [0.2.4] - 2026-02-26

- f93acc3 ci(release): make release notes generation robust (Giovanni Lauria)
- 3951131 ci(release): robustly compute release notes using env fallback for tag ref (Giovanni Lauria)
- 10837da fix(gui): search package-installed docs via importlib.resources as fallback (Giovanni Lauria)
- 29d7c98 ci(release): prefer CHANGELOG.md entry for release notes, fallback to git log (Giovanni Lauria)
- 3e78841 chore(pyproject): enable dynamic versioning via setuptools_scm (Giovanni Lauria)
- 76cd70b chore: update version on pyproject.toml (Giovanni Lauria)
- eb8771a chore: apply formatting/lint fixes and update docs (Giovanni Lauria)

## [0.2.3] - 2026-02-26

- e8141c5 chore(release): prepare v0.2.3 (Giovanni Lauria)
- 810f7c0 style(gui): place Font size controls on same header row as Item Details before scrollbar (Giovanni Lauria)
- 67c1958 fix(gui): avoid referencing docs_size_spin before it's created (Giovanni Lauria)
- da76113 style(gui): place Font size controls on same row as Item Details and adjust docs content row (Giovanni Lauria)
- 76db7eb fix(gui): avoid overlapping docs content with Font size controls (move content down) (Giovanni Lauria)
- 5d6cdaf style(gui): align Font size label under Item Details column and right-align (Giovanni Lauria)
- 669e615 style(gui): align 'Item Details' label left with docs content; move font controls right (Giovanni Lauria)
- 3bed962 style(gui): move font controls left and rename docs label to 'Item Details' (Giovanni Lauria)
- bcb16a5 style(gui): align Repeat entry right edge with input/output area (Giovanni Lauria)
- 47e77b8 style(gui): align Repeat control with input/output and shift output/buttons (Giovanni Lauria)
- d542502 fix(gui): ensure docs font spinbox updates widget font; fix line-lengths (Giovanni Lauria)
- a303fd7 style: apply pre-commit fixes (Giovanni Lauria)

## [0.2.2] - 2026-02-26

- 92abd02 style: isort fixes (Giovanni Lauria)

## [0.2.1] - 2026-02-26

- 1bf794a ci(release): use github-script to generate release notes (fix GITHUB_OUTPUT multiline) (Giovanni Lauria)
- 5935951 chore(release): bump to 0.2.1 and add changelog entry (Giovanni Lauria)
- a2a2fe8 docs(scripts): add gen_data.md (Giovanni Lauria)
- 75719ad ci(release): generate release notes and include in release body (Giovanni Lauria)

## [0.2.0] - 2026-02-26

- 4559edd chore(release): prepare 0.2.0 changelog and bump pyproject version (Giovanni Lauria)
- d66efaf fix(gui): shorten docstring to satisfy line length (Giovanni Lauria)
- c3b4af5 feat(gui): live-update items count while editing input (Giovanni Lauria)
- e769446 docs: use canonical capitalized algorithm names in README and docs (Giovanni Lauria)
- 0c3dcdc fix(gui): remove unused variable and ensure case-insensitive lookup (Giovanni Lauria)
- 7db2547 refactor: capitalize algorithm names and make CLI lookup case-insensitive (Giovanni Lauria)
- 1db75df style(gui): place algorithm selector inline with its label (Giovanni Lauria)
- 3cafdf3 feat(gui): add Clear button to clear input and output (Giovanni Lauria)
- 74c2b4b feat(gui): show items count and update on import/sort/time (Giovanni Lauria)
- 28a64f9 feat(gui): add File menu with Import and Exit (Giovanni Lauria)
- 207312f refactor: centralize algorithm registry and fix imports (Giovanni Lauria)
- 95bd532 feat(gui): show elapsed time for sort operations in GUI (Giovanni Lauria)
- 60c4827 script: report generation time in gen_data.py (Giovanni Lauria)
- f56b6fa script: increase gen_data default max to 1_000_000_000 (Giovanni Lauria)
- cdd3354 script: fix gen_data.py defaults and add CLI args (Giovanni Lauria)
- db0aef5 script: add a script to generate random data for local testing (Giovanni Lauria)
- 5bbd18f chore: maintenance on README file (Giovanni Lauria)
- 7a38f09 docs: add CLI options examples to README (Giovanni Lauria)
- b656b3a docs: update docs for --output option, versioning and package API (Giovanni Lauria)
- b763374 feat(cli): add --output option to write sorted results to file; update README (Giovanni Lauria)
- c747d6f docs: add CHANGELOG.md (Giovanni Lauria)
- fdf6cdc docs: document recent project changes and status in README (Giovanni Lauria)

## [0.1.3] - 2026-02-26

- f241001 chore(version): integrate setuptools_scm + git tag fallback for __version__ (Giovanni Lauria)
- 3dd0756 docs: add algorithm links in README and update pyproject status (Giovanni Lauria)

## [0.1.2] - 2026-02-26

- 26b48d5 ci: grant workflow permissions for release action (Giovanni Lauria)

## [0.1.1] - 2026-02-26

- cb62719 ci: release workflow: attach dist artifacts (Giovanni Lauria)

## [0.1.0] - 2026-02-26

- a1a5a15 chore: ignore PyInstaller spec file (sortItOut.spec) (assistant) (Giovanni Lauria)
- 46d4397 ci: add release workflow (build artifacts on tag push and create GitHub Release) (assistant) (Giovanni Lauria)
- 1d8fde7 docs: update launcher path to repo root (assistant) (Giovanni Lauria)
- 559f4b0 fix(cli): open GUI when launched with no parameters (assistant) (Giovanni Lauria)
- 76eeb19 fix(cli): accept piped stdin when invoked without args (assistant) (Giovanni Lauria)
- 294e433 docs: note default GUI when invoked without args (assistant) (Giovanni Lauria)
- e6aacb0 feat(cli): open GUI when called without args (assistant) (Giovanni Lauria)
- c447f1c chore: move BUILDING_EXECUTABLES.md to project root (assistant) (Giovanni Lauria)
- 90c11e5 chore: move launcher to project root (assistant) (Giovanni Lauria)
- 8a8ab84 docs: add BUILDING_EXECUTABLES guide (assistant) (Giovanni Lauria)
- e9ab07c chore: add optional pytest pre-commit instructions and config snippet (assistant) (Giovanni Lauria)
- fe9ec4a chore: stabilize pre-commit (isort+black order, remove pytest hook) and update docs (assistant) (Giovanni Lauria)
- d703007 docs: add algorithms reference and testing guide (assistant) (Giovanni Lauria)
- 36e4ed3 feat(cli): add sortItOut CLI; update README; add .flake8 and pyproject scripts (Giovanni Lauria)
- 81f6873 docs: improve README with setup, pre-commit, usage, and links (Giovanni Lauria)
- 32a3a00 style: fix flake8 issues (rename ambiguous var, wrap long lines) (Giovanni Lauria)
- 957e7ed chore: signed commit requested by user (Giovanni Lauria)
- 84ca40c docs: add pre-commit setup instructions for Windows and Linux (Giovanni Lauria)
- 5df275e chore: add pre-commit config and docs; document pre-commit setup (Giovanni Lauria)
- ea0b774 feat(sorts): add handwritten implementations of many sorting algorithms; docs: clarify handwritten implementations (Giovanni Lauria)
- edf34b2 docs: add API and dataset docs; ci: add GitHub Actions workflow (Giovanni Lauria)
- fcd2b10 docs: add project documentation (docs/index.md) (Giovanni Lauria)
- 74e999c feat: add sorting algorithms, timing utilities, and tests; update README (Giovanni Lauria)
- ee3c501 chore: initialize SortItOut — update metadata, add package, update README (Giovanni Lauria)
- 65d3282 Initial commit (Giovanni Lauria)
