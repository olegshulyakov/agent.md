---
name: writer-readme
description: >
  Use this skill whenever the user wants to write or improve a README, create project documentation,
  write a project overview, document how to install or run something, or asks "can you write a README for this?"
  Also trigger for "update the README", "document this project", "write the docs for this repo",
  or "help someone get started with this project".
author: Oleg Shulyakov
licence: MIT
version: 1.0.0
---

# writer-readme

Produce a **complete, professional README.md** that gives any reader — new contributor, user, or evaluator — everything they need to understand, install, and use the project.

## Understand the audience before writing

A README serves different readers differently. Detect the primary audience from context:

| Signal               | Audience                                      | Tone                            |
| -------------------- | --------------------------------------------- | ------------------------------- |
| Library / package    | Developers who want to use it as a dependency | Technical, API-forward          |
| CLI tool             | Developers and power users running commands   | Command-focused, example-heavy  |
| Web service / API    | Developers integrating with the API           | Endpoint-forward, auth-focused  |
| Internal tool / repo | Team members                                  | More casual, context-assumed    |
| Open source project  | Community contributors                        | Welcoming, contribution-focused |

## Information gathering

Read the repository or ask for:

- **What does this project do?** (1-sentence answer)
- **Primary language and framework**
- **How to install / run it**
- **Main use cases and quick example**
- **Contributing and license info** (if applicable)

If you have access to the codebase, read: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or equivalent — they contain name, description, version, and dependencies.

## Output format

Produce `README.md` with badges, sections, and examples appropriate to the project type.

````markdown
# [Project Name]

<!-- Optional: project logo or hero image -->

> [One-sentence description: what it does and why it's useful]

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)]()

<!-- Add CI badge if CI is detected: [![CI](https://github.com/[org]/[repo]/actions/workflows/[file].yml/badge.svg)](https://github.com/[org]/[repo]/actions) -->

## Overview

[2–4 sentences expanding on the one-liner: the problem it solves, who uses it, and what makes it notable.
Skip this section if the project is very simple — the one-liner is enough.]

## Features

- **[Feature]** — [brief value statement]
- **[Feature]** — [brief value statement]

[Omit if the project is simple or the overview covers it.]

## Requirements

| Dependency                     | Minimum Version |
| ------------------------------ | --------------- |
| [Node.js / Python / Go / etc.] | [version]       |
| [Other dependency]             | [version]       |

## Installation

[Choose the right pattern for the project type:]

**Package manager:**

```bash
npm install [package-name]

# or

pip install [package-name]
```

**From source:**

```bash
git clone https://github.com/[org]/[repo].git
cd [repo]
[install command: npm install / pip install -e . / go mod download / cargo build]
```

**Docker:**

```bash
docker pull [image]:[tag]
```

## Quick Start

[The most important section. Show the most common use case working end-to-end in < 10 lines.]

```[language]
[working example code]
```

[Expected output:]

```
[what the user should see]
```

## Usage

### [Common Use Case 1]

```[language]
[example]
```

### [Common Use Case 2]

```[language]
[example]
```

## Configuration

[Only if the project has meaningful configuration.]

| Variable / Option | Default     | Description        |
| ----------------- | ----------- | ------------------ |
| `[CONFIG_VAR]`    | `[default]` | [what it controls] |

Configuration can be set via:

- Environment variables: `export [VAR]=value`
- Config file: `[filename]` in the project root
- CLI flags: `--[flag]` (see `[command] --help`)

## API Reference

[For libraries: key public API surface. For services: link to OpenAPI spec or list key endpoints.
For CLIs: the full flag/command reference. Skip for simple scripts.]

## Development

```bash

# Install dev dependencies

[command]

# Run tests

[test command]

# Run linter

[lint command]

# Build

[build command]
```

## Contributing

[Keep brief unless this is an open source project.]

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/your-feature`)
3. Commit your changes (follow [conventional commits](https://www.conventionalcommits.org))
4. Open a pull request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details. [Omit if no CONTRIBUTING.md exists.]

## License

[License name] — see [LICENSE](LICENSE) for details.
````

## Adaptive rules

**For libraries:** Lead with a code example in the README's first screenful. Developers decide in seconds whether to read further.

**For CLIs:** Show `--help` output or a command table early. Users often read README on the CLI's homepage.

**For internal tools:** Omit badges, Contributing, and License. Add a "Who maintains this?" section.

**For open source:** Add a "Roadmap" or "Status" section if the project is early-stage. Add a "Support" section with community links.

**When reading an existing codebase:** Extract the project name from `package.json`/`pyproject.toml`, look for existing docs in `/docs`, and check for existing `README.md` to improve rather than overwrite.

## Quality checklist

Before outputting:

- [ ] Does the first paragraph explain what it does AND why it's useful?
- [ ] Is there a working code example in the first screenful?
- [ ] Are all install commands tested / plausible?
- [ ] Are there no placeholder `[YOUR_VALUE]` strings left in the output?
- [ ] Is the length proportional to the project's complexity?
