param(
    [string]$buildScript
)

# Get latest PSAKE version
Write-Host "Getting latest version..."
$latestVersion = Invoke-RestMethod -Uri "https://api.github.com/repos/psake/psake/releases/latest" | Select -ExpandProperty "name"
Write-Host "Latest version is: $latestVersion" -ForegroundColor Green

#Check if we have latest version if not download
$psakeZip = "$PSScriptRoot\$latestVersion.zip"

if (-Not (Test-Path $psakeZip)) {
    Write-Host "Downloading psake $latestVersion..."
    $downloadUrl = "https://github.com/psake/psake/archive/$latestVersion.zip"
    Invoke-WebRequest -Uri $downloadUrl -OutFile $psakeZip
    Write-Host "psake $latestVersion downloaded to $PSScriptRoot!" -ForegroundColor Green    
}

$archivePath = "psake-" + $latestVersion.TrimStart('v')

#Check if we have the archive extracted if not extract it
if(-Not (Test-Path $archivePath)) {
    Write-Host "Extracting archive to $PSScriptRoot..."
    Expand-Archive -Path $psakeZip -DestinationPath $PSScriptRoot
    Write-Host "Archive unpacked!" -ForegroundColor Green
}


$psakePath = "$archivePath\psake.ps1"

if (-Not (Test-Path $psakePath)) {
    throw [System.IO.FileNotFoundException] "$psakePath not found."
}

# Invoke the psake build file
Write-Host "Running Psake build file $buildScript!" -ForegroundColor Green
& $psakePath $buildScript