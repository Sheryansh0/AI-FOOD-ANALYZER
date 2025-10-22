# Deploy Food Analyzer Backend to Azure Container Instance
# Uses Docker Hub image: sheryansh/food-analyzer-backend:latest

param(
    [Parameter(Mandatory=$true)]
    [string]$GeminiApiKey,
    
    [Parameter(Mandatory=$false)]
    [string]$ResourceGroup = "food-analyzer-rg",
    
    [Parameter(Mandatory=$false)]
    [string]$Location = "eastus",
    
    [Parameter(Mandatory=$false)]
    [string]$ContainerName = "food-analyzer-backend",
    
    [Parameter(Mandatory=$false)]
    [string]$DnsName = "food-analyzer-backend"
)

Write-Host "Deploying to Azure Container Instances" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan

# Step 1: Login to Azure
Write-Host ""
Write-Host "Step 1: Logging in to Azure..." -ForegroundColor Yellow
az login

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to login to Azure" -ForegroundColor Red
    exit 1
}

# Step 2: Create Resource Group
Write-Host ""
Write-Host "Step 2: Creating Resource Group '$ResourceGroup'..." -ForegroundColor Yellow
az group create --name $ResourceGroup --location $Location

# Step 3: Deploy Container Instance
Write-Host ""
Write-Host "Step 3: Deploying Container Instance..." -ForegroundColor Yellow
Write-Host "This may take 2-3 minutes..." -ForegroundColor Yellow

az container create `
    --resource-group $ResourceGroup `
    --name $ContainerName `
    --image sheryansh/food-analyzer-backend:latest `
    --dns-name-label $DnsName `
    --os-type Linux `
    --ports 8000 `
    --cpu 2 `
    --memory 4 `
    --environment-variables GEMINI_API_KEY=$GeminiApiKey FLASK_ENV=production PORT=8000 `
    --restart-policy OnFailure

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to deploy container" -ForegroundColor Red
    exit 1
}

# Step 4: Get the FQDN
Write-Host ""
Write-Host "Step 4: Retrieving container URL..." -ForegroundColor Yellow
$FQDN = az container show `
    --resource-group $ResourceGroup `
    --name $ContainerName `
    --query ipAddress.fqdn `
    --output tsv

$BackendUrl = "http://${FQDN}:8000"

Write-Host ""
Write-Host "=================================================" -ForegroundColor Green
Write-Host "SUCCESS! Backend deployed to Azure" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your backend is running at:" -ForegroundColor Cyan
Write-Host "  $BackendUrl" -ForegroundColor White
Write-Host ""
Write-Host "Test the health endpoint:" -ForegroundColor Yellow
Write-Host "  curl ${BackendUrl}/api/health" -ForegroundColor White
Write-Host ""
Write-Host "For frontend deployment, use this URL:" -ForegroundColor Yellow
Write-Host "  VITE_API_URL=$BackendUrl" -ForegroundColor White
Write-Host ""
Write-Host "View container logs:" -ForegroundColor Yellow
Write-Host "  az container logs --resource-group $ResourceGroup --name $ContainerName" -ForegroundColor White
Write-Host ""
Write-Host "=================================================" -ForegroundColor Green
