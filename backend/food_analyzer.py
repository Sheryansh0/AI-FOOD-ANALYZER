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
        New Flow: 
        1. First get prediction from Gemini API
        2. Then predict with local models
        3. If local model prediction matches Gemini prediction, use model name
        4. Otherwise, use "Gemini API" as model name
        Returns: dict with food name, confidence, calories, ingredients, nutrition, quality
        """
        
        # Step 1: Get prediction from Gemini API first
        print("🔍 Step 1: Getting food identification from Gemini API...")
        gemini_food_name = self.get_food_name_from_gemini(image)
        print(f"✅ Gemini identified: {gemini_food_name}")
        
        model_to_use = "Gemini API"  # Default to Gemini
        
        # Step 2: Try local models if available
        if self.use_local_models and self.local_predictor and gemini_food_name:
            try:
                print("🔍 Step 2: Predicting with local models...")
                food_name, confidence, model_name, all_predictions = self.local_predictor.predict_ensemble(image)
                
                if food_name:
                    # Format both names for comparison (lowercase, replace underscores)
                    gemini_formatted = gemini_food_name.lower().replace(' ', '_').replace('-', '_')
                    local_formatted = food_name.lower().replace(' ', '_').replace('-', '_')
                    
                    print(f"📊 Local model prediction: {food_name} (confidence: {confidence:.2f}, model: {model_name})")
                    print(f"🔍 Comparing: Gemini='{gemini_formatted}' vs Local='{local_formatted}'")
                    
                    # Step 3: Check if predictions match
                    if gemini_formatted == local_formatted or gemini_formatted in local_formatted or local_formatted in gemini_formatted:
                        print(f"✅ MATCH! Using pretrained model: {model_name.upper()}")
                        model_to_use = model_name.upper()
                    else:
                        print(f"❌ NO MATCH! Gemini: '{gemini_food_name}' != Local: '{food_name}'")
                        print(f"✅ Using Gemini API as model name")
                        model_to_use = "Gemini API"
                else:
                    print("⚠️ Local model returned no prediction, using Gemini API")
                    
            except Exception as e:
                print(f"❌ Error with local models: {e}, using Gemini API")
        
        # Step 4: Get full detailed analysis from Gemini
        print(f"🔍 Step 3: Getting detailed analysis from Gemini (Model: {model_to_use})...")
        return self.get_detailed_analysis_from_gemini(image, gemini_food_name, model_to_use)
    
    def get_food_name_from_gemini(self, image):
        """Get just the food name from Gemini API"""
        try:
            prompt = """
            Identify the food item in this image. Return ONLY the name of the food/dish.
            Examples: "Pizza", "Chicken Curry", "Caesar Salad", "French Fries"
            
            Return just the food name, nothing else.
            """
            
            response = self.model.generate_content([prompt, image])
            food_name = response.text.strip()
            
            # Clean up the response
            food_name = food_name.replace('"', '').replace("'", "").strip()
            
            return food_name
            
        except Exception as e:
            print(f"❌ Error getting food name from Gemini: {e}")
            return None
    
    def get_detailed_analysis_from_gemini(self, image, food_name, model_used):
        """Get detailed nutritional analysis from Gemini with specified model name"""
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
                "confidence": 0.95,
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
            # Fallback to basic Gemini analysis
            return self.analyze_with_gemini(image, "Gemini API", None)
    
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
