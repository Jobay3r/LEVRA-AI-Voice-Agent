# Create and setup the AI virtual environment
Write-Host "Setting up AI environment..." -ForegroundColor Green

# Create virtual environment if it doesn't exist
if (-not (Test-Path "Scripts\python.exe")) {
    Write-Host "Creating virtual environment..."
    python -m venv .
}

# Activate virtual environment and install requirements
Write-Host "Activating virtual environment and installing packages..."
& ".\Scripts\Activate.ps1"
& ".\Scripts\pip.exe" install -r requirements.txt

Write-Host ""
Write-Host "AI environment setup complete!" -ForegroundColor Green
Write-Host "To activate: cd ai; .\Scripts\Activate.ps1"
