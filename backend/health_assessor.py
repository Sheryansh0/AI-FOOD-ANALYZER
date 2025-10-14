import math

class HealthAssessor:
    def __init__(self):
        self.disease_restrictions = {
            'diabetes': ['high sugar', 'refined carbs', 'sweet'],
            'hypertension': ['high sodium', 'salt', 'salty'],
            'heart disease': ['high fat', 'saturated fat', 'cholesterol'],
            'obesity': ['high calorie', 'fried', 'fatty'],
            'kidney disease': ['high sodium', 'high protein', 'potassium'],
            'celiac disease': ['gluten', 'wheat', 'barley', 'rye'],
            'lactose intolerance': ['milk', 'dairy', 'lactose', 'cheese'],
        }
        
        # Unhealthy food keywords for better detection
        self.unhealthy_keywords = [
            'fried', 'deep fried', 'crispy', 'burger', 'fries', 'pizza', 
            'donut', 'cake', 'pastry', 'ice cream', 'candy', 'chips', 'soda',
            'fast food', 'junk', 'processed', 'nugget', 'hot dog', 'bacon',
            'milkshake', 'cookie', 'brownie', 'nachos', 'taco bell', 'mcdonald',
            'kfc', 'wings', 'cheesy', 'creamy sauce', 'mayo', 'breaded'
        ]
        
        # Healthy food keywords
        self.healthy_keywords = [
            'salad', 'vegetable', 'fruit', 'grilled', 'steamed', 'baked',
            'whole grain', 'lean', 'fresh', 'green', 'organic', 'smoothie',
            'quinoa', 'brown rice', 'oatmeal', 'yogurt', 'nuts', 'seeds',
            'fish', 'chicken breast', 'tofu', 'lentils', 'beans'
        ]
    
    def calculate_bmi(self, height_cm, weight_kg):
        """Calculate BMI and category"""
        if height_cm <= 0 or weight_kg <= 0:
            return None, "Unknown"
        
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 25:
            category = "Normal weight"
        elif 25 <= bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
        
        return round(bmi, 2), category
    
    def calculate_bmr(self, height_cm, weight_kg, age=30, gender='male'):
        """Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation"""
        if height_cm <= 0 or weight_kg <= 0:
            return None
        
        if gender.lower() == 'male':
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
        
        return round(bmr, 2)
    
    def assess_food_suitability(self, diseases, food_data, bmi_category):
        """Assess if food is suitable based on health conditions and BMI"""
        warnings = []
        score = 10
        penalty_applied = False
        
        food_name = food_data.get('foodName', '').lower()
        ingredients = [ing.lower() for ing in food_data.get('ingredients', [])]
        nutrition = food_data.get('nutritionalBreakdown', {})
        calories = food_data.get('calories', 0)
        
        # Check if food is unhealthy/junk food
        is_unhealthy = any(keyword in food_name or any(keyword in ing for ing in ingredients) 
                          for keyword in self.unhealthy_keywords)
        is_healthy = any(keyword in food_name or any(keyword in ing for ing in ingredients) 
                        for keyword in self.healthy_keywords)
        
        # Base score adjustment for food type (more moderate)
        if is_unhealthy and not is_healthy:
            score -= 2  # Reduced from 3
            warnings.append("⚠️ This appears to be processed/junk food")
            penalty_applied = True
        
        # BMI-based assessment for obesity/overweight
        if bmi_category in ['Overweight', 'Obese']:
            if is_unhealthy and not penalty_applied:
                score -= 2  # Reduced from 3
                warnings.append(f"❌ Not recommended for {bmi_category} individuals - high in unhealthy fats/calories")
            elif is_unhealthy:
                warnings.append(f"❌ Not recommended for {bmi_category} individuals - high in unhealthy fats/calories")
            
            if calories > 700:  # Increased threshold from 600
                score -= 1.5  # Reduced from 2
                warnings.append(f"⚠️ High calorie content ({calories} cal) - May hinder weight management")
            
            # Check for fried foods
            if any(word in food_name for word in ['fried', 'deep fried', 'crispy', 'breaded']):
                if not penalty_applied:
                    score -= 1.5  # Reduced from 2
                warnings.append("❌ Fried foods are not recommended for weight management")
        
        # Extract nutritional values safely
        def extract_number(value_str):
            if isinstance(value_str, (int, float)):
                return float(value_str)
            return float(''.join(filter(str.isdigit, str(value_str)))) if value_str else 0
        
        sodium_value = extract_number(nutrition.get('sodium', '0mg'))
        sugar_value = extract_number(nutrition.get('sugar', '0g'))
        fat_value = extract_number(nutrition.get('fats', '0g'))
        saturated_fat = extract_number(nutrition.get('saturatedFat', '0g'))
        
        # Disease-specific checks
        for disease in (diseases or []):
            disease_lower = disease.lower()
            
            if disease_lower in self.disease_restrictions:
                restrictions = self.disease_restrictions[disease_lower]
                
                # Check disease-specific restrictions
                if 'diabetes' in disease_lower or 'diabetic' in disease_lower:
                    if sugar_value > 20:  # Increased threshold from 15
                        score -= 2.5  # Reduced from 3
                        warnings.append(f"❌ High sugar content ({sugar_value}g) - Dangerous for diabetes")
                    elif sugar_value > 15:
                        score -= 1
                        warnings.append(f"⚠️ Moderate sugar content ({sugar_value}g) - Monitor intake")
                    if is_unhealthy and not penalty_applied:
                        score -= 1.5  # Reduced from 2
                        warnings.append("❌ Processed foods can spike blood sugar levels")
                
                if 'hypertension' in disease_lower or 'blood pressure' in disease_lower:
                    if sodium_value > 800:  # Increased threshold from 600
                        score -= 2.5  # Reduced from 3
                        warnings.append(f"❌ Very high sodium ({sodium_value}mg) - Dangerous for hypertension")
                    elif sodium_value > 500:  # Increased from 400
                        score -= 1.5  # Reduced from 2
                        warnings.append(f"⚠️ High sodium ({sodium_value}mg) - Monitor intake")
                
                if 'heart' in disease_lower or 'cardiac' in disease_lower:
                    if fat_value > 25 or saturated_fat > 12:  # Increased thresholds
                        score -= 2.5  # Reduced from 3
                        warnings.append(f"❌ High fat content - Not suitable for heart conditions")
                    elif fat_value > 20 or saturated_fat > 10:
                        score -= 1
                        warnings.append(f"⚠️ Moderate fat content - Monitor intake")
                    if is_unhealthy and not penalty_applied:
                        score -= 1.5  # Reduced from 2
                        warnings.append("❌ Processed foods increase cardiovascular risk")
                
                if 'obesity' in disease_lower:
                    if is_unhealthy and not penalty_applied:
                        score -= 2.5  # Reduced from 4
                        warnings.append("❌ STRONGLY NOT RECOMMENDED - Junk food will worsen obesity")
                    elif is_unhealthy:
                        warnings.append("❌ STRONGLY NOT RECOMMENDED - Junk food will worsen obesity")
                    if calories > 600:  # Increased threshold from 500
                        score -= 1.5  # Reduced from 2
                        warnings.append(f"❌ High calorie meal ({calories} cal) - Choose lower calorie options")
        
        # Additional nutritional warnings (only if not already penalized)
        if sodium_value > 1000 and not any('sodium' in w.lower() for w in warnings):
            score -= 1.5  # Reduced from 2
            warnings.append(f"⚠️ Extremely high sodium ({sodium_value}mg) - Daily limit is 2300mg")
        
        if sugar_value > 30 and not any('sugar' in w.lower() for w in warnings):  # Increased threshold from 25
            score -= 1.5  # Reduced from 2
            warnings.append(f"⚠️ Very high sugar content ({sugar_value}g) - Limit sugar intake")
        
        if fat_value > 35 and not any('fat' in w.lower() for w in warnings):  # Increased threshold from 30
            score -= 0.5  # Reduced from 1
            warnings.append(f"⚠️ High fat content ({fat_value}g)")
        
        score = max(0, min(10, score))
        suitable = score >= 5
        
        return {
            'suitable': suitable,
            'warnings': warnings,
            'suitabilityScore': score,
            'isJunkFood': is_unhealthy and not is_healthy
        }
    
    def calculate_calorie_needs(self, height_cm, weight_kg, activity_level='moderate'):
        """Calculate daily calorie needs"""
        bmr = self.calculate_bmr(height_cm, weight_kg)
        if not bmr:
            return None
        
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        multiplier = activity_multipliers.get(activity_level, 1.55)
        daily_calories = bmr * multiplier
        
        return round(daily_calories, 0)
    
    def assess_health(self, height, weight, diseases, food_data):
        """
        Perform comprehensive health assessment
        """
        try:
            # Calculate BMI
            bmi, bmi_category = self.calculate_bmi(height, weight)
            
            # Calculate daily calorie needs
            daily_calories = self.calculate_calorie_needs(height, weight)
            
            # Get food calories
            food_calories = food_data.get('calories', 0)
            
            # Assess food suitability with BMI consideration
            suitability = self.assess_food_suitability(diseases, food_data, bmi_category)
            
            # Calculate percentage of daily calories
            calorie_percentage = round((food_calories / daily_calories * 100), 1) if daily_calories else 0
            
            # Calculate dynamic food quality score
            food_quality_score = self._calculate_food_quality(food_data, bmi_category, diseases)
            
            # Update food quality in data
            if 'foodQualityCycle' not in food_data:
                food_data['foodQualityCycle'] = {}
            food_data['foodQualityCycle']['healthScore'] = food_quality_score
            
            # Generate personalized recommendations
            recommendations = self._generate_recommendations(
                bmi_category, diseases, suitability, food_data, calorie_percentage
            )
            
            # Overall health score (0-10) - more strict for unhealthy foods
            health_score = self._calculate_health_score(
                bmi_category, suitability['suitabilityScore'], 
                food_quality_score, suitability.get('isJunkFood', False)
            )
            
            return {
                'bmi': bmi,
                'bmiCategory': bmi_category,
                'dailyCalorieNeeds': daily_calories,
                'foodCalories': food_calories,
                'caloriePercentage': calorie_percentage,
                'suitability': suitability,
                'recommendations': recommendations,
                'overallHealthScore': health_score,
                'healthConditions': diseases if diseases else ['None reported']
            }
            
        except Exception as e:
            print(f"Error in health assessment: {e}")
            return {
                'error': 'Failed to perform health assessment',
                'details': str(e)
            }
    
    def _calculate_food_quality(self, food_data, bmi_category, diseases):
        """Calculate food quality score based on nutritional content and user profile"""
        score = 5.0  # Start neutral
        
        food_name = food_data.get('foodName', '').lower()
        nutrition = food_data.get('nutritionalBreakdown', {})
        calories = food_data.get('calories', 0)
        
        # Extract nutritional values
        def extract_number(value_str):
            if isinstance(value_str, (int, float)):
                return float(value_str)
            return float(''.join(filter(str.isdigit, str(value_str)))) if value_str else 0
        
        protein = extract_number(nutrition.get('protein', '0g'))
        fiber = extract_number(nutrition.get('fiber', '0g'))
        sugar = extract_number(nutrition.get('sugar', '0g'))
        sodium = extract_number(nutrition.get('sodium', '0mg'))
        fat = extract_number(nutrition.get('fats', '0g'))
        
        # Check for unhealthy/junk food
        is_junk = any(keyword in food_name for keyword in self.unhealthy_keywords)
        is_healthy = any(keyword in food_name for keyword in self.healthy_keywords)
        
        if is_junk:
            score -= 2  # Reduced from 3
        elif is_healthy:
            score += 2.5  # Increased bonus for healthy foods
        
        # Nutritional quality assessment with better balance
        if protein > 25:
            score += 1.5  # Better bonus for high protein
        elif protein > 15:
            score += 0.5
        
        if fiber > 8:
            score += 1.5  # Better bonus for high fiber
        elif fiber > 5:
            score += 0.5
        
        if sugar < 8:
            score += 1.5  # Better bonus for low sugar
        elif sugar < 15:
            score += 0.5
        elif sugar > 30:  # Increased threshold from 25
            score -= 1.5  # Reduced penalty from 2
        
        if sodium < 300:
            score += 1.5  # Better bonus for low sodium
        elif sodium < 500:
            score += 0.5
        elif sodium > 1000:  # Increased threshold from 800
            score -= 1.5  # Reduced penalty from 2
        
        if fat < 12:
            score += 1  # Better bonus for low fat
        elif fat > 35:  # Increased threshold from 30
            score -= 1  # Reduced penalty from 1.5
        
        # Additional penalty for high-calorie foods for overweight/obese users (more moderate)
        if bmi_category in ['Overweight', 'Obese']:
            if calories > 700:  # Increased threshold from 600
                score -= 1  # Reduced from 1.5
            if is_junk:
                score -= 0.5  # Reduced extra penalty from 1
        
        # Clamp score between 0 and 10
        return max(0.0, min(10.0, round(score, 1)))
    
    def _calculate_health_score(self, bmi_category, suitability_score, food_quality_score, is_junk_food):
        """Calculate overall health score with balanced but strict evaluation"""
        bmi_score = {
            'Normal weight': 10,
            'Underweight': 7,  # Increased from 6
            'Overweight': 6,   # Increased from 5
            'Obese': 4         # Increased from 3
        }.get(bmi_category, 5)
        
        # If person is obese/overweight and eating junk food, penalize but not too harshly
        if (bmi_category in ['Overweight', 'Obese']) and is_junk_food:
            overall = min(4.0, (suitability_score * 0.5 + food_quality_score * 0.5))  # Increased cap from 3.0 to 4.0
        else:
            # Weighted average - balanced weights
            overall = (bmi_score * 0.25 + suitability_score * 0.45 + food_quality_score * 0.30)
        
        return round(max(0.0, min(10.0, overall)), 1)
    
    def _generate_recommendations(self, bmi_category, diseases, suitability, food_data, calorie_percentage):
        """Generate personalized health recommendations"""
        recommendations = []
        is_junk = suitability.get('isJunkFood', False)
        food_name = food_data.get('foodName', '')
        calories = food_data.get('calories', 0)
        
        # Strong warnings for junk food + obesity/overweight
        if (bmi_category in ['Overweight', 'Obese']) and is_junk:
            recommendations.append(f"🚫 AVOID THIS FOOD: {food_name} is junk food and will worsen your weight condition")
            recommendations.append("💡 Choose grilled, steamed, or baked options with vegetables instead")
            recommendations.append("🏃 Increase physical activity to burn excess calories")
        
        # BMI-based recommendations
        if bmi_category == 'Underweight':
            recommendations.append("✅ Increase caloric intake with nutrient-dense foods like nuts, avocados, and lean proteins")
            if not is_junk:
                recommendations.append(f"✅ This food can be part of your weight gain diet")
        
        elif bmi_category == 'Overweight':
            if not is_junk and calories < 500:
                recommendations.append("✅ Good choice! Focus on similar low-calorie, nutritious meals")
            recommendations.append("🎯 Target: Reduce 500 calories per day for healthy weight loss")
            if calorie_percentage > 35:
                recommendations.append("⚠️ This meal is a large portion of your daily calories - reduce serving size")
        
        elif bmi_category == 'Obese':
            if is_junk:
                recommendations.append("🚨 CRITICAL: This food will significantly hinder your weight loss goals")
            recommendations.append("💪 Urgent: Adopt a calorie deficit diet (500-1000 cal/day reduction)")
            recommendations.append("🥗 Prioritize: Vegetables, lean proteins, whole grains, and fruits")
            if calories > 400:
                recommendations.append(f"❌ This {calories} cal meal is too high - aim for 300-400 cal per meal")
        
        # Calorie-based recommendations
        if calorie_percentage > 50:
            recommendations.append("⚠️ HIGH CALORIE ALERT: This is >50% of your daily needs - skip or drastically reduce portion")
        elif calorie_percentage > 40:
            recommendations.append("⚠️ This meal uses 40%+ of daily calories - balance with light meals")
        
        # Disease-specific urgent recommendations
        if diseases:
            for disease in diseases:
                if 'diabetes' in disease.lower():
                    if is_junk:
                        recommendations.append("🚨 DIABETIC ALERT: Junk food causes dangerous blood sugar spikes")
                if 'heart' in disease.lower():
                    if is_junk:
                        recommendations.append("❤️ HEART RISK: High-fat processed foods increase cardiovascular risk")
        
        # Warnings from suitability check
        if suitability['warnings']:
            recommendations.append("⚠️ HEALTH WARNINGS: Review all warnings above carefully before consuming")
        
        # Food quality recommendations
        health_score = food_data.get('foodQualityCycle', {}).get('healthScore', 5)
        if health_score < 4:
            recommendations.append("❌ POOR FOOD QUALITY: Choose fresher, less processed alternatives")
        elif health_score < 6:
            recommendations.append("⚠️ Consider healthier preparation methods (grilled, steamed, baked)")
        
        # Positive reinforcement for good choices
        if not is_junk and suitability['suitable'] and health_score >= 7:
            recommendations.append("✅ EXCELLENT CHOICE! This food aligns well with your health goals")
            if bmi_category == 'Normal weight':
                recommendations.append("👍 Keep making healthy choices like this to maintain your weight")
        
        # Always provide an actionable tip
        if not recommendations:
            recommendations.append("💡 Maintain a balanced diet with variety in nutrients")
        
        return recommendations[:7]  # Limit to 7 recommendations
