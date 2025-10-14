# AI Food Analyzer - Futuristic Health Assessment

An advanced food analysis application powered by Google's Gemini AI that provides comprehensive nutritional analysis and personalized health assessments.

## Features

- 🍽️ **Food Recognition**: AI-powered food identification with confidence scores
- 📊 **Nutritional Analysis**: Complete breakdown of calories, macros, vitamins, and minerals
- 🏥 **Health Assessment**: Personalized recommendations based on height, weight, and health conditions
- 💯 **Quality Analysis**: Food freshness and quality scoring
- 🎯 **BMI Calculator**: Automatic BMI calculation and categorization
- ⚠️ **Health Warnings**: Smart alerts for dietary restrictions and health conditions
- 🎨 **Modern UI**: Futuristic React interface with smooth animations

## Tech Stack

### Backend

- Python 3.8+
- Flask (REST API)
- Google Generative AI (Gemini)
- PIL (Image processing)

### Frontend

- React 18
- Vite
- Tailwind CSS
- Framer Motion (animations)
- Axios

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Installation

### 1. Clone the repository or navigate to the project folder

```bash
cd "d:\chandramouli project"
```

### 2. Set up Python Backend

#### Create virtual environment

```powershell
python -m venv venv
```

#### Activate virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Install Python dependencies

```powershell
pip install -r requirements.txt
```

### 3. Set up React Frontend

```powershell
cd frontend
npm install
```

## Running the Application

### Terminal 1 - Start Backend Server

```powershell
# From project root
cd "d:\chandramouli project"
.\venv\Scripts\Activate.ps1
cd backend
python app.py
```

The backend will run on `http://localhost:5000`

### Terminal 2 - Start Frontend Development Server

```powershell
# From project root
cd "d:\chandramouli project\frontend"
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

1. **Open your browser** and navigate to `http://localhost:3000`

2. **Upload a food image** by clicking on the upload area or dragging an image

3. **Enter your personal information**:

   - Height (in centimeters)
   - Weight (in kilograms)
   - Health conditions (optional, comma-separated)

4. **Click "Analyze Food"** and wait for the AI to process

5. **Review the results**:
   - Food identification and confidence score
   - Calorie count and nutritional breakdown
   - Personalized health assessment
   - Food quality analysis
   - Recommendations based on your health profile

## Project Structure

```
chandramouli project/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── food_analyzer.py       # Gemini AI integration
│   └── health_assessor.py     # Health assessment logic
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── App.jsx           # Main app component
│   │   ├── main.jsx          # Entry point
│   │   └── index.css         # Global styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
└── README.md
```

## API Endpoints

### GET `/api/health`

Health check endpoint

### POST `/api/analyze`

Analyze food image with personal health data

**Request Body** (multipart/form-data):

- `image`: Food image file
- `height`: Height in cm
- `weight`: Weight in kg
- `diseases`: Comma-separated health conditions

**Response**:

```json
{
  "foodAnalysis": {
    "foodName": "string",
    "confidence": 0.95,
    "calories": 450,
    "ingredients": ["..."],
    "nutritionalBreakdown": {...},
    "foodQualityCycle": {...}
  },
  "healthAssessment": {
    "bmi": 23.5,
    "bmiCategory": "Normal weight",
    "suitability": {...},
    "recommendations": [...]
  }
}
```

## Features Explained

### Food Analysis

- Uses Gemini AI to identify food items
- Estimates calories and portion sizes
- Identifies ingredients
- Analyzes nutritional content
- Assesses food quality and freshness

### Health Assessment

- Calculates BMI and categorizes weight status
- Estimates daily calorie requirements
- Checks food suitability based on health conditions
- Provides personalized dietary recommendations
- Warns about potential health conflicts

### Supported Health Conditions

- Diabetes
- Hypertension
- Heart Disease
- Obesity
- Kidney Disease
- Celiac Disease
- Lactose Intolerance

## Customization

### Change API Key

Edit `.env` file and update the Gemini API key:

```
GEMINI_API_KEY=your_new_api_key_here
```

### Modify UI Colors

Edit `frontend/tailwind.config.js` to customize the color scheme:

```javascript
colors: {
  'neon-blue': '#00f3ff',
  'neon-purple': '#b537ff',
  'neon-pink': '#ff006e',
}
```

## Troubleshooting

### Backend Issues

- **Module not found**: Ensure venv is activated and dependencies are installed
- **API key error**: Check `.env` file has correct Gemini API key
- **Port in use**: Change port in `backend/app.py`

### Frontend Issues

- **npm install fails**: Delete `node_modules` and `package-lock.json`, then retry
- **Port 3000 in use**: Change port in `frontend/vite.config.js`
- **API connection error**: Ensure backend is running on port 5000

## Future Enhancements

- [ ] User authentication and history
- [ ] Meal planning suggestions
- [ ] Recipe recommendations
- [ ] Barcode scanning support
- [ ] Multiple language support
- [ ] Export results as PDF
- [ ] Integration with fitness trackers

## License

This project is for educational purposes.

## Credits

- Powered by Google Gemini AI
- UI Design inspired by modern futuristic interfaces
- Built with ❤️ using React and Flask
