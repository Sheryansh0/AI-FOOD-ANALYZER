import google.generativeai as genai
from PIL import Image
import json
import re
from model_predictor import LocalModelPredictor

class FoodAnalyzer:
    def __init__(self, api_key, use_local_models=True, confidence_threshold=0.7):
        genai.configure(api_key=api_key)
        # Use Gemini 2.5 Flash - stable and supports vision
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Initialize local model predictor
        self.use_local_models = use_local_models
        self.confidence_threshold = confidence_threshold
        
        if use_local_models:
            try:
                self.local_predictor = LocalModelPredictor(confidence_threshold=confidence_threshold)
                print("Local models initialized successfully")
                print(f"Food-101 dataset has {len(self.local_predictor.class_names)} classes")
            except Exception as e:
                print(f"Failed to initialize local models: {e}")
                self.use_local_models = False
                self.local_predictor = None
        else:
            self.local_predictor = None
    
    def analyze_food_image(self, image):
        """
        Analyze food image using local models first, then Gemini API if needed
        Returns: dict with food name, confidence, calories, ingredients, nutrition, quality
        """
        local_prediction_info = None
        use_local_model = False
        
        # Try local models first
        if self.use_local_models and self.local_predictor:
            try:
                print("Attempting prediction with local models...")
                food_name, confidence, model_name, all_predictions = self.local_predictor.predict_ensemble(image)
                
                # Validate prediction is within Food-101 dataset and has high confidence
                if food_name:
                    # Check if the predicted food is in the Food-101 dataset
                    if food_name not in self.local_predictor.class_names:
                        print(f"⚠️ Predicted food '{food_name}' NOT in Food-101 dataset, using Gemini API")
                    elif self.local_predictor.should_use_gemini(confidence):
                        print(f"⚠️ Local model confidence too low ({confidence:.2f}), using Gemini API")
                        local_prediction_info = {
                            'attempted': True,
                            'best_prediction': food_name,
                            'confidence': confidence,
                            'all_predictions': all_predictions
                        }
                    elif confidence < 0.85:
                        # Extra validation for medium confidence (70-85%)
                        print(f"⚠️ Medium confidence ({confidence:.2f}) - verifying with Gemini...")
                        formatted_food_name = self.local_predictor.format_food_name(food_name)
                        
                        # Quick verification with Gemini
                        if self.quick_verify_prediction(image, formatted_food_name):
                            print(f"✅ Verified: {formatted_food_name}")
                            model_used = f"{model_name.upper()} (Verified by Gemini)"
                            return self.get_detailed_analysis_for_food(image, formatted_food_name, confidence, model_used)
                        else:
                            print(f"❌ Verification failed, using full Gemini analysis")
                    else:
                        # High confidence (>= 85%) and in dataset - trust it
                        print(f"✅ Local model prediction: {food_name} (confidence: {confidence:.2f}, model: {model_name})")
                        formatted_food_name = self.local_predictor.format_food_name(food_name)
                        model_used = model_name.upper()
                        return self.get_detailed_analysis_for_food(image, formatted_food_name, confidence, model_used)
                    
            except Exception as e:
                print(f"❌ Error with local models: {e}, falling back to Gemini API")
        
        # Use Gemini API for full analysis
        print("🔍 Using Gemini API for food analysis...")
        return self.analyze_with_gemini(image, "Gemini API", local_prediction_info)
    
    def quick_verify_prediction(self, image, predicted_food):
        """Quick verification of prediction with Gemini (for medium confidence cases)"""
        try:
            prompt = f"""
            Is this image showing {predicted_food}? Answer with just 'YES' or 'NO'.
            """
            
            response = self.model.generate_content([prompt, image])
            answer = response.text.strip().upper()
            
            return 'YES' in answer or 'TRUE' in answer
            
        except Exception as e:
            print(f"⚠️ Verification error: {e}")
            return False  # If verification fails, use Gemini for full analysis
    
    def get_detailed_analysis_for_food(self, image, food_name, confidence, model_used):
        """Get detailed nutritional analysis from Gemini for a known food item"""
        try:
            prompt = f"""
            This is an image of {food_name}. Provide a comprehensive and ACCURATE nutritional analysis.
            
            IMPORTANT INSTRUCTIONS FOR HEALTH SCORE:
            - If this is JUNK FOOD (fried, fast food, processed, high in unhealthy fats/sugar/sodium), healthScore MUST be LOW (1-4)
            - If this is HEALTHY FOOD (grilled, steamed, fresh vegetables, fruits, lean protein), healthScore should be HIGH (7-10)
            - If this is MODERATELY HEALTHY (some good nutrients but also some concerns), healthScore should be MEDIUM (5-6)
            
            Examples:
            - French fries, burgers, pizza, fried chicken, donuts: healthScore 1-3
            - Fresh salad, grilled chicken, steamed vegetables, fruits: healthScore 8-10
            - Rice with curry, pasta, sandwiches: healthScore 5-7
            
            Return in this JSON format:
            {{
                "foodName": "{food_name}",
                "confidence": {confidence},
                "calories": (realistic calorie estimate),
                "ingredients": ["main ingredients visible or typical for this dish"],
                "nutritionalBreakdown": {{
                    "protein": "Xg",
                    "carbohydrates": "Xg",
                    "fats": "Xg",
                    "saturatedFat": "Xg",
                    "fiber": "Xg",
                    "sugar": "Xg",
                    "sodium": "Xmg",
                    "vitamins": ["list vitamins"],
                    "minerals": ["list minerals"]
                }},
                "foodQualityCycle": {{
                    "freshness": "High/Medium/Low based on image",
                    "preparation": "How is it cooked/prepared",
                    "healthScore": (1-10, BE STRICT with junk food),
                    "qualityIndicators": ["what makes it healthy or unhealthy"]
                }},
                "portionSize": "approximate serving size",
                "mealType": "Breakfast/Lunch/Dinner/Snack"
            }}
            
            BE REALISTIC and STRICT with healthScore for unhealthy foods!
            Return ONLY valid JSON without markdown formatting.
            """
            
            response = self.model.generate_content([prompt, image])
            response_text = response.text.strip()
            
            # Clean response
            response_text = re.sub(r'```json\s*', '', response_text)
            response_text = re.sub(r'```\s*', '', response_text)
            response_text = response_text.strip()
            
            analysis = json.loads(response_text)
            # Ensure model name is set correctly
            analysis['modelUsed'] = model_used
            print(f"✅ Detailed analysis complete. Food: {food_name}, Model: {model_used}")
            
            return analysis
            
        except Exception as e:
            print(f"❌ Error in detailed analysis: {e}")
            return self.analyze_with_gemini(image, "Gemini API (fallback)", None)
    
    def analyze_with_gemini(self, image, model_used="Gemini API", local_info=None):
        """Full analysis using Gemini API"""
        try:
            # Create comprehensive prompt for Gemini
            prompt = """
            Analyze this food image and provide a comprehensive, ACCURATE nutritional analysis.
            
            CRITICAL INSTRUCTIONS FOR HEALTH SCORE:
            - Junk/Fast Food (fried, processed, high fat/sugar/sodium) → healthScore: 1-4
            - Moderately Healthy (some concerns but decent nutrition) → healthScore: 5-6  
            - Healthy Food (fresh, grilled, steamed, nutritious) → healthScore: 7-10
            
            BE STRICT and REALISTIC with healthScore!
            
            Examples:
            - Pizza, burgers, fried chicken, donuts, fries → 1-3
            - Pasta, curry with rice, sandwiches → 5-6
            - Salads, grilled fish, steamed vegetables, fresh fruits → 8-10
            
            Return in JSON format:
            {
                "foodName": "Exact name of the dish",
                "confidence": 0.95,
                "calories": (realistic estimate for visible portion),
                "ingredients": ["list all visible or typical ingredients"],
                "nutritionalBreakdown": {
                    "protein": "Xg",
                    "carbohydrates": "Xg",
                    "fats": "Xg",
                    "saturatedFat": "Xg",
                    "fiber": "Xg",
                    "sugar": "Xg",
                    "sodium": "Xmg",
                    "vitamins": ["Vitamin A", "Vitamin C", etc],
                    "minerals": ["Iron", "Calcium", etc]
                },
                "foodQualityCycle": {
                    "freshness": "High/Medium/Low (based on appearance)",
                    "preparation": "How it's cooked (fried/grilled/steamed/baked/raw)",
                    "healthScore": (1-10, BE STRICT for unhealthy foods!),
                    "qualityIndicators": ["Reasons for the health score - be specific about what makes it healthy or unhealthy"]
                },
                "portionSize": "Approximate serving size with weight",
                "mealType": "Breakfast/Lunch/Dinner/Snack"
            }
            
            Return ONLY valid JSON. No markdown, no code blocks.
            """
            
            # Generate content with image
            response = self.model.generate_content([prompt, image])
            
            # Extract and parse JSON response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            response_text = re.sub(r'```json\s*', '', response_text)
            response_text = re.sub(r'```\s*', '', response_text)
            response_text = response_text.strip()
            
            # Parse JSON
            analysis = json.loads(response_text)
            
            # Validate and ensure all required fields are present
            required_fields = ['foodName', 'confidence', 'calories', 'ingredients', 
                             'nutritionalBreakdown', 'foodQualityCycle']
            
            for field in required_fields:
                if field not in analysis:
                    raise ValueError(f"Missing required field: {field}")
            
            # Set the model used - ensure it's always "Gemini API" for this method
            analysis['modelUsed'] = model_used
            print(f"✅ Analysis complete. Food: {analysis.get('foodName', 'Unknown')}, Model: {model_used}")
            
            return analysis
            
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {e}")
            print(f"Response text: {response_text}")
            return {
                'error': 'Failed to parse AI response',
                'details': str(e)
            }
        except Exception as e:
            print(f"Error in food analysis: {e}")
            return {
                'error': 'Failed to analyze food image',
                'details': str(e)
            }
    
    def get_food_recommendations(self, food_data, health_conditions):
        """
        Get personalized recommendations based on food and health conditions
        """
        try:
            prompt = f"""
            Based on this food analysis: {json.dumps(food_data)}
            And these health conditions: {', '.join(health_conditions) if health_conditions else 'None'}
            
            Provide 3-5 specific recommendations for this person regarding this food.
            Return as a JSON array of strings.
            Example: ["recommendation1", "recommendation2", "recommendation3"]
            Return ONLY valid JSON without any markdown formatting.
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            response_text = re.sub(r'```json\s*', '', response_text)
            response_text = re.sub(r'```\s*', '', response_text)
            
            recommendations = json.loads(response_text)
            return recommendations
            
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return ["Consult with a healthcare professional for personalized advice"]
