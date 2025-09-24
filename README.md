# agents-monitor-schema

> Standards Monitoring Agent for Civic Interconnect

[![Version](https://img.shields.io/badge/version-v1.0.3-blue)](https://github.com/civic-interconnect/agents-monitor-schema/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/civic-interconnect/agents-monitor-schema/actions/workflows/agent-runner.yml/badge.svg)](https://github.com/civic-interconnect/agents-monitor-schema/actions)

This agent is part of a system to monitor civic standards data sources for schema changes.

The current version monitors:

- Open Civic Data (OCD Divisions)
- OpenStates (by PluralPolicy)

OpenStates provides public API access to track U.S. state legislation and governance.

- <https://open.pluralpolicy.com/>
- <https://github.com/openstates>

## Introspection status

Introspection access for OpenStates has been requested.
This agent will activate OpenStates schema monitoring once access is granted.
Currently, we have a general API key from <https://open.pluralpolicy.com/>.

## Local development

```powershell
py -m venv .venv
.\.venv\Scripts\activate
py -m pip uninstall civic-lib-core -y
py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install --upgrade -e .[dev]
pre-commit install
schema-agent start
```

## Deployment

This agent is scheduled to run automatically using GitHub Actions.

## Before Starting Changes

```shell
git pull
```

## After Tested Changes (New Version Release)

First: Update these files to the new version:

1. VERSION file
2. README.md (update version badge)

Then run the following:

```shell
pre-commit autoupdate --repo https://github.com/pre-commit/pre-commit-hooks
ruff check . --fix
git add .
git commit -m "Release v1.0.3: works with civic-lib-core v0.9.0"
git push origin main
git tag v1.0.3
git push origin v1.0.3
```
