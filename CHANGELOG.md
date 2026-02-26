# Changelog

All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog" and the project follows
semantic versioning.

## [Unreleased]

- TODO: add unreleased changes

## [0.3.3] - 2026-02-26

### Chores

- regenerate CHANGELOG from git tags
- update CHANGELOG for v0.3.2 (include commits)
- update CHANGELOG for v0.3.2

### CI

- add changelog updater workflow and script; chore(release): update CHANGELOG for v0.3.1

## [0.3.2] - 2026-02-26

### CI

- add validation workflow and check script

## [0.3.1] - 2026-02-26

### Chores

- v0.3.1

### CI

- consider tag intervals when extracting release notes

## [0.3.0] - 2026-02-26

### Fixed

- combined docs-finder and lint fixes

### CI

- externalize release notes generator into .github/scripts/generate-release-notes.js and call from workflow

## [0.2.4] - 2026-02-26

### Fixed

- search package-installed docs via importlib.resources as fallback

### Chores

- enable dynamic versioning via setuptools_scm
- update version on pyproject.toml
- apply formatting/lint fixes and update docs

### CI

- make release notes generation robust
- robustly compute release notes using env fallback for tag ref
- prefer CHANGELOG.md entry for release notes, fallback to git log

## [0.2.3] - 2026-02-26

### Fixed

- avoid referencing docs_size_spin before it's created
- avoid overlapping docs content with Font size controls (move content down)
- ensure docs font spinbox updates widget font; fix line-lengths

### Chores

- prepare v0.2.3

### Style

- place Font size controls on same header row as Item Details before scrollbar
- place Font size controls on same row as Item Details and adjust docs content row
- align Font size label under Item Details column and right-align
- align 'Item Details' label left with docs content; move font controls right
- move font controls left and rename docs label to 'Item Details'
- align Repeat entry right edge with input/output area
- align Repeat control with input/output and shift output/buttons
- apply pre-commit fixes

## [0.2.2] - 2026-02-26

### Style

- isort fixes

## [0.2.1] - 2026-02-26

### Documentation

- add gen_data.md

### Chores

- bump to 0.2.1 and add changelog entry

### CI

- use github-script to generate release notes (fix GITHUB_OUTPUT multiline)
- generate release notes and include in release body

## [0.2.0] - 2026-02-26

### Added

- live-update items count while editing input
- add Clear button to clear input and output
- show items count and update on import/sort/time
- add File menu with Import and Exit
- show elapsed time for sort operations in GUI
- add --output option to write sorted results to file; update README

### Changed

- capitalize algorithm names and make CLI lookup case-insensitive
- centralize algorithm registry and fix imports

### Fixed

- shorten docstring to satisfy line length
- remove unused variable and ensure case-insensitive lookup

### Documentation

- use canonical capitalized algorithm names in README and docs
- add CLI options examples to README
- update docs for --output option, versioning and package API
- add CHANGELOG.md
- document recent project changes and status in README

### Chores

- prepare 0.2.0 changelog and bump pyproject version
- maintenance on README file

### Style

- place algorithm selector inline with its label

### Other

- report generation time in gen_data.py
- increase gen_data default max to 1_000_000_000
- fix gen_data.py defaults and add CLI args
- add a script to generate random data for local testing

## [0.1.3] - 2026-02-26

### Documentation

- add algorithm links in README and update pyproject status

### Chores

- integrate setuptools_scm + git tag fallback for __version__

## [0.1.2] - 2026-02-26

### CI

- grant workflow permissions for release action

## [0.1.1] - 2026-02-26

### CI

- release workflow: attach dist artifacts

## [0.1.0] - 2026-02-26

### Added

- open GUI when called without args (assistant)
- add sortItOut CLI; update README; add .flake8 and pyproject scripts
- add handwritten implementations of many sorting algorithms; docs: clarify handwritten implementations
- add sorting algorithms, timing utilities, and tests; update README

### Fixed

- open GUI when launched with no parameters (assistant)
- accept piped stdin when invoked without args (assistant)

### Documentation

- update launcher path to repo root (assistant)
- note default GUI when invoked without args (assistant)
- add BUILDING_EXECUTABLES guide (assistant)
- add algorithms reference and testing guide (assistant)
- improve README with setup, pre-commit, usage, and links
- add pre-commit setup instructions for Windows and Linux
- add API and dataset docs; ci: add GitHub Actions workflow
- add project documentation (docs/index.md)

### Chores

- ignore PyInstaller spec file (sortItOut.spec) (assistant)
- move BUILDING_EXECUTABLES.md to project root (assistant)
- move launcher to project root (assistant)
- add optional pytest pre-commit instructions and config snippet (assistant)
- stabilize pre-commit (isort+black order, remove pytest hook) and update docs (assistant)
- signed commit requested by user
- add pre-commit config and docs; document pre-commit setup
- initialize SortItOut — update metadata, add package, update README

### CI

- add release workflow (build artifacts on tag push and create GitHub Release) (assistant)

### Style

- fix flake8 issues (rename ambiguous var, wrap long lines)

### Other

- Initial commit
