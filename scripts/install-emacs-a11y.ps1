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

function Resolve-PythonRunner {
    $candidates = @()

    $pyLauncher = Get-Command py -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        $pyExecutable = if ($pyLauncher.Source) { $pyLauncher.Source } else { $pyLauncher.Name }
        $candidates += [PSCustomObject]@{
            Executable = $pyExecutable
            PrefixArgs = @("-3")
            Display    = "py -3"
        }
    }

    $pythonCommands = Get-Command python -All -ErrorAction SilentlyContinue
    foreach ($pythonCommand in $pythonCommands) {
        $pythonExecutable = if ($pythonCommand.Source) { $pythonCommand.Source } else { $pythonCommand.Name }
        if (-not $pythonExecutable) {
            continue
        }

        # Ignora alias de WindowsApps que costuma falhar em automacao.
        if ($pythonExecutable -like "*\\WindowsApps\\python.exe") {
            continue
        }

        $candidates += [PSCustomObject]@{
            Executable = $pythonExecutable
            PrefixArgs = @()
            Display    = $pythonExecutable
        }
    }

    foreach ($candidate in $candidates) {
        $probeArgs = @()
        $probeArgs += $candidate.PrefixArgs
        $probeArgs += @("-c", "import sys; print(sys.executable)")

        $probeOutput = & $candidate.Executable @probeArgs 2>$null
        if (($LASTEXITCODE -eq 0) -and $probeOutput) {
            return $candidate
        }
    }

    return $null
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

$pythonRunner = Resolve-PythonRunner
if (-not $pythonRunner) {
    throw "Python 3.11+ nao encontrado. Instale Python ou pipx para continuar."
}

$pipInstallArgs = @()
$pipInstallArgs += $pythonRunner.PrefixArgs
$pipInstallArgs += @("-m", "pip", "install", "--user", "--upgrade", $packageSpec)

& $pythonRunner.Executable @pipInstallArgs
if ($LASTEXITCODE -ne 0) {
    throw "Falha ao instalar via pip."
}

$userBaseArgs = @()
$userBaseArgs += $pythonRunner.PrefixArgs
$userBaseArgs += @("-c", "import site; print(site.USER_BASE)")

$userBaseOutput = & $pythonRunner.Executable @userBaseArgs
$userBase = ($userBaseOutput | Where-Object { $_ -and $_.Trim() } | Select-Object -Last 1)
if (-not $userBase) {
    throw "Nao foi possivel determinar site.USER_BASE para ajustar o PATH."
}

$userBase = $userBase.Trim()
$userScripts = Join-Path $userBase "Scripts"
Ensure-UserPathEntry -Entry $userScripts

Write-Host "Instalacao concluida via pip: $packageSpec"
Write-Host "Abra um novo PowerShell e execute: emacs-a11y --help"

if (-not (($env:Path -split ';') -contains $userScripts)) {
    Write-Host "Se necessario, adicione ao PATH: $userScripts"
}
