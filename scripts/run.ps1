$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$projectPython = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $projectPython)) {
    throw 'Python environment is missing. See docs/environment-setup.md.'
}
Push-Location $projectRoot
try {
    & $projectPython -m terminal.ui.application @args
    exit $LASTEXITCODE
} finally {
    Pop-Location
}
