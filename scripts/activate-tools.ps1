# Dot-source this file: . .\scripts\activate-tools.ps1
$projectRoot = Split-Path -Parent $PSScriptRoot
$env:UV_CACHE_DIR = Join-Path $projectRoot '.cache\uv'
$env:UV_PYTHON_INSTALL_DIR = Join-Path $projectRoot '.tools\python'
$env:UV_PYTHON_BIN_DIR = Join-Path $projectRoot '.tools\bin'
$toolPaths = @(
    (Join-Path $projectRoot '.venv\Scripts'),
    (Join-Path $projectRoot '.tools\uv'),
    (Join-Path $projectRoot '.tools\bin')
)
$nodeRoot = Join-Path $projectRoot '.tools\node'
if (Test-Path -LiteralPath $nodeRoot) {
    $toolPaths += Get-ChildItem -LiteralPath $nodeRoot -Directory |
        Select-Object -ExpandProperty FullName
}
$env:PATH = ($toolPaths -join ';') + ';' + $env:PATH
