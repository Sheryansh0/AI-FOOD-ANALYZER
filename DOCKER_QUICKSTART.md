# 🐳 Docker Quick Start

Run the entire AI Food Analyzer application with one command!

## Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- Model files in `models/` folder

## Setup in 3 Steps

### 1️⃣ Create `.env` file
```bash
cp .env.example .env
```
Then edit `.env` and add your API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### 2️⃣ Ensure Model Files Exist
Make sure these files are in the `models/` folder:
- `best_model_ConvNeXt-B.pth`
- `best_model_EfficientNetV2-M.pth`
- `best_model_ViT-B-16.pth`

### 3️⃣ Run with Docker Compose
```bash
docker-compose up --build
```

That's it! 🎉

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000

## Stop the Application
```bash
docker-compose down
```

## View Logs
```bash
# All services
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only
docker-compose logs -f frontend
```

## Troubleshooting

### Port Already in Use?
```bash
# Stop local development servers first
# Kill processes on port 5000 and 3000
# Then run docker-compose again
```

### Models Not Loading?
Check that `.pth` files exist in `models/` folder:
```bash
ls -la models/
```

### Need to Rebuild?
```bash
docker-compose down
docker-compose up --build
```

## For Detailed Documentation
See [DOCKER_GUIDE.md](DOCKER_GUIDE.md) for complete Docker documentation.
