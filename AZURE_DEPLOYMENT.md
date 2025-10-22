# Azure Deployment Guide for Backend

This guide will help you deploy the AI Food Analyzer backend to Azure Container Apps or Azure Web App.

## Prerequisites

- Azure CLI installed
- Docker installed
- Azure subscription
- Gemini API key from Google

## Option 1: Deploy to Azure Container Apps (Recommended)

### Step 1: Login to Azure

```bash
az login
```

### Step 2: Create Resource Group

```bash
az group create --name food-analyzer-rg --location eastus
```

### Step 3: Create Azure Container Registry

```bash
az acr create --resource-group food-analyzer-rg --name foodanalyzeracr --sku Basic
az acr login --name foodanalyzeracr
```

### Step 4: Build and Push Docker Image

```bash
cd backend
docker build -t foodanalyzeracr.azurecr.io/food-analyzer-backend:latest .
docker push foodanalyzeracr.azurecr.io/food-analyzer-backend:latest
```

### Step 5: Create Container App Environment

```bash
az containerapp env create --name food-analyzer-env --resource-group food-analyzer-rg --location eastus
```

### Step 6: Deploy Container App

```bash
az containerapp create \
  --name food-analyzer-backend \
  --resource-group food-analyzer-rg \
  --environment food-analyzer-env \
  --image foodanalyzeracr.azurecr.io/food-analyzer-backend:latest \
  --target-port 8000 \
  --ingress external \
  --registry-server foodanalyzeracr.azurecr.io \
  --env-vars GEMINI_API_KEY="your-gemini-api-key" FLASK_ENV=production \
  --cpu 2 --memory 4Gi
```

### Step 7: Get the Backend URL

```bash
az containerapp show --name food-analyzer-backend --resource-group food-analyzer-rg --query properties.configuration.ingress.fqdn -o tsv
```

Save this URL - you'll need it for your frontend Vercel deployment.

---

## Option 2: Deploy to Azure Web App

### Step 1: Create App Service Plan

```bash
az appservice plan create --name food-analyzer-plan --resource-group food-analyzer-rg --is-linux --sku B2
```

### Step 2: Create Web App

```bash
az webapp create --resource-group food-analyzer-rg --plan food-analyzer-plan --name food-analyzer-backend --deployment-container-image-name foodanalyzeracr.azurecr.io/food-analyzer-backend:latest
```

### Step 3: Configure Environment Variables

```bash
az webapp config appsettings set --resource-group food-analyzer-rg --name food-analyzer-backend --settings GEMINI_API_KEY="your-gemini-api-key" FLASK_ENV=production
```

### Step 4: Enable CORS

```bash
az webapp cors add --resource-group food-analyzer-rg --name food-analyzer-backend --allowed-origins "*"
```

---

## Local Docker Testing

Before deploying to Azure, test locally:

```bash
# Build the image
cd backend
docker build -t food-analyzer-backend .

# Run the container
docker run -p 8000:8000 -e GEMINI_API_KEY="your-key" food-analyzer-backend

# Test the API
curl http://localhost:8000/api/health
```

---

## PowerShell Commands (Windows)

If using PowerShell, use these commands instead:

### Build and Test Locally

```powershell
cd backend
docker build -t food-analyzer-backend .
docker run -p 8000:8000 -e GEMINI_API_KEY="your-key" food-analyzer-backend
```

### Push to Azure Container Registry

```powershell
az acr login --name foodanalyzeracr
docker tag food-analyzer-backend foodanalyzeracr.azurecr.io/food-analyzer-backend:latest
docker push foodanalyzeracr.azurecr.io/food-analyzer-backend:latest
```

---

## Important Notes

1. **Model Files**: The Docker image includes the PyTorch model files (~500MB each). Ensure your container has at least 4GB memory.

2. **API Key**: Never commit your GEMINI_API_KEY to Git. Use Azure's environment variables or Key Vault.

3. **CORS**: The backend already has CORS enabled in `app.py` for all origins. For production, restrict to your Vercel domain.

4. **Scaling**: For Container Apps, you can enable autoscaling:

   ```bash
   az containerapp update --name food-analyzer-backend --resource-group food-analyzer-rg --min-replicas 1 --max-replicas 3
   ```

5. **Monitoring**: Enable Application Insights for monitoring:
   ```bash
   az monitor app-insights component create --app food-analyzer-insights --location eastus --resource-group food-analyzer-rg
   ```

---

## Cost Optimization

- Use **Azure Container Apps** for automatic scaling and pay-per-use
- Use **Azure Web App Free/Basic tier** for development/testing
- Consider **Azure Functions** for sporadic usage
- Store model files in **Azure Blob Storage** and download on startup to reduce image size

---

## Next Steps

After deploying the backend:

1. Save your backend URL (e.g., `https://food-analyzer-backend.azurecontainerapps.io`)
2. Update your frontend to use this URL instead of localhost
3. Deploy frontend to Vercel
4. Test the complete application

---

## Troubleshooting

### Container fails to start

- Check memory allocation (needs at least 4GB for models)
- Verify GEMINI_API_KEY is set correctly
- Check logs: `az containerapp logs show --name food-analyzer-backend --resource-group food-analyzer-rg`

### 502 Bad Gateway

- Container might be taking too long to start (model loading)
- Increase timeout or use health check delay
- Check if port 8000 is properly exposed

### Out of Memory

- Models are large. Increase memory to 4-8GB
- Consider lazy loading models only when needed
