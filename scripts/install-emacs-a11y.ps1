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

    if (-not $Entry) {
        return
    }

    $Entry = $Entry.Trim()
    if (-not $Entry) {
        return
    }

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

function Resolve-UserScriptsEntries {
    param(
        [string]$PythonExecutable,
        [string[]]$PrefixArgs
    )

    $args = @()
    $args += $PrefixArgs
    $args += @("-c", "import json, os, site, sysconfig; candidates=[]; user_base=site.USER_BASE or ''; candidates.append(os.path.join(user_base, 'Scripts') if user_base else ''); scripts_nt_user=sysconfig.get_path('scripts', f'{os.name}_user') or ''; candidates.append(scripts_nt_user); localapp=os.environ.get('LOCALAPPDATA',''); candidates.append(os.path.join(localapp, 'Python', 'Scripts') if localapp else ''); pyexe=sys.executable or ''; py_dir=os.path.dirname(pyexe) if pyexe else ''; candidates.append(os.path.join(py_dir, 'Scripts') if py_dir else ''); print(json.dumps(candidates))")

    $raw = & $PythonExecutable @args
    if ($LASTEXITCODE -ne 0) {
        return @()
    }

    $jsonLine = ($raw | Where-Object { $_ -and $_.Trim() } | Select-Object -Last 1)
    if (-not $jsonLine) {
        return @()
    }

    try {
        $entries = $jsonLine | ConvertFrom-Json
    } catch {
        return @()
    }

    $result = @()
    foreach ($entry in $entries) {
        if (-not $entry) {
            continue
        }

        $trimmed = $entry.Trim()
        if (-not $trimmed) {
            continue
        }

        if (-not ($result -contains $trimmed)) {
            $result += $trimmed
        }
    }

    return $result
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

$userScriptsEntries = Resolve-UserScriptsEntries -PythonExecutable $pythonRunner.Executable -PrefixArgs $pythonRunner.PrefixArgs
if (-not $userScriptsEntries -or $userScriptsEntries.Count -eq 0) {
    throw "Nao foi possivel determinar os diretorios de Scripts do usuario para ajustar o PATH."
}

foreach ($entry in $userScriptsEntries) {
    Ensure-UserPathEntry -Entry $entry
}

$commandPath = $null
foreach ($entry in $userScriptsEntries) {
    $candidateExe = Join-Path $entry "emacs-a11y.exe"
    $candidateCmd = Join-Path $entry "emacs-a11y"

    if (Test-Path $candidateExe) {
        $commandPath = $candidateExe
        break
    }

    if (Test-Path $candidateCmd) {
        $commandPath = $candidateCmd
        break
    }
}

Write-Host "Instalacao concluida via pip: $packageSpec"
Write-Host "Abra um novo PowerShell e execute: emacs-a11y --help"

if (-not (Get-Command emacs-a11y -ErrorAction SilentlyContinue)) {
    if ($commandPath) {
        Write-Host "Comando ainda nao encontrado nesta sessao. Use temporariamente: $commandPath --help"
    }

    Write-Host "Se ainda falhar em novo terminal, confira estes diretorios no PATH de usuario:"
    foreach ($entry in $userScriptsEntries) {
        Write-Host " - $entry"
    }
}
