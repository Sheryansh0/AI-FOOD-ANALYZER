from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from food_analyzer import FoodAnalyzer
from health_assessor import HealthAssessor
import base64
from PIL import Image
import io

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize analyzers
food_analyzer = FoodAnalyzer(os.getenv('GEMINI_API_KEY'))
health_assessor = HealthAssessor()

# Create uploads directory
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Food Analysis API is running'}), 200

@app.route('/api/analyze', methods=['POST'])
def analyze_food():
    try:
        # Get form data
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        height = float(request.form.get('height', 0))
        weight = float(request.form.get('weight', 0))
        diseases = request.form.get('diseases', '').split(',')
        diseases = [d.strip() for d in diseases if d.strip()]
        
        if not image_file or image_file.filename == '':
            return jsonify({'error': 'Invalid image'}), 400
        
        # Read and process image
        image_bytes = image_file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Analyze food with Gemini
        print("Analyzing food image...")
        food_analysis = food_analyzer.analyze_food_image(image)
        
        if 'error' in food_analysis:
            return jsonify({'error': food_analysis['error']}), 500
        
        # Perform health assessment
        print("Performing health assessment...")
        health_assessment = health_assessor.assess_health(
            height=height,
            weight=weight,
            diseases=diseases,
            food_data=food_analysis
        )
        
        if 'error' in health_assessment:
            return jsonify({'error': health_assessment['error'], 'details': health_assessment.get('details', '')}), 500
        
        # Combine results
        result = {
            'foodAnalysis': food_analysis,
            'healthAssessment': health_assessment,
            'success': True
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
