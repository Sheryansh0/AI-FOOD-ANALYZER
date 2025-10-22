# Push Food Analyzer Backend to Docker Hub
# This script tags and pushes the Docker image to Docker Hub

param(
    [Parameter(Mandatory=$true)]
    [string]$DockerHubUsername
)

$ImageName = "food-analyzer-backend"
$Tag = "latest"

Write-Host "🐳 Pushing to Docker Hub" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Step 1: Tag the image for Docker Hub
Write-Host "`n✓ Step 1: Tagging image..." -ForegroundColor Yellow
$DockerHubImage = "${DockerHubUsername}/${ImageName}:${Tag}"
docker tag $ImageName $DockerHubImage

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to tag image" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Tagged as: $DockerHubImage" -ForegroundColor Green

# Step 2: Push to Docker Hub
Write-Host "`n✓ Step 2: Pushing to Docker Hub..." -ForegroundColor Yellow
Write-Host "This may take several minutes (image is ~2-3GB with models)..." -ForegroundColor Yellow
docker push $DockerHubImage

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to push image" -ForegroundColor Red
    exit 1
}

# Step 3: Also tag as version
$Version = Get-Date -Format "yyyyMMdd-HHmm"
$VersionedImage = "${DockerHubUsername}/${ImageName}:${Version}"
Write-Host "`n✓ Step 3: Creating versioned tag..." -ForegroundColor Yellow
docker tag $ImageName $VersionedImage
docker push $VersionedImage

Write-Host ""
Write-Host "=================================================" -ForegroundColor Green
Write-Host "SUCCESS! Image pushed to Docker Hub" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your images are now available at:" -ForegroundColor Cyan
Write-Host "  Latest: $DockerHubImage" -ForegroundColor White
Write-Host "  Version: $VersionedImage" -ForegroundColor White
Write-Host ""
Write-Host "To pull this image on any machine:" -ForegroundColor Yellow
Write-Host "  docker pull $DockerHubImage" -ForegroundColor White
Write-Host ""
Write-Host "For Azure deployment, use:" -ForegroundColor Yellow
Write-Host "  $DockerHubImage" -ForegroundColor White
Write-Host ""
Write-Host "=================================================" -ForegroundColor Green
