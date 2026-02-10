param(
    [string]$AppVersion = "2.0.0"
)

$ErrorActionPreference = "Stop"

Write-Host "[1/4] Installing Python dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host "[2/4] Building ImageResize.exe..."
python build.py

Write-Host "[3/4] Checking Inno Setup (iscc)..."
$iscc = Get-Command iscc -ErrorAction SilentlyContinue
if (-not $iscc) {
    throw "Inno Setup compiler (iscc) not found. Install Inno Setup first: https://jrsoftware.org/isdl.php"
}

Write-Host "[4/4] Building setup.exe..."
iscc "/DMyAppVersion=$AppVersion" "installer\ImageResize.iss"

Write-Host "Done. Installer created in dist\installer"
