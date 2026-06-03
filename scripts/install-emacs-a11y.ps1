$ErrorActionPreference = "Stop"

$packageName = "emacs-a11y-installer"
$version = $env:EMACS_A11Y_VERSION

function Normalize-Version {
    param([string]$Value)

    if (-not $Value) {
        return $null
    }

    return $Value.TrimStart('v')
}

function Resolve-PackageSpec {
    param([string]$Name, [string]$Version)

    $normalized = Normalize-Version -Value $Version
    if ($normalized) {
        return "$Name==$normalized"
    }

    return $Name
}

function Ensure-UserPathEntry {
    param([string]$Entry)

    $currentUserPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $pathParts = @()
    if ($currentUserPath) {
        $pathParts = $currentUserPath -split ';'
    }

    if ($pathParts -contains $Entry) {
        return
    }

    $updated = if ($currentUserPath) {
        "$currentUserPath;$Entry"
    } else {
        $Entry
    }

    [Environment]::SetEnvironmentVariable("Path", $updated, "User")

    if (-not (($env:Path -split ';') -contains $Entry)) {
        $env:Path = "$env:Path;$Entry"
    }
}

$packageSpec = Resolve-PackageSpec -Name $packageName -Version $version

if (Get-Command pipx -ErrorAction SilentlyContinue) {
    pipx install --force $packageSpec
    if ($LASTEXITCODE -ne 0) {
        throw "Falha ao instalar via pipx."
    }

    Write-Host "Instalacao concluida via pipx: $packageSpec"
    Write-Host "Execute: emacs-a11y --help"
    exit 0
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command py -ErrorAction SilentlyContinue
}

if (-not $python) {
    throw "Python 3.11+ nao encontrado. Instale Python ou pipx para continuar."
}

$pythonCmd = $python.Name
$pipInstallArgs = @("-m", "pip", "install", "--user", "--upgrade", $packageSpec)
& $pythonCmd @pipInstallArgs
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao instalar via pip."
}

$userBase = & $pythonCmd -c "import site; print(site.USER_BASE)"
$userScripts = Join-Path $userBase "Scripts"
Ensure-UserPathEntry -Entry $userScripts

Write-Host "Instalacao concluida via pip: $packageSpec"
Write-Host "Abra um novo PowerShell e execute: emacs-a11y --help"

if (-not (($env:Path -split ';') -contains $userScripts)) {
    Write-Host "Se necessario, adicione ao PATH: $userScripts"
}
