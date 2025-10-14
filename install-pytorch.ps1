# Install PyTorch and Dependencies for Local Models

Write-Host "================================" -ForegroundColor Cyan
Write-Host "Installing PyTorch Dependencies..." -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
& ".\venv\Scripts\Activate.ps1"

Write-Host "Installing PyTorch (CPU version)..." -ForegroundColor Yellow
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

Write-Host ""
Write-Host "Installing timm (PyTorch Image Models)..." -ForegroundColor Yellow
pip install timm==0.9.12

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your local models are now ready to use!" -ForegroundColor Green
Write-Host ""

pause
