# Docker Deployment Guide for AI Food Analyzer

This guide will help you run the AI Food Analyzer using Docker and Docker Compose.

## Prerequisites

- Docker Desktop installed (https://www.docker.com/products/docker-desktop/)
- Docker Compose (included with Docker Desktop)
- Gemini API Key (https://makersuite.google.com/app/apikey)
- Model files (.pth) in the `models/` folder

## Quick Start

### 1. Setup Environment Variables

Copy the example environment file and add your API key:

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your Gemini API key
# GEMINI_API_KEY=your_actual_api_key_here
```

### 2. Build and Run with Docker Compose

```bash
# Build and start all services (backend + frontend)
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

### 3. Stop the Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Docker Commands

### Backend Only

```bash
# Build backend image
docker build -t ai-food-analyzer-backend ./backend

# Run backend container
docker run -d \
  --name ai-food-backend \
  -p 5000:5000 \
  -e GEMINI_API_KEY=your_api_key \
  -v $(pwd)/models:/app/models:ro \
  -v $(pwd)/backend/uploads:/app/uploads \
  ai-food-analyzer-backend
```

### Frontend Only

```bash
# Build frontend image
docker build -t ai-food-analyzer-frontend ./frontend

# Run frontend container
docker run -d \
  --name ai-food-frontend \
  -p 3000:3000 \
  ai-food-analyzer-frontend
```

## Important Notes

### Model Files

The model files (`.pth` files in `models/` folder) are **NOT** included in the Docker image due to their large size. Instead, they are mounted as a volume:

```yaml
volumes:
  - ./models:/app/models:ro  # Read-only mount
```

**Make sure your model files are present in the `models/` folder before running Docker!**

### Uploads Folder

User uploads are persisted using a volume mount:

```yaml
volumes:
  - ./backend/uploads:/app/uploads
```

This ensures uploaded images are not lost when containers restart.

## Troubleshooting

### Issue: Models not loading

**Solution**: Ensure the `models/` folder contains the `.pth` files:
- `best_model_ConvNeXt-B.pth`
- `best_model_EfficientNetV2-M.pth`
- `best_model_ViT-B-16.pth`

### Issue: API key not working

**Solution**: Check that your `.env` file exists and contains the correct API key without quotes:
```
GEMINI_API_KEY=AIzaSy...
```

### Issue: Port already in use

**Solution**: Stop any running instances:
```bash
# Stop local development servers
# Then stop Docker containers
docker-compose down
```

Or change the port mappings in `docker-compose.yml`:
```yaml
ports:
  - "5001:5000"  # Changed from 5000 to 5001
```

### View Logs

```bash
# View all logs
docker-compose logs

# View backend logs only
docker-compose logs backend

# Follow logs in real-time
docker-compose logs -f backend
```

### Rebuild After Code Changes

```bash
# Rebuild specific service
docker-compose build backend

# Rebuild and restart
docker-compose up -d --build
```

## Production Deployment

For production deployment, consider:

1. **Use environment-specific .env files**
   ```bash
   docker-compose --env-file .env.production up -d
   ```

2. **Enable HTTPS with reverse proxy** (nginx/traefik)

3. **Use Docker secrets for sensitive data**

4. **Set resource limits**
   ```yaml
   services:
     backend:
       deploy:
         resources:
           limits:
             cpus: '2'
             memory: 4G
   ```

5. **Enable restart policies**
   ```yaml
   restart: always
   ```

## Development Mode

To run in development mode with hot reload:

```bash
# Use local development instead of Docker for better hot-reload
cd backend
python app.py

# In another terminal
cd frontend
npm run dev
```

## Docker Hub (Optional)

To push images to Docker Hub:

```bash
# Tag images
docker tag ai-food-analyzer-backend username/ai-food-analyzer-backend:latest
docker tag ai-food-analyzer-frontend username/ai-food-analyzer-frontend:latest

# Push to Docker Hub
docker push username/ai-food-analyzer-backend:latest
docker push username/ai-food-analyzer-frontend:latest
```

## Useful Commands

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# View container resource usage
docker stats

# Execute command in running container
docker exec -it ai-food-analyzer-backend bash

# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune -a
```

## Support

For issues and questions, please refer to the main README.md or open an issue on GitHub.
