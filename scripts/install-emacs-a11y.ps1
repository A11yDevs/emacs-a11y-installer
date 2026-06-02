$ErrorActionPreference = "Stop"

$repo = "A11yDevs/emacs-a11y-installer"
$installDir = if ($env:EMACS_A11Y_INSTALL_DIR) {
    $env:EMACS_A11Y_INSTALL_DIR
} else {
    Join-Path $env:LOCALAPPDATA "Programs\emacs-a11y\bin"
}

$version = $env:EMACS_A11Y_VERSION

function Get-LatestTag {
    param([string]$Repository)

    $apiUrl = "https://api.github.com/repos/$Repository/releases/latest"
    $release = Invoke-RestMethod -Uri $apiUrl
    if (-not $release.tag_name) {
        throw "Nao foi possivel detectar tag da release mais recente."
    }
    return [string]$release.tag_name
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

if (-not $version) {
    $version = Get-LatestTag -Repository $repo
}

$assetName = "emacs-a11y-$version-windows-x64.zip"
$assetUrl = "https://github.com/$repo/releases/download/$version/$assetName"

$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("emacs-a11y-install-" + [Guid]::NewGuid().ToString("N"))
$archivePath = Join-Path $tempRoot $assetName
$extractPath = Join-Path $tempRoot "extract"

New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null
New-Item -ItemType Directory -Path $extractPath -Force | Out-Null

try {
    Invoke-WebRequest -Uri $assetUrl -OutFile $archivePath
    Expand-Archive -Path $archivePath -DestinationPath $extractPath -Force

    $sourceExe = Join-Path $extractPath "emacs-a11y.exe"
    if (-not (Test-Path $sourceExe)) {
        throw "Executavel emacs-a11y.exe nao encontrado no pacote da release."
    }

    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
    Copy-Item -Path $sourceExe -Destination (Join-Path $installDir "emacs-a11y.exe") -Force

    Ensure-UserPathEntry -Entry $installDir

    Write-Host "Instalacao concluida: $(Join-Path $installDir 'emacs-a11y.exe')"
    Write-Host "PATH do usuario atualizado. Abra um novo PowerShell e execute: emacs-a11y --help"
}
finally {
    if (Test-Path $tempRoot) {
        Remove-Item -Path $tempRoot -Recurse -Force
    }
}
