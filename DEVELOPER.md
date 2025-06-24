# DEVELOPER.md

## Setup for Running Agent

1. Fork the repo.
2. Clone your fork and open it in VS Code.
3. Open a terminal (examples below use PowerShell on Windows).

```powershell
git clone https://github.com/civic-interconnect/agents-monitor-schema.git
cd agents-monitor-schema

py -m venv .venv
.\.venv\Scripts\activate
py -m pip install --upgrade pip setuptools wheel --prefer-binary
py -m pip install -e .[dev]
schema-agent start
```

## Releasing New Version

After verifying changes:

```powershell
civic-dev prep-code
civic-dev bump-version 1.0.1 1.0.2
civic-dev release
```
