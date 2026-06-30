# Contributing

Thank you for your interest in contributing to the Microsoft Fabric Smart Farming Analytics Platform.

This repository follows production-inspired engineering practices to maintain code quality, consistency, and a clean Git history.

## Development Workflow

Development follows a feature branch workflow.

Each new feature, enhancement, or bug fix should be developed in its own branch and merged through a Pull Request.

Example workflow:

```text
main
├── feature/business-scenario
├── feature/event-simulator
├── feature/eventstream
├── feature/eventhouse
└── bugfix/logging-error
```

## Branch Naming

Use the following naming convention:

```text
feature/<feature-name>
bugfix/<issue-name>
docs/<topic>
refactor/<component>
test/<component>
chore/<task>
```

Examples:

```text
feature/business-scenario
feature/event-catalog
feature/environmental-telemetry
docs/readme-update
refactor/config-module
```

## Commit Convention

This project follows the Conventional Commits specification.

| Type | Description |
|------|-------------|
| feat | New feature |
| fix | Bug fix |
| docs | Documentation changes |
| refactor | Code restructuring without changing behavior |
| test | Adding or updating tests |
| chore | Maintenance tasks |

Examples:

```text
feat: implement environmental telemetry generator
docs: add business scenario documentation
refactor: reorganize project structure
fix: handle missing sensor values
test: add unit tests for telemetry models
```

## Project Structure

```text
architecture/    Architecture diagrams and ADRs
config/          Configuration files
docs/            Project documentation
src/             Application source code
tests/           Unit and integration tests
```

## Coding Standards

- Follow PEP 8.
- Prefer type hints where practical.
- Keep functions focused on a single responsibility.
- Use configuration files instead of hard-coded values.
- Add logging and error handling for production-facing components.
- Write clear and descriptive commit messages.

## Pull Requests

Before opening a Pull Request, ensure that:

- The project builds successfully.
- Documentation has been updated if needed.
- New functionality includes appropriate tests where applicable.
- Commit messages follow the Conventional Commits format.

## Issues

Use GitHub Issues to report bugs, request features, or suggest improvements.

When creating an issue, include:

- Description
- Steps to reproduce (if applicable)
- Expected behavior
- Actual behavior
- Relevant logs or screenshots