# Local Windows environment

Prepared on 2026-11-17 (Asia/Seoul). All development tools and Python packages
live inside this project; system PATH and existing applications are unchanged.

Verified tool versions: Python 3.13.18, uv 0.13.8, Node.js LTS 26.13.1,
npm 11.20.0, PySide6 6.12.0. Exact Python dependencies are recorded in the
183-package `.tools/requirements-installed.txt` inventory (the editable project
itself is excluded).

## Start

```powershell
.\.venv\Scripts\python.exe -m terminal.ui.application
# Or: powershell -ExecutionPolicy Bypass -File .\scripts\run.ps1
```

Double-click `start-terminal.cmd` to launch the GUI. To open a terminal with
Python, uv, Node, and npm on its temporary PATH:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -NoExit -Command ". .\scripts\activate-tools.ps1"
```

This process-only execution policy allows the local helper scripts without
changing the machine or user execution policy.

`nextgen-terminal` is the core readiness check, not the GUI launcher.
The application currently uses synthetic data. Installing provider SDKs does
not implement or activate live providers. API credentials remain user supplied.

## Contents

- `.tools/uv/`: standalone uv package/environment manager.
- `.tools/python/`: managed CPython 3.13 runtime.
- `.venv/`: all application dependencies, including `ui`, `security`, and `dev`.
- `requirements-workbench.in`: additional build/packaging tools, Qt testing,
  coverage/debugging, financial analysis, notebooks, HTTP/streaming libraries,
  document parsing, and SDKs for the planned Alpaca/Tiingo providers.
- `.tools/node/`: portable Node.js LTS and npm for JavaScript chart maintenance.
- `.tools/downloads/`: original tool archives and signed Microsoft VC++ x64
  redistributable installer (downloaded for Windows deployment).
- `.cache/uv/`: retained resolver, build, and package cache.
- `.tools/requirements-installed.txt`: exact installed Python package versions.
- `.tools/downloads/wheels/`: retained pip-compatible Python package downloads.

All 183 pinned third-party packages have retained wheels (444.9 MiB total).
Offline dependency resolution with `--no-index --ignore-installed --dry-run`
passed for the full pinned workbench plus all project extras. Download hashes
are recorded in `.tools/downloads/SHA256SUMS.txt`; the offline validation log is
`.tools/offline-resolution-check.txt`.

Large local tools, caches, and virtual environments are ignored by Git.
`README.md` was already ignored by this repository; a local copy supplies the
readme referenced by `pyproject.toml`, required when building the package.

## Reinstall packages using the prepared runtime

```powershell
. .\scripts\activate-tools.ps1
uv venv --python 3.13 --seed .venv
uv pip install --python .venv\Scripts\python.exe -e '.[ui,security,dev]' -r requirements-workbench.in
```

To restore exact downloaded versions from the wheel archive on this Windows
x64 / CPython 3.13 environment:

```powershell
python -m pip install --no-index --find-links .tools\downloads\wheels -r .tools\requirements-installed.txt
python -m pip install --no-index --find-links .tools\downloads\wheels --no-build-isolation -e '.[ui,security,dev]'
```

The project directory and managed Python runtime must remain together; copying
only `.venv` to another location does not make it portable.

## Validation and builds

```powershell
python -m pytest
python -m pip check
ruff check src tests
$env:MYPYPATH = Join-Path $PWD 'src'
mypy --python-version 3.13
python -m build --no-isolation
```

Python's build module creates wheel/source distributions, not a Windows GUI
executable. PyInstaller is installed for subsequent executable packaging.
The QtWebEngine/Chromium runtime is included with the PySide6 dependencies;
no separate browser or Qt SDK is required to run the application.

Validation results: 21 unit tests passed; `pip check` and Ruff passed; mypy
passed for all 34 source files with the Python 3.13 override; source and wheel
distributions built successfully in `dist/`. A separate smoke check created
the onboarding widget, loaded the bundled Lightweight Charts 5.0.9 JavaScript
through QtWebEngine, and selected the Windows `WinVaultKeyring` backend without
writing user state or credentials. Additional workbench library imports and
Node/npm version commands passed.

The repository's default mypy Python 3.11 target cannot parse the latest NumPy
typing syntax. The explicit Python 3.13 command above matches this environment;
the project's declared minimum Python version was not changed.

The Microsoft VC++ installer is retained for deployment and its Authenticode
signature was validated as Microsoft Corporation. It was not run because the
installed Qt/Python components already loaded successfully. The Node archive
was checked against its official SHA-256 manifest.

Official tool documentation: [uv installation](https://docs.astral.sh/uv/getting-started/installation/),
[managed Python](https://docs.astral.sh/uv/guides/install-python/).
