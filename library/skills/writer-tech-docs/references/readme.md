# writer-tech-docs — readme variant

Produce a **complete, professional README.md** that gives any reader everything they need to understand, install, and use the project.

## Understand the audience

| Signal               | Audience                            | Tone                            |
| -------------------- | ----------------------------------- | ------------------------------- |
| Library / package    | Developers using it as a dependency | Technical, API-forward          |
| CLI tool             | Developers and power users          | Command-focused, example-heavy  |
| Web service / API    | Developers integrating              | Endpoint-forward, auth-focused  |
| Internal tool / repo | Team members                        | More casual, context-assumed    |
| Open source project  | Community contributors              | Welcoming, contribution-focused |

## Information gathering

Read the codebase or ask for: what does it do (1 sentence), primary language and framework, how to install/run, main use cases, contributing and license info.

If code is available, read: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod` — they contain name, description, version, dependencies.

## Output format

````markdown
# [Project Name]

<!-- Optional: project logo or hero image -->

> [One-sentence description: what it does and why it's useful]

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)]()

## Overview

[2–4 sentences expanding on the one-liner: the problem it solves, who uses it, and what makes it notable.]

## Features

- **[Feature]** — [brief value statement]
- **[Feature]** — [brief value statement]

## Requirements

| Dependency                     | Minimum Version |
| ------------------------------ | --------------- |
| [Node.js / Python / Go / etc.] | [version]       |

## Installation

**Package manager:**

```bash
npm install [package-name]
```

**From source:**

```bash
git clone https://github.com/[org]/[repo].git
cd [repo]
[install command]
```

**Docker:**

```bash
docker pull [image]:[tag]
```

## Quick Start

[Working end-to-end example in < 10 lines.]

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

## Configuration

| Variable / Option | Default     | Description        |
| ----------------- | ----------- | ------------------ |
| `[CONFIG_VAR]`    | `[default]` | [what it controls] |

## API Reference

[Key public API surface, link to OpenAPI spec, or list key endpoints.]

## Development

```bash
# Install dev dependencies
[command]
# Run tests
[test command]
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feat/your-feature`)
3. Commit your changes (follow [conventional commits](https://www.conventionalcommits.org))
4. Open a pull request

## License

[License name] — see [LICENSE](LICENSE) for details.
````

## Adaptive rules

- **Libraries**: Lead with a code example in the first screenful
- **CLIs**: Show `--help` output or a command table early
- **Internal tools**: Omit badges, Contributing, License. Add "Who maintains this?" section
- **Open source**: Add "Roadmap" or "Status" if early-stage. Add "Support" with community links
- **Existing codebase**: Extract project name from `package.json`/`pyproject.toml`, check `/docs`, and improve rather than overwrite

## Quality checklist

- [ ] First paragraph explains what it does AND why it's useful
- [ ] Working code example in the first screenful
- [ ] All install commands tested / plausible
- [ ] No placeholder `[YOUR_VALUE]` strings left in the output
- [ ] Length proportional to the project's complexity
