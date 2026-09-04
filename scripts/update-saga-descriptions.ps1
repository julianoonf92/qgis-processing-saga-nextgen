param(
    [Parameter(Mandatory = $true)]
    [string]$SagaDirectory
)

$ErrorActionPreference = "Stop"
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

Write-Host "Generated SAGA descriptions in '$DescriptionDirectory'. Review the git diff."
