param(
    [Parameter(Mandatory = $true)]
    [string]$SagaDirectory,

    [switch]$NoPause
)

$ErrorActionPreference = "Stop"
$ExitCode = 0

try {
    $SagaCommand = Join-Path $SagaDirectory "saga_cmd.exe"
    $DescriptionDirectory = Join-Path $PSScriptRoot "..\processing_saga_nextgen\description"

    if (-not (Test-Path -Path $SagaCommand -PathType Leaf)) {
        throw "SAGA executable was not found at '$SagaCommand'."
    }

    $VersionOutput = & $SagaCommand -v 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to determine the SAGA version: $VersionOutput"
    }
    if ($VersionOutput -notmatch '(?<!\d)9\.12(?:\.\d+)?(?!\d)') {
        throw "Description generation requires SAGA 9.12.x; found: $VersionOutput"
    }

    # The normal OSGeo4W/Windows binary package does not necessarily include
    # the developer tool library. Check this explicitly so that SAGA's generic
    # "select a library" error is replaced by actionable instructions.
    $LibraryOutput = & $SagaCommand dev_tools 7 -h 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0 -or $LibraryOutput -match '\[Error\]\s+select a library') {
        throw @"
The SAGA 'dev_tools' library is not available in this installation.

The QGIS interface creator is a developer tool and is commonly omitted from
pre-built OSGeo4W/Windows packages. Build SAGA 9.12.x from source with
-DWITH_DEV_TOOLS:BOOL=ON, then run this script using that build's directory.
"@
    }

    Push-Location $DescriptionDirectory
    try {
        & $SagaCommand dev_tools 7
        if ($LASTEXITCODE -ne 0) {
            throw "SAGA's QGIS interface creator failed with exit code $LASTEXITCODE."
        }
    }
    finally {
        Pop-Location
    }

    Write-Host "Generated SAGA descriptions in '$DescriptionDirectory'. Review the git diff." -ForegroundColor Green
}
catch {
    $ExitCode = 1
    Write-Host "An error occurred:`n$_" -ForegroundColor Red
}
finally {
    if (-not $NoPause) {
        Write-Host ""
        Read-Host "Press Enter to continue"
    }
}

exit $ExitCode
