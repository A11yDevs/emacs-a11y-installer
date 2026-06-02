Param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

if ($Clean -and (Test-Path "build")) {
    Remove-Item -Recurse -Force "build"
}

if ($Clean -and (Test-Path "dist")) {
    Remove-Item -Recurse -Force "dist"
}

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pip install pyinstaller

pyinstaller `
  --noconfirm `
  --clean `
  --onefile `
  --name emacs-a11y `
  --collect-data emacs_a11y `
  --collect-data emacs_a11y.resources `
  src/emacs_a11y/cli/doctor.py

Write-Host "Gerado: dist/emacs-a11y.exe"
